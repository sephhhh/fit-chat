from kivy.lang import Builder
from kivy.app import App
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from firebase import firebase
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import json
from os import walk
from kivy.uix.button import ButtonBehavior
from kivy.uix.image import Image
from kivy.properties import StringProperty
from functools import partial


Window.size = (350, 700)


class ImageButton(ButtonBehavior, Image):
    pass


class MainScreenManager(ScreenManager):
    pass


class MyApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = 'Light'
        Builder.load_file('testing2.kv')
        return MainScreenManager()


    cred = credentials.Certificate('fitchat-d7a73-firebase-adminsdk-ybqmf-e4babd672a.json')
    firebase_admin.initialize_app(cred)

    global firestore
    firestore = firestore.client()

    def initializeProfile(self): #function to initialize profile after successful login
        name = y["name"]
        self.root.ids.name.text = name

        bioText = y["bio"]
        self.root.ids.biography.text = bioText

        profile = y['profilePicture']
        self.root.ids.profile_picture.source = profile

        pass

    def get_data(self):  # function for submit button
        email = self.root.ids.email.text
        password = self.root.ids.password.text
        print(email)
        try:  # get database data
            doc_ref = firestore.collection("user_login").document(email)
            doc = doc_ref.get()
            global y
            y = json.loads(json.dumps(doc.to_dict()))
            print(y["password"])
            if str(doc_ref.id) == email and (password == y["password"]):
                print("Login Successful")
                self.root.ids.login_message.text = "Successful Login"
                self.root.current = "homepage"
                # initialize profile information function
                self.initializeProfile()
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
                'profilePicture': "fitChatAvatars/defaultAvatar.png",
                'bio': '"No Biography Written"',
                'name': "No Name Set",
            })
            self.root.ids.login_message.text = "Account Created"
            #self.initializeProfile()

    def change_data(self):
        email = self.root.ids.email.text
        password = self.root.ids.password.text
        change_bio = self.root.ids.change_bio.text
        name = self.root.ids.change_name.text
        doc_ref = firestore.collection("user_login").document(email)
        doc_ref.set({
            'email': email,
            'password': password,
            'profilePicture': "fitChatAvatars/defaultAvatar.png",
            'bio': change_bio,
            'name': name,
        })
        self.root.current = 'login'

    def change_avatar(self):
        self.root.current = 'change_avatar'
        avatar_grid = self.root.ids.avatar_grid
        for root_dir, folders, files in walk("fitChatAvatars"):
            for f in files:
                img = ImageButton(source="fitChatAvatars/" + f, on_release=partial(self.change_avatar_pic, f))
                avatar_grid.add_widget(img)
    def change_avatar_pic(self, image, widget_id):
        self.root.ids.profile_picture.source = "fitChatAvatars/" + image

        #firebase
        email = self.root.ids.email.text
        password = self.root.ids.password.text
        bio = self.root.ids.biography.text
        name = self.root.ids.name.text
        profilePicture = "fitChatAvatars/" + image
        doc_ref = firestore.collection("user_login").document(email)
        doc_ref.set({
            'email': email,
            'password': password,
            'profilePicture': profilePicture,
            'bio': bio,
            'name': name,
        })

        #return back
        self.root.ids.change_text.text = "Avatar Successfully Changed"
        self.root.current = 'homepage'

if __name__ == '__main__':
    MyApp().run()
