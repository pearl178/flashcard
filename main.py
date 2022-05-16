from tkinter import *
from pandas import *
import random
BACKGROUND_COLOR = "#B1DDC6"
ja_dict = []
ja_word = ''


def update_dict():
    try:
        data_frame = read_csv("data/to_learn.csv")
    except FileNotFoundError:
        data_frame = read_csv("data/ja_words.csv")
    global ja_dict
    ja_dict = {row.ja: row.en for (index, row) in data_frame.iterrows()}


def generate_new_word():
    global ja_dict, ja_word
    ja_word = random.choice(list(ja_dict))


def delete_word():
    global ja_dict
    global ja_word
    del ja_dict[ja_word]
    words_ja = [ja for (ja, en) in ja_dict.items() if ja != 'ja']
    words_en = [en for (ja, en) in ja_dict.items() if en != 'en']
    to_learn = {'ja': words_ja, 'en': words_en}
    df = DataFrame(to_learn)
    df.to_csv('data/to_learn.csv')


def right_new_ja_word():
    delete_word()
    update_dict()
    button_click()


def button_click():
    global flip_timer
    window.after_cancel(flip_timer)
    generate_new_word()
    canvas.itemconfig(language, text="Japanese", fill='black')
    canvas.itemconfig(card_image, image=card_front)
    canvas.itemconfig(word, text=ja_word, fill='black')
    flip_timer = window.after(3000, flip_card)


def flip_card():
    canvas.itemconfig(card_image, image=card_back)
    canvas.itemconfig(language, text="English", fill='white')
    en_word = ja_dict[ja_word]
    canvas.itemconfig(word, text=en_word, fill='white')


update_dict()
generate_new_word()


window = Tk()
window.title("Flashcards")
window.config(bg=BACKGROUND_COLOR, pady=50, padx=50)

card_front = PhotoImage(file="images/card_front.png")
card_back = PhotoImage(file="images/card_back.png")
right_img = PhotoImage(file="images/right.png")
wrong_img = PhotoImage(file="images/wrong.png")

canvas = Canvas(width=800, height=526, highlightthickness=0, bg=BACKGROUND_COLOR)
canvas.grid(column=0, row=1, columnspan=2)
card_image = canvas.create_image(400, 263, image=card_front)
language = canvas.create_text(400, 150, font=("Ariel", 40, "italic"), text='Japanese')
word = canvas.create_text(400, 280, font=("Ariel", 60, "bold"), text=ja_word)

right_button = Button(image=right_img, highlightthickness=0, command=right_new_ja_word)
right_button.grid(column=0, row=2)
wrong_button = Button(image=wrong_img, highlightthickness=0, command=button_click)
wrong_button.grid(column=1, row=2)

flip_timer = window.after(3000, flip_card)


window.mainloop()
