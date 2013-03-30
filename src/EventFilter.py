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

import re
import Event

class EventFilter:
    def isSatisfiedBy(self, event):
        return True
    def postActionUpdate(self, event):
        pass
###############################################################################
CHANGES_DONE_SOURCE_EVENTS =\
    Event.CREATED | Event.CHANGED | Event.ATTRIBUTE_CHANGED

class EventTypeFilter(EventFilter):
    files_waiting_for_changes_done_event = []

    def __init__(self, allowed_events):
        self.allowed_events = allowed_events

    def isSatisfiedBy(self, event):
        event_type = event.getType()
        event_path = event.getFile().get_path()

        if event.isChangesDoneHint() and\
            self.isWaitingForChangesDone(event_path): return True

        event_matches = event.typeMatches(self.allowed_events)

        if event_matches and\
            self.shouldWaitForChangesDone(event_path, event): return False

        return event_matches

    def isWaitingForChangesDone(self, event_path):
        if event_path in self.files_waiting_for_changes_done_event:
            self.files_waiting_for_changes_done_event.remove(event_path)
            return True
        return False

    def shouldWaitForChangesDone(self, event_path, event):
        if event.typeMatches(CHANGES_DONE_SOURCE_EVENTS):
            self.files_waiting_for_changes_done_event.append(event_path)
            return True
        return False
###############################################################################
class FileRegexFilter(EventFilter):
    def __init__(self, regex):
        self.regex = re.compile(regex)

    def isSatisfiedBy(self, event):
        return self.regex.match(event.getFile().get_basename())
###############################################################################
class EventIntervalFilter(EventFilter):
    def __init__(self, interval):
        self.interval = interval
        self.files = {}

    def isSatisfiedBy(self, event):
        path = event.getFile().get_path()

        if path not in self.files: return True

        last_modified = self.files[path]
        now = event.getEventTime()
        return (now - last_modified) > self.interval

    def postActionUpdate(self, event):
        self.purge_expired(event.getEventTime())
        self.files[event.getFile().get_path()] = event.getEventTime()

    def purge_expired(self, now):
        self.files = {k: v for (k, v) in self.files.items() \
            if now - v <= self.interval }
###############################################################################
class MimeTypeFilter(EventFilter):
    def __init__(self, mime_type):
        self.mime_type = mime_type

    def isSatisfiedBy(self, event):
        return True
###############################################################################
