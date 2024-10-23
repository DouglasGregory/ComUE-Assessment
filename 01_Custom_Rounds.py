from tkinter import *
from functools import partial
import csv
import random

def custom_rounds(self):
    self.custom_window = Toplevel()
    self.custom_window.title("Enter Number of Rounds")

    self.label = Label(self.custom_window, text="Enter a number (max 100):")
    self.label.grid(row=0, padx=10, pady=10)

    self.entry = Entry(self.custom_window)
    self.entry.grid(row=1, padx=10, pady=10)
    self.entry.bind("<FocusIn>", self.clear_placeholder)
    self.entry.bind("<FocusOut>", self.add_placeholder)

    # Output label for error messages
    self.output_label = Label(self.custom_window, text="",
                              fg="#980002")
    self.output_label.grid(row=2, padx=10, pady=10)

    self.submit_button = Button(self.custom_window,
                                text="Submit",
                                command=self.submit_custom_rounds)
    self.submit_button.grid(row=3, padx=10, pady=10)

    self.placeholder = "Enter a number"
    self.placeholder_color = "grey"
    self.default_color = self.entry.cget("fg")
    self.add_placeholder(None)


# clear the placeholder box automatically when an incorrect response is submitted

def add_placeholder(self, event):
    if not self.entry.get():
        self.entry.insert(0, self.placeholder)
        self.entry.config(fg=self.placeholder_color)


def clear_placeholder(self, event):
    if self.entry.get() == self.placeholder:
        self.entry.delete(0, END)
        self.entry.config(fg=self.default_color, bg="white")


# method to check the input for custom rounds
# if invalid, provide error message
def submit_custom_rounds(self):
    has_error = "no"

    try:
        num_rounds = int(self.entry.get())
        if 1 <= num_rounds <= 100:
            self.to_quiz(num_rounds)
            self.custom_window.destroy()
            self.custom_button.config(state=NORMAL)
        else:
            has_error = "yes"
            self.var_feedback.set("ERROR: \n"
                                  "Oops! It looks like you've entered a value\n"
                                  "that is below the minimum or above the\n"
                                  "maximum number of rounds.\n"
                                  "Please try again")
            self.output_label.config(fg="#980002")
            self.entry.config(bg="#F8CE00")
    except ValueError:
        has_error = "yes"
        self.var_feedback.set("ERROR: \n"
                              "Oops! That isn't right!\n"
                              "Please try again using\n"
                              "a whole number.")
        self.output_label.config(fg="#980002")
        self.entry.config(bg="#F8CE00")

    if has_error == "yes":
        self.var_has_error.set("yes")
        self.output_label.config(text=self.var_feedback.get())
    else:
        self.var_has_error.set("no")