from kivy.lang import Builder
from kivy.app import App
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from firebase import firebase
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from os import walk
import time
from kivy.uix.button import ButtonBehavior, Button
from kivy.uix.image import Image
from functools import partial
import webbrowser

from kivymd.uix.button import MDRectangleFlatButton

Window.size = (350, 700)


class ImageButton(ButtonBehavior, Image):
    pass


class MainScreenManager(ScreenManager):
    pass


class MyApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = 'Light'
        Builder.load_file('fitchat.kv')
        return MainScreenManager()

    def capture(self):
        '''
        Function to capture the images and give them the names
        according to their captured time and date.
        '''
        camera = self.root.ids.camera
        timestr = time.strftime("%Y%m%d_%H%M%S")
        camera.export_to_png("fitChatAvatars/IMG_{}.png".format(timestr))
        print("Captured")
        self.root.ids.camera.play = not camera.play
        self.root.current = 'homepage'

    def cameraScreen(self):
        self.root.current = 'camera'

    def initializeProfile(self):  # function to initialize profile after successful login
        self.root.ids.camera.play = False
        accInfo = firebase.get('https://fitchat-d7a73-default-rtdb.firebaseio.com/Users', '')
        name = accInfo[accountKey]['name']
        self.root.ids.name.text = name

        bioText = accInfo[accountKey]["bio"]
        self.root.ids.biography.text = bioText

        profile = accInfo[accountKey]['profilePicture']
        self.root.ids.profile_picture.source = profile

        sport = accInfo[accountKey]['sports']
        self.root.ids.sport_label.text = "Selected Interests: " + str(sport[0:len(sport) - 1])

        #displays chatrooms depending on interests
        chatRoomScreen = self.root.ids.chatRooms
        chatRoomScreen.clear_widgets()

        sport.strip()
        sport = sport[1:len(sport) - 1]
        sportList = sport.split(', ')

        publicRoom = MDRectangleFlatButton(text="Public Chatroom", size_hint=(1, .1), on_release=partial(self.chatRoomScreenToggle, "Chatroom"))
        chatRoomScreen.add_widget(publicRoom)

        for sports in sportList:
            chatRooms = MDRectangleFlatButton(text=sports, size_hint=(1, .1), on_release=partial(self.chatRoomScreenToggle, sports))
            chatRoomScreen.add_widget(chatRooms)
        
        personalChats = firebase.get('https://fitchat-d7a73-default-rtdb.firebaseio.com', "")
        for ids in personalChats.keys():
            idList = personalChats[ids]['ID'].split(', ')
            if accInfo[accountKey]['email'] in idList:
                chatID = ids
                idList.remove(accInfo[accountKey]['email'])
                users = firebase.get('/Users', '')
                for user in users.keys():
                        if users[user]['email'] in idList:
                            buttonName = users[user]['name']
                personalRooms = MDRectangleFlatButton(text=buttonName, size_hint=(1, .1), on_release=partial(self.chatRoomScreenToggle, chatID))
                chatRoomScreen.add_widget(personalRooms)
                
        print(sportList)
    def chatRoomScreenToggle(self, room, id):
        self.root.ids.ChatList.text = ''
        self.root.ids.sendMessageButton.on_press = partial(self.send_data, room)
        self.root.ids.chatHistoryButton.on_press = partial(self.get_hist, room)
        self.root.current = "Chatroom"

    def loginScreen(self):
        self.root.current = "createAccount"

    def profileListScreen(self):
        self.root.current = 'profileList'

    def friendRequestScreen(self):
        self.root.current = 'friendRequests'

    def friendRemoveScreen(self):
        self.root.current = 'removeFriend'

    def homeScreen(self):
        self.root.current = 'homepage'

    def homeScreenCamera(self):
        self.root.ids.camera.play = False
        self.root.current = 'homepage'

    def backToLoginScreen(self):
        self.root.current = 'login'

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
                        break
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
            'sports': "",
            'requests': '',
            'friends': '',
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
        sports = self.root.ids.sports_label.text

        data = {
            'email': email,
            'password': password,
            'profilePicture': profilePicture,
            'bio': bio,
            'name': name,
            'sports' : sports,
        }

        accountLink = 'https://fitchat-d7a73-default-rtdb.firebaseio.com/Users/' + accountKey
        firebase.patch(accountLink, data)
        # return back
        self.root.ids.change_text.text = "Avatar Successfully Changed"
        self.root.current = 'homepage'

    global firebase
    firebase = firebase.FirebaseApplication('https://fitchat-d7a73-default-rtdb.firebaseio.com/', None)
    global accountKey

    def get_hist(self, chatroom):
        chatroomLink = "/" + chatroom
        messages = firebase.get(chatroomLink, "")
        newMessages = ""
        for i in messages.keys():
            try:
                email = self.root.ids.email.text
                if messages[i]["Email"] == email:
                    email = 'You'
                else:
                    email = messages[i]["Email"]
                newMessages = newMessages + "\n" + (email) + ' said: \n' + (messages[i]["Message"] + '\n')
            except:
                pass
        self.root.ids.ChatList.text = newMessages

    def send_data(self, chatroom):
        email = self.root.ids.email.text
        chatroomLink = "/" + chatroom
        chatroomText = "ChatroomMessageText"
        data = {'Message': '',
                'Email': email}
        message = self.root.ids[chatroomText].text
        data['Message'] = message
        firebase.post('https://fitchat-d7a73-default-rtdb.firebaseio.com/' + chatroomLink, data)
        self.root.ids.ChatList.text += "\n" + 'You said: \n' + message + "\n"
        self.root.ids[chatroomText].text = ''

    cred = credentials.Certificate('fitchat-d7a73-firebase-adminsdk-ybqmf-e4babd672a.json')
    firebase_admin.initialize_app(cred)
    checks = []

    def check(self, instance, value, sport):
        if value == True:
            MyApp.checks.append(sport)
            sports = ""
            for i in MyApp.checks:
                sports = f"{sports} {i}" + ","
            self.root.ids.sports_label.text = f"{sports}"
        else:
            MyApp.checks.remove(sport)
            sports = ""
            for i in MyApp.checks:
                sports = f"{sports} {i}" + ","
            self.root.ids.sports_label.text = f"{sports}"

    def privacy_policy(instance):
        webbrowser.open("https://www.freeprivacypolicy.com/live/e80d9fa1-6aba-4479-bd20-f4a73d129eaf/")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.list_of_btns = []

    def createProfileList(self):
        profilelist = self.root.ids.profileListing
        profilelist.clear_widgets()
        #avatar_grid = self.root.ids.avatar_grid
        users = firebase.get('/Users', '')
        for user in users.keys():
            if user != accountKey:
                img = Image(source = users[user]['profilePicture'])
                btn = Button(text = 'User: ' + str(users[user]['name'] + '\nEmail: ' + users[user]['email'] + '\nInterest: ' + users[user]['sports']), on_press = self.press)
                profilelist.add_widget(img)
                profilelist.add_widget(btn)

    def showFriendList(self):
        friendListScreen = self.root.ids.friendList
        friendListScreen.clear_widgets()
        users = firebase.get('/Users', '')
        friends = users[accountKey]['friends']
        friendList = friends.split(', ')
        for user in users.keys():
            if users[user]['email'] in friendList:
                img = Image(source=users[user]['profilePicture'])
                btn = Button(text='User: ' + str(
                    users[user]['name'] + '\nEmail: ' + users[user]['email'] + '\nInterest: ' + users[user]['sports']),
                             on_press=self.press)
                friendListScreen.add_widget(img)
                friendListScreen.add_widget(btn)

    def showRequests(self):
        requestsListScreen = self.root.ids.requests
        requestsListScreen.clear_widgets()
        users = firebase.get('/Users', '')
        requests = users[accountKey]['requests']
        requestsList = requests.split(', ')
        for user in users.keys():
            if users[user]['email'] in requestsList:
                img = Image(source=users[user]['profilePicture'])
                btn = Button(text='User: ' + str(
                    users[user]['name'] + '\nEmail: ' + users[user]['email'] + '\nInterest: ' + users[user]['sports']),
                             on_press=self.press)
                requestsListScreen.add_widget(img)
                requestsListScreen.add_widget(btn)

    def showRemoveList(self):
        friendListScreen = self.root.ids.removeList
        friendListScreen.clear_widgets()
        users = firebase.get('/Users', '')
        friends = users[accountKey]['friends']
        friendList = friends.split(', ')
        for user in users.keys():
            if users[user]['email'] in friendList:
                img = Image(source=users[user]['profilePicture'])
                btn = Button(text='User: ' + str(
                    users[user]['name'] + '\nEmail: ' + users[user]['email'] + '\nInterest: ' + users[user]['sports']),
                             on_press=self.press)
                friendListScreen.add_widget(img)
                friendListScreen.add_widget(btn)

    def add(self,screen):
        friendemail = self.root.ids[screen].text
        users = firebase.get('/Users', "")
        ownEmail = users[accountKey]['email']
        for user in users.keys():
            if users[user]['email'] == friendemail:
                otherUser = user
                storeEmail = 'https://fitchat-d7a73-default-rtdb.firebaseio.com/Users/' + otherUser
                ownstoreEmail = 'https://fitchat-d7a73-default-rtdb.firebaseio.com/Users/' + accountKey
                ownRequests = users[accountKey]['requests'].split(', ')
                ownFriends = users[accountKey]['friends'].split(', ')
                otherRequests = users[otherUser]['requests'].split(', ')
                if users[otherUser]['email'] in ownRequests:
                    ownRequests.remove(users[otherUser]['email'])
                    updateRequest = ', '.join(ownRequests)
                    data = {'requests' : updateRequest}
                    firebase.patch(ownstoreEmail, data)
                    addData = users[accountKey]['friends'] + ', ' + users[otherUser]['email']
                    data = {'friends' : addData}
                    firebase.patch(ownstoreEmail, data)
                    addotherData = users[otherUser]['friends'] + ', ' + users[accountKey]['email']
                    data = {'friends' : addotherData}
                    firebase.patch(storeEmail, data)
                    chatData = users[accountKey]['email'] + ', ' + users[otherUser]['email']
                    data = {'ID' : chatData}
                    firebase.post('https://fitchat-d7a73-default-rtdb.firebaseio.com', data)
                elif (users[accountKey]['email'] in otherRequests) or (users[otherUser]['email'] in ownFriends):
                    pass
                else:
                    addData = users[otherUser]['requests'] + ', ' + ownEmail
                    data = {'requests' : addData}
                    firebase.patch(storeEmail,data)
            else:
                pass
    def remove(self, screen):
        friendemail = self.root.ids[screen].text
        users = firebase.get('/Users', "")
        for user in users.keys():
            if users[user]['email'] == friendemail:
                otherUser = user
                storeEmail = 'https://fitchat-d7a73-default-rtdb.firebaseio.com/Users/' + otherUser
                ownstoreEmail = 'https://fitchat-d7a73-default-rtdb.firebaseio.com/Users/' + accountKey
                ownFriends = users[accountKey]['friends'].split(', ')
                otherFriends = users[otherUser]['friends'].split(', ')
                if users[otherUser]['email'] in ownFriends:
                    ownFriends.remove(users[otherUser]['email'])
                    updateFriends = ', '.join(ownFriends)
                    data = {'friends': updateFriends}
                    firebase.patch(ownstoreEmail, data)
                    otherFriends.remove(users[accountKey]['email'])
                    updateOtherFriends = ', '.join(otherFriends)
                    otherData = {'friends': updateOtherFriends}
                    firebase.patch(storeEmail, otherData)
                else:
                    pass                    



    def press(self, instance):
        pass

if __name__ == '__main__':
    MyApp().run()
