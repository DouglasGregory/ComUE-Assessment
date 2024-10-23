from tkinter import *
from functools import partial
import csv
import random


def new_round(self):
    # Disable the next button at the start of each round.
    self.next_button.config(state=DISABLED)
    self.Major_button.config(state=NORMAL)
    self.Minor_button.config(state=NORMAL)

    # Check if the quiz is complete.
    if self.rounds_played.get() >= self.rounds_wanted.get():
        self.question_label.config(text="Well Done, You finished.")
        self.Major_button.config(state=DISABLED)
        self.Minor_button.config(state=DISABLED)
        self.user_choice_label.config(text=f"Your Score: {self.user_score} out of {self.rounds_wanted.get()}")
        return

    # Select a random question for the new round.
    current_question = random.choice(self.all_data)
    # Remove the selected question from the data.
    self.all_data.remove(current_question)

    # Set the question details.
    self.god_name = current_question[2]
    self.correct_answer = current_question[1]

    # Update the UI wih the new question.
    self.god_label.config(text=self.god_name)
    self.choose_heading.config(text=f"Round {self.rounds_played.get() + 1} of {self.rounds_wanted.get()}")
