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

import MonitorFactory
import Settings

class GAutomator():
    menu = None
    tray_icon = None
    monitors = None

    def __init__(self):
        self.makeTrayIcon()
        self.setupMetaMenu()

    def makeTrayIcon(self):
        self.tray_icon = Gtk.StatusIcon()
        self.tray_icon.set_from_icon_name("applications-system")
        self.tray_icon.set_title("GAutomator")
        self.tray_icon.set_tooltip_text("Automate shit.")
        self.tray_icon.set_has_tooltip(True)
        self.tray_icon.set_visible(True)

    def setupMetaMenu(self):
        #item = Gtk.ImageMenuItem(Gtk.Stock.QUIT)
        #item.set_label("Quit")

        image = Gtk.Image()
        image.set_from_stock(Gtk.STOCK_QUIT, Gtk.IconSize.MENU)

        item = Gtk.ImageMenuItem("Quit")
        item.set_image(image)
        item.set_always_show_image(True)
        item.connect('activate', self.quit)

        self.menu = Gtk.Menu()
        self.menu.append(item)
        self.menu.show_all()

        self.tray_icon.connect("popup-menu", self.onMenuActivate)

    def onMenuActivate(self, icon, button, time):
        def pos(menu, icon):
            return (Gtk.StatusIcon.position_menu(menu, icon))

        self.menu.popup(None, None, pos, self.tray_icon, button, time)

    def makeMonitors(self):
        settings = Settings.makeSettings()
        factory = MonitorFactory.makeMonitorFactory(settings)
        self.monitors = factory.makeMonitors()

    def run(self):
        self.makeMonitors()
        Gtk.main()
        return 0

    def quit(self, item):
        Gtk.main_quit()
