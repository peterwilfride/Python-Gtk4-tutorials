import gi

gi.require_version(namespace='Gtk', version='4.0')
gi.require_version(namespace='Adw', version='1')

from gi.repository import Adw, Gio, Gtk, Gdk

Adw.init()

class ExampleWindow(Gtk.ApplicationWindow):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.set_title(title='Types of buttons')
        self.set_default_size(width=int(1366 / 2), height=int(768 / 2))
        self.set_size_request(width=int(1366 / 2), height=int(768 / 2))

        headerbar = Gtk.HeaderBar.new()
        self.set_titlebar(titlebar=headerbar)

        menu_button_model = Gio.Menu()
        menu_button_model.append('Preferências', 'app.preferences')

        menu_button = Gtk.MenuButton.new()
        menu_button.set_icon_name(icon_name='open-menu-symbolic')
        menu_button.set_menu_model(menu_model=menu_button_model)
        headerbar.pack_end(child=menu_button)

        vbox = Gtk.Box.new(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        vbox.set_homogeneous(True)
        vbox.set_margin_top(margin=12)
        vbox.set_margin_end(margin=12)
        vbox.set_margin_bottom(margin=12)
        vbox.set_margin_start(margin=12)
        self.set_child(child=vbox)

        hbox1 = Gtk.Box.new(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        hbox1.set_homogeneous(homogeneous=True)
        vbox.append(child=hbox1)

        hbox2 = Gtk.Box.new(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        hbox2.set_homogeneous(homogeneous=True)
        vbox.append(child=hbox2)

        button1 = Gtk.Button.new()
        button1.set_icon_name(icon_name='list-remove-symbolic')
        button1.get_style_context().add_class(class_name='destructive-action')

        button2 = Gtk.Button.new()
        button2.set_icon_name(icon_name='list-add-symbolic')
        button2.get_style_context().add_class(class_name='suggested-action')

        button3 = Gtk.Button.new()
        button3.set_icon_name(icon_name='list-add-symbolic')
        button3.get_style_context().add_class(class_name='flat')

        hbox1.append(button1)
        hbox1.append(button2)
        hbox1.append(button3)

        # Circular buttons
        button4 = Gtk.Button.new()
        button4.set_icon_name(icon_name='list-remove-symbolic')
        button4.get_style_context().add_class(class_name='destructive-action')
        button4.get_style_context().add_class(class_name='circular')

        button5 = Gtk.Button.new()
        button5.set_icon_name(icon_name='list-add-symbolic')
        button5.get_style_context().add_class(class_name='suggested-action')
        button5.get_style_context().add_class(class_name='circular')

        button6 = Gtk.Button.new()
        button6.set_icon_name(icon_name='list-add-symbolic')
        button6.get_style_context().add_class(class_name='flat')
        button6.get_style_context().add_class(class_name='circular')

        hbox2.append(button4)
        hbox2.append(button5)
        hbox2.append(button6)

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