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

from gi.repository import Gio, GLib
from Event import Event

def isDirectory(gfile):
    return gfile.query_file_type(Gio.FileQueryInfoFlags.NONE, None) == \
           Gio.FileType.DIRECTORY

def infoIsDirectory(file_info):
    return file_info.get_file_type() == Gio.FileType.DIRECTORY


class DirectoryMonitor:
    def __init__(self, path, recurse, action, conditions):
        directory = Gio.File.new_for_path(path)
        if not isDirectory(directory):
            raise Exception("Error: '%s' is not a directory." %(path))

        self.directory = directory
        self.recurse = recurse
        self.action = action
        self.conditions = conditions
        self.sub_monitors = {}
        self.monitor = None

        self.setupMonitor()
        self.setupSubMonitors()

    def setupMonitor(self):
        self.monitor = \
            self.directory.monitor_directory(Gio.FileMonitorFlags.SEND_MOVED, None)
        #self.monitor.set_rate_limit(5000) # 5 seconds
        self.monitor.connect('changed', self.onChangedEvent)
        print("Created monitor at '%s'" %(self.directory.get_path()))

    def setupSubMonitors(self):
        if self.recurse:
            self.addSubMonitors()

    def addSubMonitors(self):
        try:
            children = self.directory.enumerate_children('standard::name,' + \
                                                         'standard::type',
                                                         Gio.FileQueryInfoFlags.NONE,
                                                         None)
            for child in children:
                if infoIsDirectory(child):
                    child_file = self.directory.get_child(child.get_name())
                    child_name = child_file.get_path()
                    self.addSubMonitor(child_name)

        except GLib.Error as e:
            print("Error while creating recursive monitors: %s" %(e.message))

    def addSubMonitor(self, sub_dir):
        try:
            self.sub_monitors[sub_dir] = DirectoryMonitor(sub_dir,
                                                          self.recurse,
                                                          self.action,
                                                          self.conditions)
        except GLib.Error as e:
            print("Failed to create monitor at: %s" %(e.message))

    def checkConditionsSatified(self, event):
        for condition in self.conditions:
            if not condition.isSatisfiedBy(event):
                return False
        return True

    def doPostActionUpdate(self, event):
        for condition in self.conditions:
            condition.postActionUpdate(event)

    def onChangedEvent(self, monitor, gfile, other_file, event_type):
        event = Event(event_type, gfile, other_file)
        print("Got '%s' on '%s'" %(event_type, gfile.get_path()))

        if not self.handleDirectoryEvent(event) and \
               self.checkConditionsSatified(event):
            self.action.execute(gfile)
            self.doPostActionUpdate(event)

    def handleDirectoryEvent(self, event):
        if event.isCreated() and event.isDirectory():
            self.addSubMonitor(event.getFile().get_path())
            return True
        elif event.isMoved() and isDirectory(event.other_file):
            self.removeSubMonitor(event)
            return self.addSubMonitor(event.other_file.get_path())
        elif event.isDeleted():
            return self.removeSubMonitor(event)

    def removeSubMonitor(self, event):
        path = event.getFile().get_path()
        if path in self.sub_monitors:
            print("Destroy monitor at '%s'" %(path))
            del(self.sub_monitors[path]) # is this really working?
            return True
        return False
