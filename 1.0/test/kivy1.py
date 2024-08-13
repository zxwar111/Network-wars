from Kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup

class MenuExampleApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')

        open_button = Button(text='Open')
        open_button.bind(on_release=self.on_open)
        layout.add_widget(open_button)

        save_button = Button(text='Save')
        save_button.bind(on_release=self.on_save)
        layout.add_widget(save_button)

        exit_button = Button(text='Exit')
        exit_button.bind(on_release=self.on_exit)
        layout.add_widget(exit_button)

        return layout

    def on_open(self, instance):
        self.show_popup('Open clicked')

    def on_save(self, instance):
        self.show_popup('Save clicked')

    def on_exit(self, instance):
        App.get_running_app().stop()

    def show_popup(self, message):
        popup = Popup(title='Menu',
                      content=Label(text=message),
                      size_hint=(None, None), size=(200, 200))
        popup.open()

if __name__ == '__main__':
    MenuExampleApp().run()
