# ● wake Speaker
# -*- coding: UTF-8 -*-
# Copyright (C) 2023 David CM
import time, threading
from ctypes import c_short
from io import BytesIO
from random import uniform

import addonHandler, atexit, config, globalPluginHandler, nvwave, speech, tones, wx
from synthDriverHandler import synthDoneSpeaking
from gui import guiHelper, nvdaControls, settingsDialogs, SettingsPanel
from ._configHelper import configSpec, registerConfig
addonHandler.initTranslation()


@configSpec('wakeSpeaker')
class AppConfig:
	wakeSpeaker = "boolean(default=True)"
	keepAlive = "integer(default=60, min=0)"
	noiseVolume = "integer( default=0, min=0, max=100)"
	smallPauseAfter = "integer(default=0)"
	pauseSizeMs = "integer(default=500)"
AF = registerConfig(AppConfig)


def createWhiteNoise(ms, vol=0, stereo=True, sampleRate=44100, bytes=2):
	vol = vol / 2000
	MAX_AMPLITUDE = int(2 ** (bytes * 8) / 2) - 1
	b = BytesIO()
	for i in range(int(sampleRate *ms/1000)):
		v = int(uniform(-1, 1) *vol *MAX_AMPLITUDE)
		v = c_short(v)
		b.write(v)
		if stereo:
			b.write(v)
	return b


class Waker(threading.Thread):
	def __init__(self):
		super().__init__()
		self.sampleRate = 44100
		self.volume = AF.noiseVolume
		self.device = None
		self.samples = None
		self.player = None
		# event to start to wake the speaker.
		self.wakeEvent = threading.Event()
		# the last time the speaker stopped being asleep
		self.wakeStart = None
		# the last time the wake signal was sent.
		self.currentWakeStart = None
		# flag to stop the thread.
		self.stopFlag = False
		# flag to determine if another audio stream is active.
		self.isAudioActive = False
		self.chunkSize = 4000

	def updateNoiseVolume(self):
		self.setPlayer()
		if self.samples == None or self.volume != AF.noiseVolume:
			self.volume = AF.noiseVolume
			self.samples = createWhiteNoise(1000, self.volume, stereo=True)

	def setPlayer(self):
		device = config.conf["speech"]["outputDevice"]
		if device != self.device:
			self.device = device
			self.player = nvwave.WavePlayer(2, self.sampleRate, 16, outputDevice=device, wantDucking=False, buffered=True)

	def elapsed(self):
		return time.time() - self.currentWakeStart if self.currentWakeStart else 0

	def elapsedWake(self):
		# this method returns the time since the first time the wake was started.
		# this attribute will be reset when the noise make a pause.
		return time.time() - self.wakeStart if self.wakeStart else 0

	def run(self):
		# the noise is sent in small chunks, to listen the signals between chunks.
		self.wakeStart = time.time()
		while True:
			if self.stopFlag:
				break
			self.wakeEvent.wait()
			self.wakeEvent.clear()
			self.updateNoiseVolume()
			self.currentWakeStart = time.time()
			if self.wakeStart == 0:
				self.wakeStart = time.time()
			self.samples.seek(0)
			while not self.wakeEvent.is_set():
				if self.elapsed() > AF.keepAlive:
					self.wakeStart = 0
					break
				if AF.smallPauseAfter != 0 and self.elapsedWake() > AF.smallPauseAfter and not self.isAudioActive:
					self.player.stop()
					time.sleep(AF.pauseSizeMs /1000)
					# if a signal of other player was detected during the pause, the elapced time won't be reset to try the pause again
					if not self.isAudioActive:
						self.wakeStart = time.time()
				data = self.samples.read(self.chunkSize)
				if data == b'':
					self.samples.seek(0)
					continue
				self.player.feed(data)
		self.player.close()
		self.player= None

	def wake(self):
		# if this method is called during a pause of data sending, this will indicate that the pause failed because new data by another stream was sent.
		self.isAudioActive = True
		self.wakeEvent.set()

	def externalAudioStopped(self):
		""" this method set the flag to indicates that no audio is being send from another player, like a synthesizer.
		is not possible to determine if the tone beep function is running, because this function has not a stop or done signal.
		this method should be called when the synth voice stops.
		"""
		self.isAudioActive = False

	def terminate(self):
		self.stopFlag = True
		self.wakeEvent.set()
waker = None


def extensionBeep(*args, **qwargs):
	waker.wake()
	return True


def extensionSynthDone(*args, **kwargs):
	waker.externalAudioStopped()
	return True


def makeFakeFunction(origFunc, signalFunc):
	def fake(*args, **kwargs):
		origFunc(*args, **kwargs)
		signalFunc()
		return True
	return fake


origBeep = tones.beep
origSpeak = speech._manager.speak
origCancel = speech._manager.cancel
def patchNVDA(waker):
	# patch beep
	try:
		from tones import decide_beep as d
		d.register(extensionBeep)
		d.moveToEnd(extensionBeep)
	except:
		fakeBeep = makeFakeFunction(origBeep, waker.wake)
		tones.beep = fakeBeep
	# patch speak
	fakeSpeak = makeFakeFunction(origSpeak, waker.wake)
	fakeCancel = makeFakeFunction(origCancel, waker.externalAudioStopped)
	speech._manager.speak = fakeSpeak
	speech._manager.cancel = fakeCancel
	synthDoneSpeaking.register(extensionSynthDone)


def unpatchNVDA():
	try:
		from tones import decide_beep as d
		d.unregister(extensionBeep)
	except:
		tones.beep = origBeep
	speech._manager.speak = origSpeak
	speech._manager.cancel = origCancel
	synthDoneSpeaking.unregister(extensionSynthDone)


class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	def __init__(self):
		super(globalPluginHandler.GlobalPlugin, self).__init__()
		self.handleConfigProfileSwitch()
		settingsDialogs.NVDASettingsDialog.categoryClasses.append(WakeSpeakerSettings)
		config.post_configProfileSwitch.register(self.handleConfigProfileSwitch)

	def terminate(self):
		super(GlobalPlugin, self).terminate()
		self.disableAddon()

	def disableAddon(self):
		unpatchNVDA()
		waker.terminate()

	def handleConfigProfileSwitch(self):
		global waker
		if not AF.wakeSpeaker :
			self.disableAddon()
			waker = None
			return
		if not waker:
			waker = Waker()
			waker.start()
		patchNVDA(waker)


class WakeSpeakerSettings(SettingsPanel):
	# Translators: The label for the NVDA's settings category.
	title = _("Wake Speaker")

	def makeSettings(self, settingsSizer):
		sHelper = guiHelper.BoxSizerHelper(self, sizer=settingsSizer)

		# Translators: toggle the add-on functionality.
		self.enableAddon = sHelper.addItem(
			wx.CheckBox(self, label=_("&Enable Wake Speaker"))
		)
		self.enableAddon.SetValue(AF.wakeSpeaker)

		# Translators: the time to keep alive the speaker.
		self.keepAlive = sHelper.addLabeledControl(_("&Sleep after (seconds)"), nvdaControls.SelectOnFocusSpinCtrl, min=1, max=1800, initial=AF.keepAlive)

		# Translators: the noise volume value.
		self.noise = sHelper.addLabeledControl(_("Noise volume"), nvdaControls.EnhancedInputSlider, minValue=0,maxValue=100)
		self.noise.SetValue(AF.noiseVolume)
		# Translators: the time to make a small pause since the noise started the first time.
		self.pauseAfter = sHelper.addLabeledControl(_("&Try to pause noise after (seconds)"), nvdaControls.SelectOnFocusSpinCtrl, min=0, max=1800, initial=AF.smallPauseAfter)
		# Translators: the length of the pause (in MS)
		self.pauseSize = sHelper.addLabeledControl(_("&Pause length (in MS)"), nvdaControls.SelectOnFocusSpinCtrl, min=5, max=3000, initial=AF.pauseSizeMs)

	def onSave(self):
		AF.wakeSpeaker = self.enableAddon.GetValue()
		AF.keepAlive = self.keepAlive.GetValue()
		AF.noiseVolume = self.noise.GetValue()
		AF.smallPauseAfter = self.pauseAfter.GetValue()
		AF.pauseSizeMs = self.pauseSize.GetValue()
		config.post_configProfileSwitch.notify()
