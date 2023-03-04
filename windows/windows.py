import gi

gi.require_version(namespace='Gtk', version='4.0')
gi.require_version(namespace='Adw', version='1')

from gi.repository import Adw, Gio, Gtk

Adw.init()

class ExampleWindow(Gtk.ApplicationWindow):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.set_title(title='Janela antiga')
        self.set_default_size(width=200, height=200)
        self.set_size_request(width=200, height=200)

        self.value = 80

        headerbar = Gtk.HeaderBar.new()
        self.set_titlebar(titlebar=headerbar)

        menu_button_model = Gio.Menu()
        menu_button_model.append('Preferências', 'app.preferences')

        menu_button = Gtk.MenuButton.new()
        menu_button.set_icon_name(icon_name='open-menu-symbolic')
        menu_button.set_menu_model(menu_model=menu_button_model)
        headerbar.pack_end(child=menu_button)

        vbox = Gtk.Box.new(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        vbox.set_margin_top(margin=12)
        vbox.set_margin_end(margin=12)
        vbox.set_margin_bottom(margin=12)
        vbox.set_margin_start(margin=12)
        self.set_child(child=vbox)

        label = Gtk.Label.new(str=f'Current value: {self.value}')
        vbox.append(label)

        button = Gtk.Button()
        button.set_label("Hide current and open new window")
        button.connect('clicked', self.hide_current_and_open_new_window)
        vbox.append(button)

        button2 = Gtk.Button()
        button2.set_label("Open new window")
        button2.connect('clicked', self.open_new_window)
        vbox.append(button2)
    
    def open_new_window(self, widget):
        window = NewWindow2()
        window.show()
    
    def hide_current_and_open_new_window(self, widget):
        window = NewWindow()
        window.show()
        self.set_hide_on_close(True)
        self.close()

class NewWindow2(Gtk.ApplicationWindow):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.set_transient_for(ExampleWindow())
        self.parent = self.get_transient_for()
        
        self.value = self.parent.value

        #self.set_modal(modal=True)
        self.set_title(title='Janela nova')
        self.set_default_size(width=400, height=200)
        self.set_size_request(width=400, height=200)

        vbox = Gtk.Box.new(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        vbox.set_margin_top(margin=12)
        vbox.set_margin_end(margin=12)
        vbox.set_margin_bottom(margin=12)
        vbox.set_margin_start(margin=12)
        vbox.set_valign(Gtk.Align.CENTER)
        self.set_child(child=vbox)

        label = Gtk.Label.new(str="Previous window is opened")
        vbox.append(label)

        label2 = Gtk.Label.new(str=f"Value inherit from old window : {self.value}")
        vbox.append(label2)

        button = Gtk.Button.new_with_label('Close current window')
        button.connect('clicked', self.on_window_button_close_clicked)
        vbox.append(child=button)

        # exibe a janela
        self.show()

    def on_window_button_close_clicked(self, widget):
        self.destroy()

class NewWindow(Gtk.ApplicationWindow):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.set_transient_for(ExampleWindow())
        self.parent = self.get_transient_for()
        
        self.value = self.parent.value

        #self.set_modal(modal=True)
        self.set_title(title='Janela nova')
        self.set_default_size(width=400, height=200)
        self.set_size_request(width=400, height=200)

        vbox = Gtk.Box.new(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        vbox.set_margin_top(margin=12)
        vbox.set_margin_end(margin=12)
        vbox.set_margin_bottom(margin=12)
        vbox.set_margin_start(margin=12)
        vbox.set_valign(Gtk.Align.CENTER)
        self.set_child(child=vbox)

        label = Gtk.Label.new(str="Previous window is hide")
        vbox.append(label)

        label2 = Gtk.Label.new(str=f"Value inherit from old window : {self.value}")
        vbox.append(label2)

        button = Gtk.Button.new_with_label('Close current window')
        button.connect('clicked', self.on_window_button_close_clicked)
        vbox.append(child=button)

        # exibe a janela
        self.show()

    def on_window_button_close_clicked(self, widget):
        self.destroy()
        self.parent.set_hide_on_close(False)
        self.parent.show()

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