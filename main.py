import os
import json
import random
import tkinter as tk
from tkinter import messagebox
from tkinter import font as tkfont

WIDTH, HEIGHT = 1100, 700
MIN_W, MIN_H = 1000, 600

BASE_DIR = os.path.dirname(__file__)
DICT_FILE = os.path.join(BASE_DIR, "dictionary.json")

RUS_LETTERS = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"


def load_dictionary():
    with open(DICT_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


class BaldaApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Балда")
        self.root.geometry(f"{WIDTH}x{HEIGHT}")
        self.root.minsize(MIN_W, MIN_H)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = BaldaApp()
    app.run()