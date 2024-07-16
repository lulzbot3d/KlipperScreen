import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from ks_includes.screen_panel import ScreenPanel


COLORS = {
    "lulzbot": "#c1d82f",
    "text": "White",
}


class Panel(ScreenPanel):
    def __init__(self, screen, title):
        super().__init__(screen, title)
        
        image = self._gtk.Image("QSG-qr-code", self._gtk.content_width * .25, self._gtk.content_height * .5)

        self.tb = Gtk.TextBuffer(text="")
        tv = Gtk.TextView(editable=False, cursor_visible=False, wrap_mode=Gtk.WrapMode.WORD_CHAR)
        tv.set_buffer(self.tb)
        scroll = Gtk.ScrolledWindow(hexpand=False, vexpand=True)
        scroll.add(tv)

        info = Gtk.Box()
        info.pack_start(scroll, True, True, 8)
        info.pack_end(image, False, True, 8)

        self.content.add(info)

    def activate(self):
        self.tb.set_text("")
        self.tsize = 26
        self.color = COLORS["text"]
        self.add_line("\n")

        self.color = COLORS["lulzbot"]
        self.tsize = 42
        self.add_line("LulzBot Mini 3\n")
        
        self.color = COLORS["text"]
        self.tsize = 18
        self.add_line("\n")
        self.add_line("LulzBot\n")
        self.add_line("1001 25th St N\n")
        self.add_line("Fargo, ND 58102\n")
        self.add_line("USA\n")
        self.add_line("\n")
        self.add_line("Email: support@lulzbot.com\n")
        self.add_line("Phone: +1-701-809-0800 ext 2\n")
        self.add_line("\n\n")

    def add_line(self, txt):
        self.tb.insert_markup(
            self.tb.get_end_iter(),
            f'<span font="{self.tsize}" color="{self.color}">{txt}</span>',
            -1
        )
