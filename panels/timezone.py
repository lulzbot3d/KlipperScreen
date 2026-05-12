# ***********************************
# KlipperScreen Time Zone Menu
# By Carl Smith  2026 - FAME3D
# ***********************************


import logging
import subprocess
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from ks_includes.screen_panel import ScreenPanel
from ks_includes.widgets.autogrid import AutoGrid


class Panel(ScreenPanel):
    def __init__(self, screen, title):
        title = title or _("Time Zone")
        super().__init__(screen, title)

        self.current_timezone = self.get_current_timezone()
        self.timezone_label = Gtk.Label(label=f"Current Time Zone:  {self.current_timezone}")
        self.timezone_label.get_style_context().add_class("timezone_top")
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=50, margin=10)
        main_box.pack_start(self.timezone_label, False, False, 0)
        self.content.add(main_box)

        self.timezones = self.get_timezones()
        self.timezone_buttons = []

        for timezone in self.timezones:
            self.labels[timezone] = self._gtk.Button(label=timezone, style="buttons_main_top")
            self.labels[timezone].connect("clicked", self.on_timezone_clicked, timezone)
            self.timezone_buttons.append(self.labels[timezone])

        grid = AutoGrid(self.timezone_buttons, vertical=self._screen.vertical_mode, max_columns=2)
        scroll = self._gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scroll.add(grid)
        self.content.add(scroll)

    def get_timezones(self):
        result = subprocess.run(
            ["timedatectl", "list-timezones"],
            capture_output=True,
            text=True
        )
        return result.stdout.splitlines()

    def get_current_timezone(self):
        result = subprocess.run(
            ["timedatectl", "show", "--property=Timezone", "--value"],
            capture_output=True,
            text=True
        )
        return result.stdout.strip()

    def on_timezone_clicked(self, widget, timezone):

        dialog = Gtk.MessageDialog(
            transient_for=self._screen,
            flags=0,
            message_type=Gtk.MessageType.QUESTION,
            buttons=Gtk.ButtonsType.YES_NO,
            text="\nChange time zone?"
        )

        dialog.get_style_context().add_class("timezone_confirm")
        for child in dialog.get_action_area().get_children():
            if isinstance(child, Gtk.Button):
                child.get_style_context().add_class("timezone_confirm")
        dialog.format_secondary_text(f"Set time zone to:\n{timezone}")

        response = dialog.run()
        dialog.destroy()

        if response == Gtk.ResponseType.YES:
            self.set_timezone(timezone)

    def get_current_time(self):
        result = subprocess.run(
            ["timedatectl", "show", "--property=TimeUSec", "--value"],
            capture_output=True,
            text=True
        )
        return result.stdout.strip()

    def set_timezone(self, timezone):
        subprocess.run(["sudo", "timedatectl", "set-timezone", timezone])
        self.current_timezone = self.get_current_timezone()
        if self.current_timezone == timezone:
            time = self.get_current_time()
            self._screen.show_popup_message(f"Time zone changed to {timezone}\nTime is now: {time}", level=1)
        else:
            self._screen.show_popup_message(f"Failed to change time zone to {timezone}", level=3)
        self.timezone_label.set_text(f"Current Time Zone:  {self.current_timezone}")
        self.content.show_all()
