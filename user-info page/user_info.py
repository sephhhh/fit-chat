from kivy.lang import Builder
from kivy.app import App
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from firebase import firebase
from kivymd.uix.textfield import MDTextField
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivymd.uix.button import MDRectangleFlatButton

Window.size = (350, 650)
firebase = firebase.FirebaseApplication('https://fitchat-d7a73-default-rtdb.firebaseio.com/', None)

data = {'Name' : name,
        'Biography' : biography}

firebase.post('')

class testApp(MDApp):
    def build(self):
        return Builder.load_file('testApp.kv')

    def get_data(self):
        name = self.root.ids.name.text
        biography = self.root.ids.bio.text
        print(name)
        print(biography)

if __name__ == '__main__':
    testApp().run()
