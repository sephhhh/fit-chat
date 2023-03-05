from kivy.lang import Builder
from kivy.app import App
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from firebase_admin import db
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase import firebase

Window.size = (350, 700)

class MyApp(MDApp):
    global firebase
    firebase = firebase.FirebaseApplication('https://fitchat-d7a73-default-rtdb.firebaseio.com//', None)
    #get information from firestore database

    def build(self):
        self.title = 'Home Page'
        self.theme_cls.theme_style = 'Dark'
        return Builder.load_file('test.kv')

if __name__ == '__main__':
    MyApp().run()
