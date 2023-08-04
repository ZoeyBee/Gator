import gi; gi.require_version('Gtk', '3.0'); from gi.repository import Gtk

from frontend.widgets.button import Button


class BaseModule:
    module_name = ''
    collapsed = False
    collapsed_modules = 0
    total_modules = 0

    def setup_ui(self):
        BaseModule.total_modules += 1
        if self.collapsed: BaseModule.collapsed_modules += 1
        self.icons = {
            'iconArrowDown': self.manager.icon('iconArrowDown', 25, 25),
            'iconArrowUp':   self.manager.icon('iconArrowUp',   25, 25),
        }

        self.set_name('module')
        self.header_box = Gtk.Box(orientation='horizontal', spacing=0); self.pack_start(self.header_box, False, False, 0)

        self.collapse_button = Button(None, self.on_toggle_collapse_button_pressed, image=self.icons['iconArrowDown'])
        self.header_box.pack_start(self.collapse_button, False, False, 0)
        self.collapse_button.set_name('hideBackground')

        self.name_label = Gtk.Label(); self.name_label.set_text(self.module_name)
        self.name_label.set_name('moduleNameLabel')
        self.header_box.pack_start(self.name_label, True, False, 0)

        self.scroll_area = Gtk.ScrolledWindow()
        self.scroll_area.set_vexpand(True); self.scroll_area.set_hexpand(True)
        self.scroll_area.set_name('ModuleScrollArea')
        self.pack_start(self.scroll_area, True, True, 0)

        self.box = Gtk.Box(orientation='horizontal'); self.scroll_area.add(self.box)
        self.add_button = Button(None, self.on_add_button_pressed, image=self.manager.icon('iconPlus', 40, 40))
        self.box.pack_start(self.add_button, False, False, 0)

    def on_toggle_collapse_button_pressed(self, *args):
        if self.collapsed:
            self.collapsed = False
            BaseModule.collapsed_modules -= 1
            self.collapse_button.set_image(self.icons['iconArrowDown'])
        elif BaseModule.collapsed_modules != BaseModule.total_modules - 1:
            self.collapsed = True
            BaseModule.collapsed_modules += 1
            self.collapse_button.set_image(self.icons['iconArrowUp'])
        self.scroll_area.set_visible(not self.collapsed)

    def on_add_button_pressed(self, *args): pass
