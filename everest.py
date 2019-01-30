#!/usr/bin/python
import json
import os
import random
import time
from tkinter import *

user_map = {
	"r": "rebecca",
	"j": "josh",
	"d": "dom",
	"a": "andrew"
}

messages = ["Good work!", "Well done!", "Smashed it!", "Congrats!"]

def update_json(username, num_flights):
    jsonFile = open("data/climbs.json", "r") # Open the JSON file for reading
    data = json.load(jsonFile) # Read the JSON into the buffer
    jsonFile.close() # Close the JSON file

    ## Working with buffered content
    new_climb_dict = {
    	"climber": username,
    	"flights": num_flights,
    	"timestamp": int(time.time())
    }
    tmp = data["climbs"]
    tmp.append(new_climb_dict)
    data["climbs"] = tmp

    ## Save our changes to JSON file
    jsonFile = open("data/climbs.json", "w+")
    jsonFile.write(json.dumps(data))
    jsonFile.close()

def commit_json():
	add_command = "git add data/climbs.json"
	commit_command = "git commit -m \"update\""
	push_command = "git push"
	full_command = " && ".join([add_command, commit_command])
	os.system(full_command)


class FlexiLabel:
	def __init__(self, parent, starter_text, y, font_size):
		self.v = StringVar()
		self.v.set(starter_text)
		self.label = Label(parent, textvariable=self.v)
		self.label.place(x=500,y=y,anchor="center")
		self.label.config(font=("Courier",font_size))

	def clear(self):
		self.v.set("")

	def update(self, msg):
		self.v.set(msg)

	def temp_update(self, msg, millis):
		self.v.set(msg)
		self.label.after(millis, self.clear)


def key(event):
	global current_mode
	global current_user

	if current_mode == "number":
		num_char = str(event.char)
		if num_char in ['1','2','3','4','5','6','7']:
			response_label.temp_update(num_char, 500)
			congrats_label.temp_update(random.choice(messages), 1500)

			update_json(current_user, int(num_char))
			commit_json()

			current_mode = "user"
			instruction_label.update("Please enter user character...")
		else:
			instruction_label.update("Please enter valid number for flights climbed...")
	elif current_mode == "user":
		user_char = str(event.char)
		if user_char in list(user_map.keys()):
			response_label.temp_update(user_char, 500)
			instruction_label.update("Please enter number of flights climbed... ")
			(current_user, current_mode) = (user_map[user_char], "number")
		else:
			instruction_label.update("Please enter valid user character... ")


app = Tk()
frame = Frame(app, width=1000, height=800)

current_mode = "user"
current_user = ""

title_label = FlexiLabel(frame, "INRIX Everest Challenge", 100, 40)
instruction_label = FlexiLabel(frame, "Please enter user character...", 300, 22)
response_label = FlexiLabel(frame, "", 400, 22)
congrats_label = FlexiLabel(frame, "", 600, 30)

frame.bind("<Key>", key)
frame.focus_set()
frame.pack()

app.mainloop()