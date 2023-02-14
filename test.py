from kivy.lang import Builder
from kivy.app import App
from kivymd.app import MDApp

class MyApp(MDApp):
    def build(self):
        self.title = 'Home Page'
        self.theme_cls.theme_style = 'Dark'
        self.theme_cls.primary_palette = 'Teal'

if __name__ == '__main__':
    MyApp().run()