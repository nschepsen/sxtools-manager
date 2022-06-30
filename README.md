## PROJECT ##

* ID: **S**xTools!**M**ANAGER
* Contact: git@schepsen.eu

## DESCRIPTION ##

**S**xTools!**M**ANAGER helps you to manage a video collection according to your wishes

### WHAT'S IMPLEMENTED?! ###

TBA

### SCREENSHOTS ###

TBA

## CHANGELOG ##

### SxTools!MANAGER 1.2.0-beta.3 ###

* Add Qt6-based UI (PySide6) Prototype
* Add Thumbnails for Scene(s), see "Scan Perform" action
* Add cache() for thumbnails and other temp files
* Fix Typos
* Update Performer & Paysite DB to the latest version

### SxTools!MANAGER 1.2.0-beta.2 ###

* Add "CLI"-client console (commands: :v, :q, :s, :f[ path], :a, :cl)
* Add a better date parser, part of self.analyse(s: Scene)
* Add a duplicate detection method; keep, remove or skip
* Fix #1: 1-Token-Name vs. Unknown Performer's name starting with the same token
* Fix wiping sitemap by --dry-run & changes
* Implement the sortmap() to keep the DB sorted
* Rewrite the ffprobe part of Scene.__init__() as an own method for performance and reuse reasons

### SxTools!MANAGER 1.2.0-beta.1 ###

* Add 'ffprobe' support to read out scene's metadata
* Add a logger ('~/sxtools/sXtools.log') for a better debugging experience
* Convert the app to a pip package, e.g. 'pip install sxtools'
* Rewrite the "CLI"-client and improve its performance
* Split the app in Core, CLI & GUI (using Qt6) modules

### SxTools!MANAGER 1.0.1, updated @ 2021-04-28 ###

* Add Support for different Scene Releases
* Fix Typo
* Update Performer & Publisher DB to the latest version

### SxTools!MANAGER 1.0.0, updated @ 2021-04-21 ###

* Initial Release
