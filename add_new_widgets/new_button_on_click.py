import gi

gi.require_version(namespace='Gtk', version='4.0')
gi.require_version(namespace='Adw', version='1')

from gi.repository import Adw, Gio, Gtk

Adw.init()

class ExampleWindow(Gtk.ApplicationWindow):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.set_title(title='Add new button')
        self.set_default_size(width=int(1366 / 2), height=int(768 / 2))
        self.set_size_request(width=int(1366 / 2), height=int(768 / 2))

        self.index = 0
        self.all_listbox_childrens = []
        self.selected_list = []

        headerbar = Gtk.HeaderBar.new()
        self.set_titlebar(titlebar=headerbar)

        menu_button_model = Gio.Menu()
        menu_button_model.append('Preferências', 'app.preferences')

        menu_button = Gtk.MenuButton.new()
        menu_button.set_icon_name(icon_name='open-menu-symbolic')
        menu_button.set_menu_model(menu_model=menu_button_model)
        headerbar.pack_end(child=menu_button)

        # toggle selection mode
        selecion_mode_button = Gtk.Button.new()
        selecion_mode_button.set_icon_name(icon_name="document-open-recent-symbolic")
        selecion_mode_button.connect("clicked", self.toggle_selecion_mode)
        headerbar.pack_end(child=selecion_mode_button)

        # Vertical Box to add everything
        vbox = Gtk.Box.new(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        vbox.set_margin_top(margin=12)
        vbox.set_margin_end(margin=12)
        vbox.set_margin_bottom(margin=12)
        vbox.set_margin_start(margin=12)
        self.set_child(child=vbox)

        # Horizontal Box to add control buttons
        hbox = Gtk.Box.new(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        hbox.set_homogeneous(True)
        vbox.append(child=hbox)

        # add button
        self.add_button = Gtk.Button.new()
        self.add_button.set_icon_name(icon_name='list-add-symbolic')
        self.add_button.get_style_context().add_class(class_name='suggested-action')
        self.add_button.get_style_context().add_class(class_name='circular')
        self.add_button.set_halign(Gtk.Align.END)
        self.add_button.set_size_request(50, 50)
        self.add_button.connect("clicked", self.add_button_to_list)
        self.add_button.set_visible(True)
        hbox.append(self.add_button)

        # remove button
        self.rm_button = Gtk.Button.new()
        self.rm_button.set_icon_name(icon_name='list-remove-symbolic')
        self.rm_button.get_style_context().add_class(class_name='destructive-action')
        self.rm_button.get_style_context().add_class(class_name='circular')
        self.rm_button.set_halign(Gtk.Align.END)
        self.rm_button.connect("clicked", self.remove_rows_on_listbox)
        self.rm_button.set_size_request(50, 50)
        self.rm_button.set_visible(False)
        hbox.append(self.rm_button)

        self.listbox = Gtk.ListBox.new()
        vbox.append(self.listbox)

    def add_button_to_list(self, widget):
        # box horizontal para guardar os widgets de cada row
        hbox = Gtk.Box.new(orientation=Gtk.Orientation.HORIZONTAL, spacing=2)
        # add checkbutton in selection mode end in hide mode
        checkbutton = Gtk.CheckButton.new()
        checkbutton.get_style_context().add_class(class_name='selection-mode')
        checkbutton.set_visible(False)
        checkbutton.connect("toggled", self.on_toggle_checkbutton)
        # add a button
        new_button = Gtk.Button.new()
        new_button.set_hexpand(True)
        new_button.set_label(f"Button {self.index}")
        new_button.get_style_context().add_class(class_name='flat')
        # add to box
        hbox.append(checkbutton)
        hbox.append(new_button)
        ## add to listbox
        self.listbox.append(hbox)
        # increment the index
        self.index = self.index + 1
        # add child to list
        self.all_listbox_childrens.append(checkbutton)

    def on_toggle_checkbutton(self, widget):
        # Widget -> Box => ListBoxRow
        # tenho que apagar o widget ListBoxRow
        row = widget.get_parent().get_parent()

        if widget.get_active():
            self.selected_list.append(row)
        else:
            self.selected_list.remove(row)

    def remove_rows_on_listbox(self, widget):
        for obj in self.selected_list:
            self.listbox.remove(obj)
            self.all_listbox_childrens.remove(obj.get_child().get_first_child())
        
        self.selected_list.clear()
    
    def toggle_selecion_mode(self, widget):
        for obj in self.all_listbox_childrens:
            if obj.get_visible():
                obj.hide()
                self.add_button.show()
                self.rm_button.hide()
            else:
                obj.show()
                self.add_button.hide()
                self.rm_button.show()

class ExampleApplication(Adw.Application):

    def __init__(self):
        super().__init__(application_id='br.com.justcode.Example',
                         flags=Gio.ApplicationFlags.FLAGS_NONE)

        self.create_action('quit', self.exit_app, ['<primary>q'])
        self.create_action('preferences', self.on_preferences_action)

    def do_activate(self):
        win = self.props.active_window
        if not win:
            win = ExampleWindow(application=self)
        win.present()

    def do_startup(self):
        Gtk.Application.do_startup(self)

    def do_shutdown(self):
        Gtk.Application.do_shutdown(self)

    def on_preferences_action(self, action, param):
        print('Ação app.preferences foi ativa.')

    def exit_app(self, action, param):
        self.quit()

    def create_action(self, name, callback, shortcuts=None):
        action = Gio.SimpleAction.new(name, None)
        action.connect('activate', callback)
        self.add_action(action)
        if shortcuts:
            self.set_accels_for_action(f'app.{name}', shortcuts)


if __name__ == '__main__':
    import sys

    app = ExampleApplication()
    app.run(sys.argv)