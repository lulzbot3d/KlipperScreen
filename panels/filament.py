# ***********************************
# Lulzbot KlipperScreen Filament Menu
# By Carl Smith  2024 - FAME3D
# ***********************************

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Pango
from ks_includes.screen_panel import ScreenPanel


class Panel(ScreenPanel):
    def __init__(self, screen, title):
        super().__init__(screen, title)

        self.presets_low = [180, 200, 220, 240]
        self.presets_high = [210, 220, 240, 260]
        self.presets_active = self.presets_low
        self.right_button_mode = "Cooldown"
        self.load_unload_enabled = True

        self.filament_menu = Gtk.Grid()
        self.filament_menu.set_hexpand(True)
        self.filament_menu.set_vexpand(True)

        # These buttons are defined here so they can be seen by the update routine
        self.ext_temp = self._gtk.Button('nozzle1', "°C", "color1", self.bts * 1.5, Gtk.PositionType.LEFT, 1)
        self.right_button = self._gtk.Button(None, self.right_button_mode, "buttons_filament_preset", self.bts * 1.5, Gtk.PositionType.LEFT, 1)
        self.pre1 = self._gtk.Button(None, f"PLA, PVA, PVB = {self.presets_active[0]}°C", "buttons_filament_preset")
        self.pre2 = self._gtk.Button(None, f"TPU, Flexibles = {self.presets_active[1]}°C", "buttons_filament_preset")
        self.pre3 = self._gtk.Button(None, f"ABS, PETg, ASA = {self.presets_active[2]}°C", "buttons_filament_preset")
        self.pre4 = self._gtk.Button(None, f"Nylon, PC = {self.presets_active[3]}°C", "buttons_filament_preset")
        self.load = self._gtk.Button('arrow-down', " Load", "button_change", self.bts * 3, Gtk.PositionType.LEFT, 2)
        self.unload = self._gtk.Button('arrow-up', " Unload", "button_change", self.bts * 3, Gtk.PositionType.LEFT, 2)

        # Create and add panels
        self.top_panel = self.create_top_panel()
        self.filament_menu.attach(self.top_panel, 0, 0, 3, 1)

        self.preset_panel = self.create_preset_panel()
        self.filament_menu.attach(self.preset_panel, 0, 1, 1, 1)

        self.load_unload_panel = self.create_load_unload_panel()
        self.filament_menu.attach(self.load_unload_panel, 0, 2, 1, 1)

        self.sensor_panel = self.create_sensor_panel()
        self.filament_menu.attach(self.sensor_panel, 0, 3, 4, 1)

        self.content.add(self.filament_menu)


    def create_load_unload_panel(self):
        self.load.connect("clicked", self.load_clicked)
        self.unload.connect("clicked", self.unload_clicked)
        loadunload = Gtk.Grid(row_homogeneous=True, column_homogeneous=True)
        loadunload.set_vexpand(True)
        loadunload.set_hexpand(True)
        loadunload.set_margin_bottom(10)
        loadunload.attach(self.load, 0, 0, 2, 1)
        loadunload.attach(self.unload, 2, 0, 2, 1)
        return loadunload

    def load_clicked(self, widget):
        self._screen._ws.klippy.gcode_script("LOAD_FILAMENT")

    def unload_clicked(self, widget):
        self._screen._ws.klippy.gcode_script("UNLOAD_FILAMENT")


    def create_preset_panel(self):
        # Buttons are defined in the init so they can be seen by the update routine
        self.pre1.connect("clicked", self.pre1_clicked)
        self.pre2.connect("clicked", self.pre2_clicked)
        self.pre3.connect("clicked", self.pre3_clicked)
        self.pre4.connect("clicked", self.pre4_clicked)
        presets = Gtk.Grid(row_homogeneous=True, column_homogeneous=True)
        presets.set_property("height-request", 140)
        presets.set_vexpand(False)
        presets.set_hexpand(False)
        presets.set_margin_bottom(10)
        presets.attach(self.pre1, 0, 0, 2, 1)
        presets.attach(self.pre2, 0, 1, 2, 1)
        presets.attach(self.pre3, 2, 0, 2, 1)
        presets.attach(self.pre4, 2, 1, 2, 1)
        return presets


    def create_top_panel(self):
        # Some buttons are defined in the init so they can be seen by the update routine
        self.middle_button = self._gtk.Button(None, "Park for Change", "buttons_filament_preset", self.bts * 1.5, Gtk.PositionType.LEFT, 1)

        self.ext_temp.connect("clicked", self.menu_item_clicked, {"name": "Temperature", "panel": "temperature"})
        self.middle_button.connect("clicked", self.middle_button_clicked)
        self.right_button.connect("clicked", self.right_button_clicked)

        self.ext_temp.get_style_context().add_class("buttons_main_top")
        self.ext_temp.get_style_context().add_class("main_temp_off")

        top = Gtk.Grid(row_homogeneous=True, column_homogeneous=True)
        top.set_property("height-request", 80)
        top.set_vexpand(False)
        top.set_margin_bottom(10)
        top.attach(self.ext_temp, 0, 0, 1, 1)
        top.attach(self.middle_button, 1, 0, 1, 1)
        top.attach(self.right_button, 2, 0, 1, 1)
        return top

    def middle_button_clicked(self, widget):
        y_filament_change = float(self._printer.get_config_section('stepper_y')['position_min']) + 1.0
        if self._printer.get_stat("toolhead", "homed_axes") != "xyz":
            self._screen._ws.klippy.gcode_script("G28")
        if self._printer.state == "printing":
            self._screen._ws.klippy.gcode_script("PAUSE PARK=false")
            self._screen._ws.klippy.gcode_script(f"G1 X30 Y{y_filament_change} F6000")
        elif self._printer.state == "paused":
            self._screen._ws.klippy.gcode_script(f"G1 X30 Y{y_filament_change} F6000")
        else:
            self._screen._ws.klippy.gcode_script("Park_Nozzle")

    def right_button_clicked(self, widget):
        if self.right_button_mode == "Pause":
            self._screen._ws.klippy.gcode_script("PAUSE")
        elif self.right_button_mode == "Resume":
            self._screen._ws.klippy.gcode_script("RESUME")
        elif self.right_button_mode == "Cooldown":
            self._screen._ws.klippy.gcode_script("SET_HEATER_TEMPERATURE HEATER=extruder TARGET=0")
            self._screen._ws.klippy.gcode_script("SET_HEATER_TEMPERATURE HEATER=heater_bed TARGET=0")
        else:
            return

    def pre1_clicked(self, widget):
        self._screen._ws.klippy.gcode_script(f"SET_HEATER_TEMPERATURE HEATER=extruder TARGET={self.presets_active[0]}")

    def pre2_clicked(self, widget):
        self._screen._ws.klippy.gcode_script(f"SET_HEATER_TEMPERATURE HEATER=extruder TARGET={self.presets_active[1]}")

    def pre3_clicked(self, widget):
        self._screen._ws.klippy.gcode_script(f"SET_HEATER_TEMPERATURE HEATER=extruder TARGET={self.presets_active[2]}")

    def pre4_clicked(self, widget):
        self._screen._ws.klippy.gcode_script(f"SET_HEATER_TEMPERATURE HEATER=extruder TARGET={self.presets_active[3]}")


    def update_panels(self):
        ext_temp = self._printer.get_dev_stat("extruder", "temperature")
        ext_target = self._printer.get_dev_stat("extruder", "target")
        ext_label = f"{int(ext_temp)} / {int(ext_target)}°C"

        if ext_target > 0:
            self.ext_temp.get_style_context().remove_class("main_temp_off")
            self.ext_temp.get_style_context().add_class("main_temp_on")
        else:
            self.ext_temp.get_style_context().remove_class("main_temp_on")
            self.ext_temp.get_style_context().add_class("main_temp_off")

        self.ext_temp.set_label(ext_label)
        self.right_button.set_label(self.right_button_mode)

        self.pre1.set_label(f"PLA, PVA, PVB = {self.presets_active[0]}°C")
        self.pre2.set_label(f"TPU, Flexibles = {self.presets_active[1]}°C")
        self.pre3.set_label(f"ABS, PETg, ASA = {self.presets_active[2]}°C")
        self.pre4.set_label(f"Nylon, PC = {self.presets_active[3]}°C")

        self.load.set_sensitive(self.load_unload_enabled)
        self.unload.set_sensitive(self.load_unload_enabled)


    def process_update(self, action, data):
        if action != "notify_status_update":
            return
        if self._printer.state == "printing":
            self.presets_active = self.presets_high
            self.right_button_mode = "Pause"
            self.load_unload_enabled = False
        elif self._printer.state == "paused":
            self.presets_active = self.presets_high
            self.right_button_mode = "Resume"
            self.load_unload_enabled = True
        else:
            self.presets_active = self.presets_low
            self.right_button_mode = "Cooldown"
            self.load_unload_enabled = True
        self.update_panels()
        self.update_filament_sensors(data)


# The code below was copy and pasted from extruder.py, just added the "limit=4"

    def create_sensor_panel(self):
        limit = 4
        filament_sensors = self._printer.get_filament_sensors()
        sensors = Gtk.Grid(valign=Gtk.Align.CENTER, row_spacing=5, column_spacing=5)
        if len(filament_sensors) > 0:
            for s, x in enumerate(filament_sensors):
                if s > limit:
                    break
                name = x[23:].strip()
                self.labels[x] = {
                    'label': Gtk.Label(label=self.prettify(name), hexpand=True, halign=Gtk.Align.CENTER,
                                       ellipsize=Pango.EllipsizeMode.END),
                    'switch': Gtk.Switch(width_request=round(self._gtk.font_size * 2),
                                         height_request=round(self._gtk.font_size)),
                    'box': Gtk.Box()
                }
                self.labels[x]['switch'].connect("notify::active", self.enable_disable_fs, name, x)
                self.labels[x]['box'].pack_start(self.labels[x]['label'], True, True, 10)
                self.labels[x]['box'].pack_start(self.labels[x]['switch'], False, False, 0)
                self.labels[x]['box'].get_style_context().add_class("filament_sensor")
                sensors.attach(self.labels[x]['box'], s, 0, 1, 1)
        return sensors

    def enable_disable_fs(self, switch, gparams, name, x):
        if switch.get_active():
            self._printer.set_dev_stat(x, "enabled", True)
            self._screen._ws.klippy.gcode_script(f"SET_FILAMENT_SENSOR SENSOR={name} ENABLE=1")
            if self._printer.get_stat(x, "filament_detected"):
                self.labels[x]['box'].get_style_context().add_class("filament_sensor_detected")
            else:
                self.labels[x]['box'].get_style_context().add_class("filament_sensor_empty")
        else:
            self._printer.set_dev_stat(x, "enabled", False)
            self._screen._ws.klippy.gcode_script(f"SET_FILAMENT_SENSOR SENSOR={name} ENABLE=0")
            self.labels[x]['box'].get_style_context().remove_class("filament_sensor_empty")
            self.labels[x]['box'].get_style_context().remove_class("filament_sensor_detected")

    def update_filament_sensors(self, data):
        for x in self._printer.get_filament_sensors():
            if x in data:
                if 'enabled' in data[x]:
                    self._printer.set_dev_stat(x, "enabled", data[x]['enabled'])
                    self.labels[x]['switch'].set_active(data[x]['enabled'])
                if 'filament_detected' in data[x]:
                    self._printer.set_dev_stat(x, "filament_detected", data[x]['filament_detected'])
                    if self._printer.get_stat(x, "enabled"):
                        if data[x]['filament_detected']:
                            self.labels[x]['box'].get_style_context().remove_class("filament_sensor_empty")
                            self.labels[x]['box'].get_style_context().add_class("filament_sensor_detected")
                        else:
                            self.labels[x]['box'].get_style_context().remove_class("filament_sensor_detected")
                            self.labels[x]['box'].get_style_context().add_class("filament_sensor_empty")
