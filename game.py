from tkinter import *
from tkinter import messagebox
import random, pandas

BACKGROUND_COLOR = "#B1DDC6"
PATH = "romanian_words.csv"
PATH_TOLEARN = "words_to_learn.csv"

data = pandas.read_csv(PATH)
to_learn = data.to_dict(orient='records')
current_french_word = random.choice(to_learn)

def new_random_word(counter):
    global current_french_word, flip_timer
    window.after_cancel(flip_timer)
    #if pressed on check button, generate new french word and flip back the card
    if counter == 1:
        #Add exception if words_to_learn.csv is not available
        try:
            # Check if the CSV exists, otherwise create and append new word
            data_words = pandas.read_csv(PATH_TOLEARN)
            words_to_learn = pandas.DataFrame(data_words)
            new_row = pandas.DataFrame([{'Romanian': current_french_word['Romanian'], 'English': current_french_word['English']}])
            words_to_learn = pandas.concat([words_to_learn, new_row], ignore_index=True)
            words_to_learn.to_csv(PATH_TOLEARN, index=False)         
        except FileNotFoundError:
            # If the file doesn't exist, create a new one
            words_to_learn = pandas.DataFrame([{'Romanian': current_french_word['Romanian'], 'English': current_french_word['English']}])
            words_to_learn.to_csv(PATH_TOLEARN, index=False)   
        
        #Remove known word from french_words.csv
        to_learn.remove(current_french_word)
        update_data = pandas.DataFrame(to_learn)
        update_data.to_csv(PATH, index=False)
        current_french_word = random.choice(to_learn)    #Get a new random french word
        change_french()
        flip_timer = window.after(3000, func=change_english)
    else:
        current_french_word = random.choice(to_learn)    #Get a new random french word
        change_french()
        flip_timer = window.after(3000, func=change_english)

#Flip card and fetch English translation
def change_english():
    canvas.itemconfig(image_card, image=card_back_img)
    canvas.itemconfig(title_french, text ='English', fill='white')
    canvas.itemconfig(word_french, text=current_french_word['English'], fill='white')

#Flip card and fetch French translation
def change_french():
    canvas.itemconfig(image_card, image=card_front_img)
    canvas.itemconfig(title_french, text = 'Romanian', fill='black')
    canvas.itemconfig(word_french, text=current_french_word['Romanian'], fill='black')

#Tkinter window setup
window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, background=BACKGROUND_COLOR)

#Create canvas for displaying the flashcards
canvas = Canvas(height=526, width=800)
card_front_img = PhotoImage(file="card_front.png")
card_back_img = PhotoImage(file="card_back.png")
image_card = canvas.create_image(400, 263, image=card_front_img)
title_french = canvas.create_text(400, 150, text='Romanian', font=("Ariel", 40, "italic"))
word_french = canvas.create_text(400, 263, text=random.choice(to_learn), font=("Ariel", 60, "bold"))
canvas.config(background=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=0, column=0, columnspan=2)

#Buttons for known and unknown words
cross_image=PhotoImage(file='wrong.png')
unknown_button = Button(image=cross_image, highlightthickness=0, borderwidth=0, command=lambda: new_random_word(0))
unknown_button.grid(row=1, column=0)

check_image=PhotoImage(file='right.png')
known_button = Button(image=check_image, highlightthickness=0, borderwidth=0, command=lambda: new_random_word(1))
known_button.grid(row=1, column=1)

#After 3 seconds flip the card with english translation
flip_timer = window.after(3000, func=change_english)

#Start with a random word
new_random_word(0)

#All words are guessed print a message
if len(to_learn) == 1:
    messagebox.showinfo(title='Last card', message="Romanian: Macao / English: Uno")

window.mainloop()