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

from Action import Action
from DirectoryMonitor import DirectoryMonitor
from EventFilter import *
from Event import *


class MonitorFactory:
    def __init__(self, settings):
        self.settings = settings

    def makeMonitors(self):
        self.settings.load()

        monitors = []
        while self.settings.next():
            enabled = self.settings.getEnabled()
            if not enabled: continue

            path = self.settings.getPath()
            recurse = self.settings.getRecurse()
            action = makeAction(self.settings.getAction())
            filters = makeFilters(self.settings.getFilters())
            monitors.append(DirectoryMonitor(path,
                                             recurse,
                                             action,
                                             filters))
        return monitors


def makeAction(action):
    return Action(action)


def makeFilters(filtersConfig):
    result = []
    for filter in filtersConfig:
        result.append(makeFilter(filter))
    return result

#FIXME: Knows too much about the structure of the condition configuration
def makeFilter(filterConfig):
    type = filterConfig['type']

    if type == 'EventTypeFilter':
        event_types = filterConfig['event_types']
        return EventTypeFilter(makeEventTypes(event_types))

    elif type == 'FileRegexFilter':
        regex = filterConfig['regex']
        return FileRegexFilter(regex)

    elif type == 'EventIntervalFilter':
        interval = filterConfig['interval']
        return EventIntervalFilter(interval)

    elif type == 'MimeTypeFilter':
        mime_type = filterConfig['mime_type']
        return MimeTypeFilter(mime_type)

    else:
        raise Exception('Invalid Filter type "%s".' %(type))


def makeEventTypes(event_types):
    result = 0
    for et in event_types:
        result = result | EVENT_TYPES[et]
    return result


#In case we ever want/need multiple implementations
def makeMonitorFactory(settings):
    return MonitorFactory(settings)
