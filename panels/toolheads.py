import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib
from ks_includes.screen_panel import ScreenPanel


class Panel(ScreenPanel):
    def __init__(self, screen, title):
        super().__init__(screen, title)

        # Buttons for tool selection
        self.current_tool = None
        self.buttons = {}
        self.button_values = {
            'MET175': 'MET175',
            'MET285': 'MET285',
            'Park Tool Head': 'Park_Nozzle'
        }
        self.content_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)

        self.buttons['MET175'] = self._gtk.Button(None, "MET175", "buttons_toolheads")
        self.buttons['MET285'] = self._gtk.Button(None, "MET285", "buttons_toolheads")
        self.buttons['Park Tool Head'] = self._gtk.Button(None, "Park Tool Head", "buttons_toolheads")

        self.buttons['MET175'].connect("clicked", self.select_tool, self.button_values['MET175'])
        self.buttons['MET285'].connect("clicked", self.select_tool, self.button_values['MET285'])
        self.buttons['Park Tool Head'].connect("clicked", self.select_tool, self.button_values['Park Tool Head'])

        for b in ('MET175', 'MET285', 'Park Tool Head'):
            btn = self.buttons[b]
            btn.set_hexpand(True)
            btn.set_vexpand(True)
            self.content_box.pack_start(btn, True, True, 0)

        self.content.add(self.content_box)

    def activate(self):
        if self._printer is not None and self._printer.data:
            self.process_update("notify_status_update", self._printer.data)
        if self._screen.restApi is not None:
            GLib.idle_add(self.query_save_variables)

    def query_save_variables(self):
        data = self._screen.restApi.send_request("printer/objects/query?save_variables")
        if data and 'result' in data and 'status' in data['result']:
            self.process_update("notify_status_update", data['result']['status'])
        return False

    def select_tool(self, widget, name):
        self._screen._send_action(widget, "printer.gcode.script", {"script": name})

        if name in ("MET175", "MET285"):
            self.update_selection(name)

        if self._screen.restApi is not None:
            GLib.timeout_add_seconds(1, self.query_save_variables)

    def process_update(self, action, data):
        if action == "notify_status_update":
            value = self.find_current_extruder(data)
            if value is not None:
                self.update_selection(str(value))

    def find_current_extruder(self, data):
        return data.get('save_variables', {}).get('variables', {}).get('currentextruder')

    def update_selection(self, current):
        self.current_tool = current
        for name, btn in self.buttons.items():
            value = self.button_values.get(name, name)
            if value == current:
                btn.get_style_context().add_class('button_toolhead_selected')
                btn.set_label(f"{name} (Selected)")
            else:
                btn.get_style_context().remove_class('button_toolhead_selected')
                btn.set_label(name)
