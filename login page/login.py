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
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import json

Window.size = (350, 650)


class testApp(MDApp):
    def build(self):
        return Builder.load_file('logintest.kv')

    global doc_ref

    cred = credentials.Certificate('fitchat-d7a73-firebase-adminsdk-ybqmf-e4babd672a.json')
    firebase_admin.initialize_app(cred)

    global firestore
    firestore = firestore.client()

    def get_data(self):  # function for submit button
        email = self.root.ids.email.text
        password = self.root.ids.password.text
        try: #get database data
            doc_ref = firestore.collection("user_login").document(email)
            doc = doc_ref.get()
            y = json.loads(json.dumps(doc.to_dict()))
            print(y["password"])
            if str(doc_ref.id) == email and (password == y["password"]):
                print("Login Successful")
                self.root.ids.login_message.text = "Successful Login"
                #move screen function
            else:
                print("Invalid Password")
                self.root.ids.login_message.text = "Invalid Password"
        except:
            print(email)
            print(password)
            doc_ref = firestore.collection("user_login").document(email)
            doc_ref.set({
                    'email': email,
                    'password': password,
            })
            self.root.ids.login_message.text = "Account Created"

if __name__ == '__main__':
    testApp().run()
