from kivy.lang import Builder
from kivy.app import App
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window

Window.size = (350, 700)

class MyApp(MDApp):
    def build(self):
        self.title = 'Home Page'
        self.theme_cls.theme_style = 'Dark'
        self.theme_cls.primary_palette = 'Teal'
        return Builder.load_file('my.kv')

if __name__ == '__main__':
    MyApp().run()
