from tkinter import *
from functools import partial
import csv
import random


# Choose rounds class - beginning of programme
class ChooseRounds:
    def __init__(self):
        button_fg = "#FFFFFF"
        button_font = ("Arial", "13", "bold")

        # Initialise variables (such as the feedback variable)
        self.var_feedback = StringVar()
        self.var_feedback.set("")

        self.var_has_error = StringVar()
        self.var_has_error.set("no")

        # Set up GUI Frame
        self.intro_frame = Frame(padx=10, pady=10)
        self.intro_frame.grid()

        # Heading and introduction
        self.intro_heading_label = Label(self.intro_frame, text="Greek Gods",
                                         font=("Arial", "16", "bold"))
        self.intro_heading_label.grid(row=0)

        introduction = "Welcome to the Major or Minor God Quiz!" \
                       "To begin choose between 5, 10, or A Custom amount of rounds!, " \
                       "These will determine how many rounds you play!"
        self.choose_instructions_label = Label(self.intro_frame,
                                               text=introduction,
                                               wraplength=300, justify="left")
        self.choose_instructions_label.grid(row=1)

        # Setting up the "how many" frame
        self.how_many_frame = Frame(self.intro_frame)
        self.how_many_frame.grid(row=2)

        self.output_label = Label(self.intro_frame, text="",
                                  fg="#980002")
        self.output_label.grid(row=3)

        btn_colour_value = [
            ["#BE2727", 5],
            ["#305CDE", 10]
        ]

        for item in range(0, 2):
            self.rounds_button = Button(self.how_many_frame,
                                        fg=button_fg,
                                        bg=btn_colour_value[item][0],
                                        text="{}".format(btn_colour_value[item][1]),
                                        font=button_font, width=10,
                                        command=lambda i=item: self.to_quiz(btn_colour_value[i][1])
                                        )
            self.rounds_button.grid(row=0, column=item,
                                    padx=5, pady=5)

        self.custom_button = Button(self.how_many_frame,
                                    bg="#6C9484",
                                    fg=button_fg, text="Custom",
                                    font=button_font, width=10,
                                    command=lambda: self.custom_rounds()
                                    )
        self.custom_button.grid(row=0, column=2,
                                padx=5, pady=5)
