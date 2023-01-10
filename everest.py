#!/usr/bin/python
import json
import os
import random
import time
from tkinter import *
from tkinter import messagebox, ttk

users = [
	"Aileen Holohan",
	"Allan Chan",
	"Andrew Turner",
	"Bryn Mills",
	"Caitlin Kilcoyne",
	"Christina Schreiber",
	"Dave Moseley",
	"Egidijus Kukstas",
	"Filipe Cunha",
	"Ian Whelan",
	"Jegor Popovkin",
	"Joshua Kidd",
	"Martin Rodgers",
	"Max Culley",
	"Nicholas Burgoyne",
	"Ross Fenning",
	"Samuel Dysch",
	"Tina Buckley"
]

messages = ["Good work!", "Well done!", "Smashed it!", "Congrats!", "Sensational!", "You're on fire!", "Wonderful!", "Outstanding!", "Marvelous!", "Tremendous!", "Wow!"]

def push_update(username, num_flights):
    jsonFile = open("data/climbdata.json", "r") # Open the JSON file for reading
    data = json.load(jsonFile) # Read the JSON into the buffer
    jsonFile.close() # Close the JSON file

    new_climb_dict = {
    	"climber": username,
    	"flights": num_flights,
    	"timestamp": int(time.time())
    }
    tmp = data["climbs"]
    tmp.append(new_climb_dict)
    data["climbs"] = tmp

    ## Save our changes to JSON file
    jsonFile = open("data/climbdata.json", "w+")
    jsonFile.write(json.dumps(data))
    jsonFile.close()

    add_command = "git add data/climbdata.json"
    commit_command = "git commit -m \"update at {}\"".format(str(time.time()))
    push_command = "git push"
    full_command = " && ".join([add_command, commit_command, push_command])
    os.system(full_command)
    return True


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

	def update_and_function(self, msg, millis, username, num_flights):
		self.v.set(msg)
		self.label.after(millis, self.clear)
		push_update(username, int(num_flights))

def handle_logged_steps():

	(instruction_label, response_label, congrats_label) = labels
	user = combo.get()

	instruction_label.update(f"Logging climb for {user}...")
	frame.update()

	push_update(user, 5)

	congrats_label.temp_update(random.choice(messages), 2500)
	instruction_label.update("Please select user...")

def main():
	global current_mode
	global current_user
	global combo
	global labels
	global frame

	app = Tk()
		
	frame = Frame(app, width=1000, height=800)

	current_mode = "user"
	current_user = ""
	
	title_label = FlexiLabel(frame, "INRIX Everest Challenge", 100, 40)
	instruction_label = FlexiLabel(frame, "Please select user...", 300, 22)
	response_label = FlexiLabel(frame, "", 400, 22)
	congrats_label = FlexiLabel(frame, "", 600, 30)
	labels = (instruction_label, response_label, congrats_label)
	
	combo = ttk.Combobox(state="readonly",values=users)
	combo.place(relx=.4, y=350, anchor= CENTER)  #.place(x=390, y=350)

	button = ttk.Button(text="Submit", command=handle_logged_steps)
	button.place(relx=.6, y=350, anchor= CENTER)

	frame.focus_set()
	frame.pack()
	
	app.mainloop()


if __name__ == "__main__":

	main()
