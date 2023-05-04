import socket 
import kivy
from kivy.uix.gridlayout import GridLayout
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget 
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.core.window import Window
from kivy.config import Config
from kivy.lang import Builder
from kivy.properties import StringProperty, ObjectProperty, NumericProperty, ReferenceListProperty
from kivy.graphics.texture import Texture
from kivy.core.camera import Camera
from kivy.graphics import *
import time
import os 
from pathlib import Path 							
import struct
import threading
import pickle
from firebase import firebase
import firebase_admin
from kivymd.app import MDApp
from kivymd.uix.textfield import MDTextField

Window.size = (350, 700)


Builder.load_file('main.kv')

firebase = firebase.FirebaseApplication('https://fitchat-d7a73-default-rtdb.firebaseio.com/Chat', None)

class fscreen(Widget):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)

		self.list_of_btns = []


	def create(self):
		accountKey = '-NTZUO5QPBsQQDBqCvLL'
		self.h = self.height*0.9
		users = firebase.get('/Users', "")
		for user in users.keys():
			if user != accountKey: 
				self.h = self.h - self.height*0.08
				self.img = Image(source =users[user]['profilePicture'],size=(self.width*0.15, self.height*0.08), pos=(self.width*0, self.h))
				self.btn = Button(text='User: '+str(users[user]['name'] + '\nEmail: ' +users[user]['email'] + '\nInterests: ' + users[user]['sports']), size=(self.width*1, self.height*0.08), pos=(self.width*0.15, self.h), halign = 'left',on_press = self.press)
				self.list_of_btns.append(self.btn)
				self.add_widget(self.btn)
				self.add_widget(self.img)
	
	def add(self):
		accountKey = '-NTZUO5QPBsQQDBqCvLL'
		friendemail = self.ids.friendrequest.text
		users = firebase.get('/Users', "")
		for user in users.keys():
			if users[user]['email'] == friendemail:
				otherUser = user
			elif user == accountKey:
				ownEmail = users[user]['email']
		storeEmail = 'https://fitchat-d7a73-default-rtdb.firebaseio.com/Users/' + otherUser
		ownstoreEmail = 'https://fitchat-d7a73-default-rtdb.firebaseio.com/Users/' + accountKey
		ownRequests = users[accountKey]['requests'].split(', ')
		ownFriends = users[accountKey]['friends'].split(', ')
		print(ownRequests)
		otherRequests = users[otherUser]['requests'].split(', ')
		print(otherRequests)
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
		elif (users[accountKey]['email'] in otherRequests) or (users[otherUser]['email'] in ownFriends):
			pass
		else:
			addData = users[otherUser]['requests'] + ', ' + ownEmail
			data = {'requests' : addData}
			firebase.patch(storeEmail,data)
			

	def press(self, instance):
		pass

class fitchat(MDApp):
	def build(self):
		
		self.screenm = ScreenManager() 

		self.fscreen = fscreen()
		screen = Screen(name = "friendlist")
		screen.add_widget(self.fscreen)
		self.screenm.add_widget(screen)


		return self.screenm

if __name__ == "__main__":
	fit = fitchat()	
	fit.run()
