# Wake Speaker NVDA Add-on #

This plugin emits white noise at a very low volume to keep the speakers awake. This is useful if you have speakers that go to sleep when they stop receiving an audio stream, usually to save power.

Copyright (C) 2023 David CM <dhf360@gmail.com>

This package is distributed under the terms of the GNU General Public License, version 2 or later.

## How does this plugin differ from existing ones?

The idea came after a need for some bluetooth headphones, which require that the audio flow be paused from time to time in order to maintain the low latency mode. Otherwise, latency increases or audio is interrupted at times.

If you don't have such a need, you can use the add-on with its basic functionality. If you need this additional feature, then check the settings to adapt it to your needs.

## Download.
 The latest release is available to [download in this link](https://davidacm.github.io/getlatest/gh/davidacm/WakeSpeaker/?index=1)

## Usage and settings.

When you install this plugin, it will be active by default.

This add-on has a script to toggle the state of the add-on (on or off) without gesture assigned. You can assign gestures in the "Input Gestures" dialog.

If you want to change some features, go to NVDA Options, Wake Speaker category, and adjust any of the following options:

* Enable Wake Speaker: Toggles the functionality of the add-on.
* Sleep After (seconds): The amount of time before suspending the noise stream used to keep the audio output awake. The time starts from the last time NVDA produced voice or tones. By default 60 seconds.
* Noise volume: the volume of white noise, default is 0. Increase it if 0 level is not enough for your output device.
* Try to pause noise after (Seconds): this will try to pause audio after n seconds, the add-on will try until there is no other NVDA audio stream during the pause. keep this parameter at 0 if you don't need this feature. If you have an audio stream external to NVDA, such as when listening to music, pausing the stream will have no effect.
* Pause length (MS): the time that the pause lasts in milliseconds, this parameter only has effect if the previous one is active.

## Requirements
  You need NVDA 2019.3 or later.

## contributions, reports and donations

If you like my project or this software is useful for you in your daily life and you would like to contribute in some way, you can donate via the following methods:

* [PayPal.](https://paypal.me/davicm)
* [Ko-fi.](https://ko-fi.com/davidacm)
* [cryptocurrencies and other methods.](https://davidacm.github.io/donations/)

If you want to fix bugs, report problems or new features, you can contact me at: <dhf360@gmail.com>.

  Or in the github repository of this project:
  [Wake Speaker on GitHub](https://github.com/davidacm/WakeSpeaker)

    You can get the latest release of this add-on in that repository.
