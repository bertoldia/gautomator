# GAutomator

**NOTE: This program is not yet ready for mass consumption.**

## Description

Monitor folders and execute a command when files are modified.

GAutomator monitors files in a specified folder; when a file in that folder is
modified GAutomator will run a configured command on said file.  In addition to
the command that is executed, one can configure filters that controls which
files in the folder (via regex, mime-type) and which events (create, modify,
etc.) will trigger the command. GAutomator can also automatically monitor
folders recursively.

A typical use case it to automatically compile your .tex files when you save
them, or automatically rename, rotate and resize pictures when you copy them
from your digital camera to your Photos folder.

## Details

GAutomator is writen in Python3 and uses GTK+/Gio.

## Features

* Configure folders to monitor.
* Configure command to run; one per folder being monitored.
* Configure events that should trigger the command to be run. Supports all file
  events Gio supports ( changed, changes_done_hint, deleted, created,
  attribute_changed, pre_unmount, unmounted, moved).
* Configure property of files that should trigger command (regex, mime-type).
* Optionally Monitor folders recursively.
