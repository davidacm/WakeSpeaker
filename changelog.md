# version 24.1.1

* added support for NVDA 2024.2.
* added a donation dialog to support the author with add-ons development.
* added turkish language.
* added an option to avoid patching NVDA functions. This can help to solve incompatibilities with some add-ons, but can affect the performance of audio devices.
* updated the locale strings and documentation.
* updated the spanish locale strings and documentation.
* Modified the settings dialog to hide or show just the needed parameters depending on the options checked.
* added a new version of configHelper, to allow set options for the general profile. This is required for the connectSignals option, because this option is not allowed to set for other profiles.
* modified the way of manage the waker thread. Now this thread is created when the add-on is imported, and if the add-on is disabled, the thread is not deleted, is just paused instead. This solves some issues when in some cases, NVDA failed to patch functions or duplicated threads.

# version 0.4.0

* ukrainian translation
* added turkish documentation.
* Added Simplified Chinese translation

# version 0.3

* updated turkish language.
* fixed a bug that causes a python error if the add-on was disabled and NVDA is restarted.
* added a script (without gesture assigned) to disable or enable the add-on
* added turkish locale strings.

# version 0.2

* modified the method to generate the white noise.
* added portuguese locale strings and documentation.
