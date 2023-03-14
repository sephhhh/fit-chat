from kivy.lang import Builder
from kivy.app import App
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.label import MDLabel
from kivy.core.window import Window
from firebase import firebase
from kivymd.uix.textfield import MDTextField
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivymd.uix.button import MDRectangleFlatButton
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import json

Window.size = (350, 650)

class main(MDApp):
    def build(self):
        return Builder.load_file('main.kv')
        

    global firebase
    firebase = firebase.FirebaseApplication('https://fitchat-d7a73-default-rtdb.firebaseio.com/Chat', None)

    def get_hist(self):
        messages = firebase.get('/Chat', "")
        newMessages = ""
        for i in messages.keys():
            newMessages = newMessages + '\nYou said: ' + (messages[i]["Message"])
        self.root.ids.Chat.text = newMessages

    def send_data(self):
        data = {'Message': ''}
        message = self.root.ids.message.text
        data['Message'] = message
        firebase.post('https://fitchat-d7a73-default-rtdb.firebaseio.com/Chat', data)
        self.root.ids.Chat.text += '\nYou said: ' + message

if __name__ == '__main__':
    main().run()
