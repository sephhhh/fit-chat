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
from functools import partial

Window.size = (350, 700)


class ImageButton(ButtonBehavior, Image):
    pass


class MainScreenManager(ScreenManager):
    pass


class MyApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = 'Light'
        Builder.load_file('main.kv')
        return MainScreenManager()

    def initializeProfile(self):  # function to initialize profile after successful login
        accInfo = firebase.get('https://fitchat-d7a73-default-rtdb.firebaseio.com/Users', '')
        name = accInfo[accountKey]['name']
        self.root.ids.name.text = name

        bioText = accInfo[accountKey]["bio"]
        self.root.ids.biography.text = bioText

        profile = accInfo[accountKey]['profilePicture']
        self.root.ids.profile_picture.source = profile

        sport = accInfo[accountKey]['sportSelection']
        self.root.ids.sport_selectcion.source = sport

    def loginScreen(self):
        self.root.current = "createAccount"

    def get_data(self):  # function for submit button
        email = self.root.ids.email.text
        password = self.root.ids.password.text
        print(email)
        try:  # get database data
            accInfo = firebase.get('https://fitchat-d7a73-default-rtdb.firebaseio.com/Users', '')
            for loginInfo in accInfo.keys():
                if accInfo[loginInfo]['email'] == email:
                    if accInfo[loginInfo]['password'] == password:
                        print("Login Successful")
                        self.root.ids.login_message.text = "Successful Login"
                        self.root.current = "homepage"
                        # initialize profile information function
                        global accountKey
                        accountKey = loginInfo
                        self.initializeProfile()
                else:
                    print("Invalid Password")
                    self.root.ids.login_message.text = "Invalid Password"
        except:
            pass

    def createAccount(self):
        email = self.root.ids.newEmail.text
        password = self.root.ids.newPassword.text
        bio = self.root.ids.newBio.text
        name = self.root.ids.newName.text
        data = {
            'email': email,
            'password': password,
            'profilePicture': 'fitChatAvatars/defaultAvatar.png',
            'bio': bio,
            'name': name,
        }
        firebase.post('https://fitchat-d7a73-default-rtdb.firebaseio.com/Users', data)
        self.root.current = 'login'

    def change_data(self):
        email = self.root.ids.email.text
        password = self.root.ids.password.text
        change_bio = self.root.ids.change_bio.text
        name = self.root.ids.change_name.text
        sport = self.root.ids.sports_label.text
        accountLink = 'https://fitchat-d7a73-default-rtdb.firebaseio.com/Users/' + accountKey
        accInfo = firebase.get('https://fitchat-d7a73-default-rtdb.firebaseio.com/Users', '')

        data = {
            'email': email,
            'password': password,
            'profilePicture': accInfo[accountKey]['profilePicture'],
            'bio': change_bio,
            'name': name,
        }
        firebase.patch(accountLink, data)
        self.root.current = 'login'

    def changeSports(self):
        sport = self.root.ids.sports_label.text
        accountLink = 'https://fitchat-d7a73-default-rtdb.firebaseio.com/Users/' + accountKey
        data = {
            'sports': sport
        }
        firebase.patch(accountLink, data)
        self.root.current = 'login'

    def change_avatar(self):
        self.root.current = 'change_avatar'
        avatar_grid = self.root.ids.avatar_grid
        for root_dir, folders, files in walk("fitChatAvatars"):
            for f in files:
                if f != '.DS_Store':  # for mac folders
                    img = ImageButton(source="fitChatAvatars/" + f, on_release=partial(self.change_avatar_pic, f))
                    avatar_grid.add_widget(img)

    def change_avatar_pic(self, image, widget_id):
        self.root.ids.profile_picture.source = "fitChatAvatars/" + image

        # firebase
        email = self.root.ids.email.text
        password = self.root.ids.password.text
        bio = self.root.ids.biography.text
        name = self.root.ids.name.text
        profilePicture = "fitChatAvatars/" + image

        data = {
            'email': email,
            'password': password,
            'profilePicture': profilePicture,
            'bio': bio,
            'name': name,
        }

        accountLink = 'https://fitchat-d7a73-default-rtdb.firebaseio.com/Users/' + accountKey
        firebase.patch(accountLink, data)
        # return back
        self.root.ids.change_text.text = "Avatar Successfully Changed"
        self.root.current = 'homepage'

    global firebase
    firebase = firebase.FirebaseApplication('https://fitchat-d7a73-default-rtdb.firebaseio.com/', None)
    global accountKey

    def get_hist(self):
        messages = firebase.get('/Chat', "")
        newMessages = ""
        for i in messages.keys():
            newMessages = newMessages + "\n" + (messages[i]["Email"]) + ' said: ' + (messages[i]["Message"])
        self.root.ids.Chat.text = newMessages

    def send_data(self):
        email = self.root.ids.email.text
        data = {'Message': '',
                'Email': email}
        message = self.root.ids.message.text
        data['Message'] = message
        firebase.post('https://fitchat-d7a73-default-rtdb.firebaseio.com/Chat', data)
        self.root.ids.Chat.text += "\n" + email + ' said: ' + message

    cred = credentials.Certificate('fitchat-d7a73-firebase-adminsdk-ybqmf-e4babd672a.json')
    firebase_admin.initialize_app(cred)
    checks = []

    def check(self, instance, value, sport):
        if value == True:
            MyApp.checks.append(sport)
            sports = ""
            for i in MyApp.checks:
                sports = f"{sports} {i}"
            self.root.ids.sports_label.text = f"{sports}"
        else:
            MyApp.checks.remove(sport)
            sports = ""
            for i in MyApp.checks:
                sports = f"{sports} {i}"
            self.root.ids.sports_label.text = f"{sports}"


if __name__ == '__main__':
    MyApp().run()
