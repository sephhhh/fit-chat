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

Window.size = (350, 700)


Builder.load_file('main.kv')

firebase = firebase.FirebaseApplication('https://fitchat-d7a73-default-rtdb.firebaseio.com/Chat', None)

class fscreen(Widget):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)

		self.list_of_btns = []


	def create(self):
		self.h = self.height*0.9
		users = firebase.get('/Users', "")
		for user in users.keys():
			if user != accInfo[accountKey]:
				self.h = self.h - self.height*0.1
				self.btn = Button(text='User: '+str(users[user]['name']), size=(self.width*0.4, self.height*0.05), pos=(self.width*0.3, self.h), on_press = self.press)
				self.list_of_btns.append(self.btn)
				self.add_widget(self.btn)
	

	def press(self, instance):
		pass

class fitchat(App):
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