#!/usr/bin/python3
#
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

from gi.repository import Gtk
import sys
import MonitorFactory
import Settings

#Comment the first line and uncomment the second before installing
#or making the tarball (alternatively, use project variables)
UI_FILE = "gautomator.ui"
#UI_FILE = "/usr/local/share/gautomator/ui/gautomator.ui"


class GAutomator:
    def __init__(self):
        self.builder = Gtk.Builder()
        self.builder.add_from_file(UI_FILE)
        self.builder.connect_signals(self)
        window = self.builder.get_object('window')
        window.connect('delete-event', destroy)
        window.show_all()

        settings = Settings.makeSettings()
        factory = MonitorFactory.makeMonitorFactory(settings)
        self.monitors = factory.makeMonitors()

def main():
    app = GAutomator()
    Gtk.main()

def destroy(window, event):
    Gtk.main_quit()

if __name__ == "__main__":
    sys.exit(main())
