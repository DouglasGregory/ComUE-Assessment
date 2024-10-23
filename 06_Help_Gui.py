from tkinter import *
from functools import partial
import csv
import random

class DisplayHelp:
    def __init__(self, partner):
        # setup dialogue box and background colour
        background = "#E4E1CE"
        self.help_box = Toplevel()

        # disable help button
        partner.help_button.config(state=DISABLED)

        # If users press cross at top, closes help and
        # 'releases' help button
        self.help_box.protocol('WM_DELETE_WINDOW',
                               partial(self.close_help, partner))

        self.help_frame = Frame(self.help_box, width=500,
                                height=400,
                                bg=background)
        self.help_frame.grid()

        self.help_heading_label = Label(self.help_frame,
                                        bg=background,
                                        text="Help",
                                        font=("Arial", "14", "bold"))
        self.help_heading_label.grid(row=0)

        # help text
        help_text = "To play this quiz your task is to" \
                    " see how many questions you can get correct by guessing between, " \
                    "Major and Minor Gods." \
                    " When you run this game you have these options below..\n" \
                    "options - 5, 10 or a custom amount (1-99). \n" \

        self.help_text_label = Label(self.help_frame, bg=background,
                                     text=help_text, wraplength=350,
                                     justify="left")
        self.help_text_label.grid(row=1, padx=10)

        self.dismiss_button = Button(self.help_frame,
                                     font=("Arial", "12", "bold"),
                                     text="Dismiss", bg="#305CDE",
                                     fg="#FFFFFF",
                                     command=partial(self.close_help,
                                                     partner))
        self.dismiss_button.grid(row=2, padx=10, pady=10)

    # closes help dialogue (used by button and x at top of dialogue)
    def close_help(self, partner):
        # Put help button back to normal...

        partner.help_button.config(state=NORMAL)
        self.help_box.destroy()
