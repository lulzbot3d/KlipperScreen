# *********************************
# Lulzbot KlipperScreen Main Menu
# By Carl Smith  2024 - FAME3D
# *********************************

import logging
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib
from panels.menu import Panel as MenuPanel


class Panel(MenuPanel):
    def __init__(self, screen, title, items=None):
        super().__init__(screen, title, items)
        self.main_menu = Gtk.Grid()
        self.main_menu.set_hexpand(True)
        self.main_menu.set_vexpand(True)
        scroll = self._gtk.ScrolledWindow()

        logging.info("### Making Lulzbot MainMenu")

        # Build new top row live extruder temp, bed temp, and fan buttons.  Buttons are defined here
        # rather than in create_top_panel so they can be seen by the update routine
        self.ext_temp = self._gtk.Button('nozzle1', "°C", "color1", self.bts * 1.5, Gtk.PositionType.LEFT, 1)
        self.bed_temp = self._gtk.Button('bed', "°C", "color2", self.bts * 1.3, Gtk.PositionType.LEFT, 1)
        self.fan_spd = self._gtk.Button('fan', "%", "color3", self.bts * 1.5, Gtk.PositionType.LEFT, 1)
        self.top_panel = self.create_top_panel()
        self.main_menu.attach(self.top_panel, 0, 0, 3, 1)

        self.labels['menu'] = self.arrangeMenuItems(items, 2, True)
        scroll.add(self.labels['menu'])
        self.main_menu.attach(scroll, 1, 1, 1, 1)

        for child in self.labels['menu'].get_children():
            child.get_style_context().add_class("buttons_main_left")

        self.right_panel = self.create_right_panel()
        self.main_menu.attach(self.right_panel, 2, 1, 1, 1)

        self.content.add(self.main_menu)

    def process_update(self, action, data):
        if action != "notify_status_update":
            return
        self.update_top_panel()

    def create_top_panel(self):
        # Buttons are defined in the init so they can be seen by the update routine

        self.ext_temp.connect("clicked", self.menu_item_clicked, {"name": "Temperature", "panel": "temperature"})
        self.bed_temp.connect("clicked", self.menu_item_clicked, {"name": "Temperature", "panel": "temperature"})
        self.fan_spd.connect("clicked", self.menu_item_clicked, {"name": "Fan", "panel": "fan"})

        self.ext_temp.get_style_context().add_class("buttons_main_top")
        self.ext_temp.get_style_context().add_class("main_temp_off")

        self.bed_temp.get_style_context().add_class("buttons_main_top")
        self.bed_temp.get_style_context().add_class("main_temp_off")

        self.fan_spd.get_style_context().add_class("buttons_main_top")
        self.fan_spd.get_style_context().add_class("main_temp_off")

        top = Gtk.Grid(row_homogeneous=True, column_homogeneous=True)
        top.set_property("height-request", 80)
        top.set_vexpand(False)
        top.set_margin_bottom(10)
        top.attach(self.ext_temp, 0, 0, 1, 1)
        top.attach(self.bed_temp, 1, 0, 1, 1)
        top.attach(self.fan_spd, 2, 0, 1, 1)

        return top

    def update_top_panel(self):
        ext_temp = self._printer.get_dev_stat("extruder", "temperature")
        ext_target = self._printer.get_dev_stat("extruder", "target")
        ext_label = f"{int(ext_temp)} / {int(ext_target)}°C"

        bed_temp = self._printer.get_dev_stat("heater_bed", "temperature")
        bed_target = self._printer.get_dev_stat("heater_bed", "target")
        bed_label = f" {int(bed_temp)} / {int(bed_target)}°C"

        fs = self._printer.get_fan_speed("fan")
        fan_label = f" {float(fs) * 100:.0f}%"

        if ext_target > 0:
            self.ext_temp.get_style_context().remove_class("main_temp_off")
            self.ext_temp.get_style_context().add_class("main_temp_on")
        else:
            self.ext_temp.get_style_context().remove_class("main_temp_on")
            self.ext_temp.get_style_context().add_class("main_temp_off")

        if bed_target > 0:
            self.bed_temp.get_style_context().remove_class("main_temp_off")
            self.bed_temp.get_style_context().add_class("main_temp_on")
        else:
            self.bed_temp.get_style_context().remove_class("main_temp_on")
            self.bed_temp.get_style_context().add_class("main_temp_off")

        if fs > 0:
            self.fan_spd.get_style_context().remove_class("main_temp_off")
            self.fan_spd.get_style_context().add_class("main_temp_on")
        else:
            self.fan_spd.get_style_context().remove_class("main_temp_on")
            self.fan_spd.get_style_context().add_class("main_temp_off")

        self.ext_temp.set_label(ext_label)
        self.bed_temp.set_label(bed_label)
        self.fan_spd.set_label(fan_label)
        return

    def create_right_panel(self):
        self.change = self._gtk.Button('Filament3', " Filament", "button_change", self.bts * 3,
                                       Gtk.PositionType.LEFT, 2)
        self.change.connect("clicked", self.menu_item_clicked, {"name": "Filament", "panel": "filament"})

        self.preheat = self._gtk.Button('heat-up', " Preheat", "button_change", self.bts * 3,
                                        Gtk.PositionType.LEFT, 2)
        self.preheat.connect("clicked", self.preheat_clicked)

        self.print = self._gtk.Button('print', " Print", "button_print", self.bts * 3, Gtk.PositionType.LEFT, 1)
        self.print.connect("clicked", self.menu_item_clicked, {"name": "Print", "panel": "print"})

        right = Gtk.Grid(row_homogeneous=True, column_homogeneous=True)
        right.set_property("width-request", 300)
        right.set_vexpand(True)
        right.set_hexpand(False)
        right.attach(self.preheat, 0, 0, 1, 1)
        right.attach(self.change, 0, 1, 1, 1)
        right.attach(self.print, 0, 2, 1, 1)
        return right

    def preheat_clicked(self, widget):
        self._screen._ws.klippy.gcode_script("SET_HEATER_TEMPERATURE HEATER=extruder TARGET=180")
        self._screen._ws.klippy.gcode_script("SET_HEATER_TEMPERATURE HEATER=heater_bed TARGET=60")
        return
