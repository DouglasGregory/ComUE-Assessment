from tkinter import *
from functools import partial
import csv
import random


# Choose rounds = beginning
def to_quiz(num_rounds):
    Quiz(num_rounds)

    # hide the root.
    root.withdraw()


class ChooseRounds:
    def __init__(self):
        self.label = None
        self.entry = None
        self.placeholder = "Enter a number"
        self.placeholder_color = None
        self.custom_window = None
        self.submit_button = None
        self.default_color = None
        button_fg = "#FFFFFF"
        button_font = ("Arial", "13", "bold")

        # initialise variables
        self.var_feedback = StringVar()
        self.var_feedback.set("")

        self.var_has_error = StringVar()
        self.var_has_error.set("no")

        # Gui frame
        self.intro_frame = Frame(padx=5, pady=5)
        self.intro_frame.grid()

        # introduction / heading
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

        # create a output label for displaying messages
        self.output_label = Label(self.intro_frame, text="",
                                  fg="#980002")
        self.output_label.grid(row=3) # label in row 3

        # button colours
        btn_colour_value = [
            ["#E4D4AC", 5],
            ["#E4A484", 10]
        ]

        # create buttons for number of rounds
        for item in range(0, 2):
            self.rounds_button = Button(self.how_many_frame,
                                        fg=button_fg,
                                        bg=btn_colour_value[item][0],
                                        text="{}".format(btn_colour_value[item][1]),
                                        font=button_font, width=10,
                                        command=lambda i=item: to_quiz(btn_colour_value[i][1])
                                        )
            self.rounds_button.grid(row=0, column=item,
                                    padx=2.5, pady=2.5)

        self.custom_button = Button(self.how_many_frame,
                                    bg="#6C9484",
                                    fg=button_fg, text="Custom",
                                    font=button_font, width=10,
                                    command=lambda: self.custom_rounds()
                                    )
        self.custom_button.grid(row=0, column=2,
                                padx=2.5, pady=2.5)

    # Custom rounds/ opens a 2nd window
    def custom_rounds(self):
        self.custom_window = Toplevel()
        self.custom_window.title("Enter Number of Rounds")

        self.label = Label(self.custom_window, text="Enter a number (max 99):")
        self.label.grid(row=0, padx=5, pady=5)

        self.entry = Entry(self.custom_window)
        self.entry.grid(row=1, padx=5, pady=5)
        self.entry.bind("<FocusIn>", self.clear_placeholder)
        self.entry.bind("<FocusOut>", self.add_placeholder)

        # error label messages
        self.output_label = Label(self.custom_window, text="",
                                  fg="#980002")
        self.output_label.grid(row=2, padx=5, pady=5)

        self.submit_button = Button(self.custom_window,
                                    text="Submit",
                                    command=self.submit_custom_rounds)
        self.submit_button.grid(row=3, padx=5, pady=5)

        self.placeholder_color = "grey"
        self.default_color = self.entry.cget("fg")
        self.add_placeholder()

    # clears placeholder area

    def add_placeholder(self):
        if not self.entry.get():
            self.entry.insert(0, self.placeholder)
            self.entry.config(fg=self.placeholder_color)

    def clear_placeholder(self,):
        if self.entry.get() == self.placeholder:
            self.entry.delete(0, END)
            self.entry.config(fg=self.default_color, bg="white")

    # checks custom round input
    # provide error message if not correct
    def submit_custom_rounds(self):
        has_error = "no"

        try:
            num_rounds = int(self.entry.get())
            if 1 <= num_rounds <= 99:
                to_quiz(num_rounds)
                self.custom_window.destroy()
                self.custom_button.config(state=NORMAL)
            else:
                has_error = "yes"
                self.var_feedback.set("error: \n"
                                      "1-99 come on man\n"
                                      "You ended up picking below or above\n"
                                      "the maximum number of rounds.\n"
                                      "Please try again")
                self.output_label.config(fg="#000000")
                self.entry.config(bg="#FFFFFF")
        except ValueError:
            has_error = "yes"
            self.var_feedback.set("error: \n"
                                  "A whole number or an actual number\n"
                                  "was not presented. Please try again using\n"
                                  "a whole number.")
            self.output_label.config(fg="#000000")
            self.entry.config(bg="#FFFFFF")

        if has_error == "yes":
            self.var_has_error.set("yes")
            self.output_label.config(text=self.var_feedback.get())
        else:
            self.var_has_error.set("no")

    # Quiz function


# Csv File data
def get_all_data():
    with open("gods.csv", "r") as file:
        var_all_data = list(csv.reader(file, delimiter=","))
    # Remove the header row from the data.
    var_all_data.pop(0)
    return var_all_data


# Main gameplay
class Quiz:
    def __init__(self, how_many):
        self.god_name = None
        self.correct_answer = None
        background = "#E4E1CE"
        # see users score
        self.user_score = 0
        # new window for quiz
        self.quiz_box = Toplevel()

        # If users press X will close
        self.quiz_box.protocol('WM_DELETE_WINDOW', partial(self.close_quiz))

        # Variables used to work out statistics, when game ends etc
        self.rounds_wanted = IntVar()
        self.rounds_wanted.set(how_many)

        # see rounds played and set to 0
        self.rounds_played = IntVar()
        self.rounds_played.set(0)

        self.rounds_won = IntVar()
        self.rounds_won.set(0)

        # Load csv file data
        self.all_data = get_all_data()

        # Quiz frame
        self.quiz_frame = Frame(self.quiz_box, width=300,
                                height=200, padx=5, pady=5,
                                bg=background)
        self.quiz_frame.grid()

        # round heading
        rounds_heading = f"Choose - Round 1 of {how_many}"
        self.choose_heading = Label(self.quiz_frame, text=rounds_heading,
                                    font=("Ariel", "16", "bold"),
                                    bg=background)
        self.choose_heading.grid(row=0)

        # Instructions
        instructions = "Choose which ever option you feel is correct " \
                       "It shouldn't be that hard as its the same odds " \
                       "To get it correct!" \
                       " click on Help if you need more."
        self.instructions_label = Label(self.quiz_frame, text=instructions,
                                        wraplength=350, justify="left",
                                        bg=background)
        self.instructions_label.grid(row=1, padx=2.5, pady=2.5)

        # current question label
        self.question_label = Label(self.quiz_frame, text="Is this god a Major or Minor?",
                                    wraplength=350, justify="center",
                                    font=("Ariel", 16, "bold"), padx=2.5, pady=2.5,
                                    bg=background)
        self.question_label.grid(row=2)

        # Label for gods name
        self.god_label = Label(self.quiz_frame, text="god name goes here",
                               bg="#6C9484", width=40, font=("Ariel", "12"))
        self.god_label.grid(row=3, padx=2.5, pady=2.5)

        # option buttons
        self.option_frame = Frame(self.quiz_frame)
        self.option_frame.grid(row=4)

        # Major option
        self.Major_button = Button(self.option_frame, fg="#000000", width=17, bg="#E4D4AC",
                                   text="Major", font=("Arial", "12", "bold"),
                                   command=lambda: self.check_answer("Major"))
        self.Major_button.grid(row=0, column=0, padx=2.5, pady=2.5)

        # Minor option
        self.Minor_button = Button(self.option_frame, fg="#000000", width=17, bg="#E4D4AC",
                                   text="Minor", font=("Arial", "12", "bold"),
                                   command=lambda: self.check_answer("Minor"))
        self.Minor_button.grid(row=0, column=1, padx=2.5, pady=2.5)

        # navigation and round results
        self.rounds_frame = Frame(self.quiz_frame)
        self.rounds_frame.grid(row=5, padx=5, pady=5)

        # area that displays choice and result
        self.user_choice_label = Label(self.quiz_frame,
                                       text="When you choose things will "
                                            " be here!",
                                       bg="#E4A484", width=52,
                                       justify="left")
        self.user_choice_label.grid(row=5, padx=5, pady=5)

        # navigation buttons
        self.control_frame = Frame(self.quiz_frame)
        self.control_frame.grid(row=7)

        # current round results
        self.round_results_label = Label(self.rounds_frame, text="",
                                         width=44,
                                         font=("Arial", 10),
                                         bg=background)
        self.round_results_label.grid(row=0, column=0)

        self.start_over_button = Button(self.control_frame, text="Menu",
                                        fg="#FFFFFF", bg="#BE2727",
                                        font=("Arial", 11, "bold"),
                                        width=12,
                                        padx=2.5, pady=2.5,
                                        command=self.close_quiz)
        self.start_over_button.grid(row=0, column=0)

        # help button
        self.help_button = Button(self.control_frame, text="Instructions",
                                  fg="#FFFFFF", bg="#305CDE",
                                  font=("Arial", 11, "bold"),
                                  width=12,
                                  padx=2.5, pady=2.5,
                                  command=self.get_help)
        self.help_button.grid(row=0, column=1)

        # next round button
        self.next_button = Button(self.control_frame, text="Continue",
                                  fg="#FFFFFF", bg="#6C9484",
                                  font=("Arial", 11, "bold"),
                                  width=12, state=DISABLED,
                                  padx=2.5, pady=2.5,
                                  command=self.new_round)
        self.next_button.grid(row=0, column=2)

        # first round
        self.new_round()

    # new round
    def new_round(self):
        # stop next button from working at the start of new round
        self.next_button.config(state=DISABLED)
        self.Major_button.config(state=NORMAL)
        self.Minor_button.config(state=NORMAL)

        # check quiz status
        if self.rounds_played.get() >= self.rounds_wanted.get():
            self.question_label.config(text="Well Done, You finished.")
            self.Major_button.config(state=DISABLED)
            self.Minor_button.config(state=DISABLED)
            self.user_choice_label.config(text=f"Your Score: {self.user_score} out of {self.rounds_wanted.get()}")
            return

        # random question for new round
        current_question = random.choice(self.all_data)
        # Remove the selected question
        self.all_data.remove(current_question)

        # question details
        self.god_name = current_question[2]
        self.correct_answer = current_question[1]

        # New question
        self.god_label.config(text=self.god_name)
        self.choose_heading.config(text=f"Round {self.rounds_played.get() + 1} of {self.rounds_wanted.get()}")

    # checks answer
    def check_answer(self, user_answer):
        # score if correct
        if user_answer.lower() == self.correct_answer.lower():
            self.user_score += 1
            self.user_choice_label.config(text="Great work!\n"
                                               f"You've gotten it right! \n"
                                               f"{self.god_name} is {self.correct_answer}.",
                                          bg="#50C878", width="30", fg="#000000")
            self.round_results_label.config(
                text=f"Round {self.rounds_played.get() + 1}: Current score: {self.user_score}")

        else:
            self.user_choice_label.config(text="Well Gosh.. \n"
                                               "You really got that wrong? \n"
                                               f"{self.god_name} is {self.correct_answer}.",
                                          bg="#FF474C", width="30", fg="#000000")
            self.round_results_label.config(
                text=f"Round {self.rounds_played.get() + 1}: Current score: {self.user_score}")

        # enable the next round button after answer
        self.rounds_played.set(self.rounds_played.get() + 1)
        self.Minor_button.config(state=DISABLED)
        self.next_button.config(state=NORMAL)
        self.Major_button.config(state=DISABLED)

    # display help
    def get_help(self):
        DisplayHelp(self)

    # close quiz
    def close_quiz(self):
        # next game to start

        root.deiconify()
        self.quiz_box.destroy()


# Help information
class DisplayHelp:
    def __init__(self, partner):

        background = "#E4E1CE"
        self.help_box = Toplevel()

        # stop help button from working
        partner.help_button.config(state=DISABLED)

        # close help button

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
                    " Choosing between these two options you will be informed after if  \n" \
                    " you got it correct or not enjoy and have fun.\n" \

        self.help_text_label = Label(self.help_frame, bg=background,
                                     text=help_text, wraplength=350,
                                     justify="left")
        self.help_text_label.grid(row=1, padx=5)

        self.dismiss_button = Button(self.help_frame,
                                     font=("Arial", "12", "bold"),
                                     text="Close", bg="#305CDE",
                                     fg="#FFFFFF",
                                     command=partial(self.close_help,
                                                     partner))
        self.dismiss_button.grid(row=2, padx=5, pady=5)

    # stops help message
    def close_help(self, partner):
        # Put help button back to normal

        partner.help_button.config(state=NORMAL)
        self.help_box.destroy()


# Main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Major Minor Quiz")
    ChooseRounds()
    root.mainloop()
