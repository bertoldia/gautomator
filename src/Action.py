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

from gi.repository import GLib

class Action:
    def __init__(self, command):
        self.command = command

    def execute(self, gfile):
        path = gfile.get_path()
        wd = gfile.get_parent().get_path()

        argv = self.makeArgv(path)
        cmdLine = " ".join(argv)
        print("Executing '%s'" %(cmdLine))

        try:
            GLib.spawn_async(argv, working_directory = wd, \
                             flags = GLib.SPAWN_SEARCH_PATH)
        except GLib.Error as e:
            print("Failed to execute '%s': %s" %(cmdLine, e))

    def makeArgv(self, path):
        '''
        Split the command at every space character and replace %s with the file
        on which to execute the command.
        '''
        result = self.command.split(' ')
        i = 0
        while i < len(result):
            try:
                result[i] = result[i] %(path)
                break
            except TypeError as e:
                pass
            i += 1
        return result
