# ● wake Speaker
# -*- coding: UTF-8 -*-
# Copyright (C) 2023 David CM
import time, threading
from ctypes import c_short
from io import BytesIO
from random import randint

import addonHandler, config, core, globalPluginHandler, gui, nvwave, speech, tones, ui, wx
from synthDriverHandler import synthDoneSpeaking
from gui import nvdaControls
from ._configHelper import configSpec, registerConfig, boolValidator

addonHandler.initTranslation()


@configSpec('wakeSpeaker')
class AppConfig:
	wakeSpeaker = "boolean(default=True)"
	connectSignals = ('boolean(default=True)', True, boolValidator)
	keepAlive = "integer(default=60, min=0)"
	noiseVolume = "integer( default=0, min=0, max=100)"
	smallPauseAfter = "integer(default=0)"
	pauseSizeMs = "integer(default=500)"
AF = registerConfig(AppConfig)


def createWhiteNoise(ms, vol, stereo=True, sampleRate=44100, bytes=2):
	vol = vol / 2000
	boundaries = int((2 ** (bytes * 8) / 2 -1) * vol)
	b = BytesIO()
	for i in range(int(sampleRate *ms/1000)):
		v = c_short(randint(-boundaries, boundaries))
		b.write(v)
		if stereo:
			b.write(v)
	return b


class Waker(threading.Thread):
	"""
	This thread will emit a white noise during N seconds since the last wake signal was received.
	The stream is send in chunks, to check conditions before send each chunk.
	If configured, this thread will do a pause after N seconds since the first wake signal of the curent stream.
	To do the pause, isAudioActive must be false before starting and after ending the sleep. The thread will try this indefinitely until those conditions are met or the stream ends.
	To wake up the stream, use the "wake" method.
	To indicate that external audio sptreams ended, use the "externalAudioStopped" method. This is important to detect if other audio streams are active.
	"""
	def __init__(self):
		super().__init__()
		self.sampleRate = 44100
		self.CHUNK_SIZE = 4000
		self.volume = AF.noiseVolume
		self.device = None
		self.samples = None
		self.player = None
		# event to start sending audio.
		self.wakeEvent = threading.Event()
		self.wakeStart = 0
		self.lastWakeTime = 0
		self.endFlag = False
		self.isAudioActive = True
		self.play = False
		self.connectSignals = False

	def updateNoiseVolume(self):
		self.setPlayer()
		if self.samples == None or self.volume != AF.noiseVolume:
			self.volume = AF.noiseVolume
			self.samples = createWhiteNoise(1000, self.volume)

	def setPlayer(self):
		device = config.conf["speech"]["outputDevice"]
		if device != self.device:
			self.device = device
			self.player = nvwave.WavePlayer(2, self.sampleRate, 16, outputDevice=device, wantDucking=False, buffered=True)

	def elapsed(self):
		return time.time() - self.lastWakeTime

	def streamElapsed(self):
		return time.time() - self.wakeStart

	def run(self):
		while True:
			self.wakeEvent.wait()
			self.wakeEvent.clear()
			if self.endFlag:
				break
			if not self.play:
				continue
			self.updateNoiseVolume()
			self.lastWakeTime = time.time()
			if self.wakeStart == 0:
				self.wakeStart = time.time()
			while not self.wakeEvent.is_set():
				data = self.samples.read(self.CHUNK_SIZE)
				if data == b'':
					self.samples.seek(0)
					continue
				self.player.feed(data)
				if not self.play:
					self.player.stop()
					self.wakeStart = 0
					break
				if not self.connectSignals:
					continue
				if self.elapsed() > AF.keepAlive:
					self.player.stop()
					self.wakeStart = 0
					break
				if AF.smallPauseAfter != 0 and self.streamElapsed() > AF.smallPauseAfter and not self.isAudioActive:
					self.player.stop()
					time.sleep(AF.pauseSizeMs /1000)
					if not self.isAudioActive:
						self.wakeStart = time.time()
		self.player.close()
		self.player= None

	def notify(self):
		if self.play:
			self.wakeEvent.set()

	def wake(self):
		self.isAudioActive = True
		self.notify()

	def togglePlay(self, switch):
		"""
		plays or pauses the white noise stream, it's used to toggle the addon.
		"""
		self.play = switch
		self.notify()

	def externalAudioStopped(self):
		self.isAudioActive = False

	def terminate(self):
		self.endFlag = True
		self.wakeEvent.set()
waker = Waker()


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
def patchNVDA(waker: Waker):
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
	# Translators: script category for add-on gestures
	scriptCategory = _("Wake Speaker")

	def __init__(self):
		super().__init__()
		if AF.connectSignals:
			patchNVDA(waker)
			waker.connectSignals = True
		self.handleConfigProfileSwitch()
		gui.settingsDialogs.NVDASettingsDialog.categoryClasses.append(WakeSpeakerSettings)
		config.post_configProfileSwitch.register(self.handleConfigProfileSwitch)
		waker.start()

	def terminate(self):
		super().terminate()
		if waker.connectSignals:
			unpatchNVDA()
		waker.terminate()

	def handleConfigProfileSwitch(self):
		waker.togglePlay(AF.wakeSpeaker)

	def script_toggleWakeSpeaker(self, gesture):
		AF.wakeSpeaker = not AF.wakeSpeaker
		self.handleConfigProfileSwitch()
		# Translators: message to announce the add-on state (on or off) the %s is the part of the state of the add-on.
		ui.message(_("Wake speaker %s" % (_("on") if AF.wakeSpeaker else _("off"))))
	# Translators: toggle wake speaker functionality.
	script_toggleWakeSpeaker.__doc__ = _("toggles the wake speaker functionality")


def promptUserForRestart():
	restartMessage = _(
		# Translators: A message asking the user if they wish to restart NVDA
		# as the connect signals option requires restart to take effect.
		"The option Listen voice and beep signals has been changed. "
		"You must restart NVDA for that change to take effect. "
		"Would you like to restart now?"
	)
	# Translators: Title for message asking if the user wishes to restart NVDA as addons have been added or removed.
	restartTitle = _("Restart NVDA")
	result = gui.messageBox(
		message=restartMessage,
		caption=restartTitle,
		style=wx.YES | wx.NO | wx.ICON_WARNING
	)
	if wx.YES == result:
		core.restart()


class WakeSpeakerSettings(gui.SettingsPanel):
	# Translators: The label for the NVDA's settings category.
	title = _("Wake Speaker")

	def makeSettings(self, settingsSizer):
		sHelper = gui.guiHelper.BoxSizerHelper(self, sizer=settingsSizer)

		# Translators: toggle the add-on functionality.
		self.enableAddon = sHelper.addItem(
			wx.CheckBox(self, label=_("&Enable Wake Speaker"))
		)
		self.enableAddon.SetValue(AF.wakeSpeaker)
		self.enableAddon.Bind(wx.EVT_CHECKBOX, self.onToggleAddon)

		# Translators: toggles the listening of voice and beep signals.
		self.connectSignals  = sHelper.addItem(
			wx.CheckBox(self, label=_("&Listen voice and beep signals (disable if there are issues with other add-ons)"))
		)
		self.connectSignals .SetValue(AF.connectSignals )
		self.connectSignals .Bind(wx.EVT_CHECKBOX, self.onToggleConnectSignals )

		# Translators: the time to keep alive the speaker.
		self.keepAlive = sHelper.addLabeledControl(_("&Sleep after (seconds)"), nvdaControls.SelectOnFocusSpinCtrl, min=1, max=1800, initial=AF.keepAlive)

		# Translators: the noise volume value.
		self.noise = sHelper.addLabeledControl(_("Noise volume"), nvdaControls.EnhancedInputSlider, minValue=0,maxValue=100)
		self.noise.SetValue(AF.noiseVolume)
		# Translators: the time to make a small pause since the noise started the first time.
		self.pauseAfter = sHelper.addLabeledControl(_("&Try to pause noise after (seconds)"), nvdaControls.SelectOnFocusSpinCtrl, min=0, max=1800, initial=AF.smallPauseAfter)
		# Translators: the length of the pause (in MS)
		self.pauseSize = sHelper.addLabeledControl(_("&Pause length (in MS)"), nvdaControls.SelectOnFocusSpinCtrl, min=5, max=3000, initial=AF.pauseSizeMs)
		self.onToggleAddon()

	def toggleControls(self,controls, toggle):
		for k in controls:
			if toggle:
				k.Show()
			else:
				k.Hide()

	def onToggleAddon(self, e=None):
		if self.enableAddon.GetValue():
			self.toggleControls((self.connectSignals, self.noise), True)
			self.onToggleConnectSignals()
		else:
			self.toggleControls((self.connectSignals, self.noise, self.keepAlive, self.pauseAfter, self.pauseSize), False)

	def onToggleConnectSignals (self, e=None):
		self.toggleControls((self.keepAlive, self.pauseAfter, self.pauseSize), self.connectSignals.GetValue())

	def onSave(self):
		AF.wakeSpeaker = self.enableAddon.GetValue()
		AF.keepAlive = self.keepAlive.GetValue()
		AF.noiseVolume = self.noise.GetValue()
		AF.smallPauseAfter = self.pauseAfter.GetValue()
		AF.pauseSizeMs = self.pauseSize.GetValue()
		signals = AF.connectSignals
		AF.connectSignals = self.connectSignals.GetValue()
		config.post_configProfileSwitch.notify()
		if signals != AF.connectSignals:
			promptUserForRestart()
