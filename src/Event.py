# Copyright (C) Axel von Bertoldi 2013 <bertoldia@gmail.com>
#
# gautomator is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# gautomator is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.

import time
from gi.repository import Gio

CHANGED           = 1 << Gio.FileMonitorEvent.CHANGED
CHANGES_DONE_HINT = 1 << Gio.FileMonitorEvent.CHANGES_DONE_HINT
DELETED           = 1 << Gio.FileMonitorEvent.DELETED
CREATED           = 1 << Gio.FileMonitorEvent.CREATED
ATTRIBUTE_CHANGED = 1 << Gio.FileMonitorEvent.ATTRIBUTE_CHANGED
PRE_UNMOUNT       = 1 << Gio.FileMonitorEvent.PRE_UNMOUNT
UNMOUNTED         = 1 << Gio.FileMonitorEvent.UNMOUNTED
MOVED             = 1 << Gio.FileMonitorEvent.MOVED

EVENT_TYPES = {
    'CHANGED': CHANGED,
    'CHANGES_DONE_HINT': CHANGES_DONE_HINT,
    'DELETED': DELETED,
    'CREATED': CREATED,
    'ATTRIBUTE_CHANGED': ATTRIBUTE_CHANGED,
    'PRE_UNMOUNT': PRE_UNMOUNT,
    'UNMOUNTED': UNMOUNTED,
    'MOVED': MOVED
}

class Event:
    def __init__(self, event_type, gfile, other_file):
        self.event_type = (1 << event_type)
        self.gfile = gfile
        self.other_file = other_file
        self.event_time = time.time()

    def getFile(self):
        if self.isMoved() and self.other_file != None:
            return self.other_file
        return self.gfile

    def getType(self):
        return self.event_time

    def typeMatches(self, event_types):
        return (self.event_type & event_types > 0)

    def fileEquals(self, gfile):
        return (self.gfile.get_path() == gfile.get_path())

    def getEventTime(self):
        return self.event_time

    def isDirectory(self):
        return self.gfile.query_file_type(Gio.FileQueryInfoFlags.NONE, None) == \
            Gio.FileType.DIRECTORY

    def isChanged(self):
        return self.event_type == CHANGED
    def isChangesDoneHint(self):
        return self.event_type == CHANGES_DONE_HINT
    def isDeleted(self):
        return self.event_type == DELETED
    def isCreated(self):
        return self.event_type == CREATED
    def isAttributeChanged(self):
        return self.event_type == ATTRIBUTE_CHANGED
    def isPreUnmount(self):
        return self.event_type == PRE_UNMOUNT
    def isUnmounted(self):
        return self.event_type == UNMOUNTED
    def isMoved(self):
        return self.event_type == MOVED
