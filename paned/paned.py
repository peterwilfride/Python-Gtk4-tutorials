import gi

gi.require_version(namespace='Gtk', version='4.0')
gi.require_version(namespace='Adw', version='1')

from gi.repository import Adw, Gio, Gtk

Adw.init()

class ExampleWindow(Gtk.ApplicationWindow):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.set_title(title='Python e GTK 4: PyGObject Gtk.Application()')
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

        hbox = Gtk.Box.new(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        hbox.set_homogeneous(True)
        hbox.set_margin_top(margin=0)
        hbox.set_margin_end(margin=0)
        hbox.set_margin_bottom(margin=0)
        hbox.set_margin_start(margin=0)
        self.set_child(child=hbox)

        # cria o paned e define a posição da barra
        self.paned = Gtk.Paned()
        self.paned.set_position(200)
        hbox.append(child=self.paned)

        # cria a sidebar, é uma box 
        self.sidebar = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.sidebar.set_size_request(200, -1)
        self.sidebar.set_vexpand(True)
        self.paned.set_start_child(self.sidebar)

        # cria a main area, é uma boz
        self.main_area = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.main_area.set_homogeneous(True)
        self.main_area.set_vexpand(True)
        self.paned.set_end_child(self.main_area)

        ## adding to sidebar
        label1 = Gtk.Label.new()
        label1.set_text(str='Sidebar')
        label1.set_valign(Gtk.Align.CENTER)

        label2 = Gtk.Label.new()
        label2.set_text(str='Mais opções')
        label2.set_valign(Gtk.Align.CENTER)

        self.sidebar.append(child=label1)
        self.sidebar.append(child=label2)

        ## adding to main área
        label3 = Gtk.Label.new()
        label3.set_text(str='Área principal')
        label3.set_halign(Gtk.Align.CENTER)

        self.main_area.append(child=label3)

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