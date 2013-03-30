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

import os

os.getenv("HOME")

SETTINGS_DIR = os.getenv('HOME') + '/.config/gautomator'

######################## Settings interface ####################################
#FIXME: Do I really need this?
class Settings:
    def load():
        raise Exception('No default Settings implementation.')

    def write(data):
        raise Exception('No default Settings implementation.')

    def next():
        return False

    def getPath():
        return None

    def getAction():
        return None

    def getRecurse():
        return None

    def getFilters():
        return None

    def getEnabled():
        return False

######################## Yaml backend implementation ###########################
import yaml

YAML_SETTINGS_FILE_NAME = 'gautomator.yaml'
YAML_SETTINGS_PATH = SETTINGS_DIR + '/' + YAML_SETTINGS_FILE_NAME

class YamlSettings(Settings):
    i = -1;
    settings_loaded = False

    def load(self):
        stream = open(YAML_SETTINGS_PATH, 'r')
        self.settingsDict = yaml.load(stream)
        stream.close()
        self.monitors = self.settingsDict['monitors']
        self.settings_loaded = True

    def next(self):
        self.checkSettingsLoaded()
        self.i += 1
        return  self.i < len(self.monitors)

    def getPath(self):
        self.checkSettingsLoaded()
        if self.i < 0: self.next()
        return self.monitors[self.i]['path']

    def getAction(self):
        self.checkSettingsLoaded()
        if self.i < 0: self.next()
        return self.monitors[self.i]['action']

    def getRecurse(self):
        self.checkSettingsLoaded()
        if self.i < 0: self.next()
        return self.monitors[self.i]['recurse']

    def getEnabled(self):
        self.checkSettingsLoaded()
        if self.i < 0: self.next()
        return self.monitors[self.i]['enabled']

    #FIXME: Exposing details of config structure to caller :-|
    def getFilters(self):
        self.checkSettingsLoaded()
        if self.i < 0: self.next()
        return self.monitors[self.i]['filters']

    def write(self, data):
        pass

    #FIXME: This is crap. Need a better way to make sure load() is called
    #before any other methods, but don't want to do it at construction.
    def checkSettingsLoaded(self):
        if not self.settings_loaded:
            raise Exception("Setting have not been loaded yet.")


# Change the setting implementation used here.
def makeSettings():
    return YamlSettings()

