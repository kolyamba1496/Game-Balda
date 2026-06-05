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
BG_COLOR = "#f4fbf6"
PANEL_COLOR = "#ffffff"
BUTTON_COLOR = "#bbf7d0"
BUTTON_HOVER = "#86efac"
BUTTON_TEXT = "#14532d"
ACCENT = "#16a34a"
DARK_GREEN = "#166534"
BOARD_EMPTY = "#f0fdf4"
BOARD_FILLED = "#dcfce7"
BOARD_SELECTED = "#bef264"
BOARD_NEW = "#86efac"
BOARD_BORDER = "#15803d"
def load_dictionary():
    with open(DICT_FILE, "r", encoding="utf-8") as file:
        return json.load(file)
class BaldaGame:
    def __init__(self, size, dictionary):
        self.size = size
        self.dictionary = set(dictionary)
        self.board = [["" for _ in range(size)] for _ in range(size)]
        self.used_words = set()
        self.current_player = 1
        self.scores = {1: 0, 2: 0}
        self.player_words = {1: [], 2: []}
        self.selected = []
        self.new_cell = None
        self.new_letter = None
        self.new_index = None
        self.pass_count = 0
        self.create_start_word()
    def create_start_word(self):
        words = [word for word in self.dictionary if len(word) == self.size]
        word = random.choice(words)
        row = self.size // 2
        for col, letter in enumerate(word):
            self.board[row][col] = letter
        self.used_words.add(word)
    def is_empty(self, r, c):
        return self.board[r][c] == ""
    def is_filled(self, r, c):
        return self.board[r][c] != ""
    def is_near(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1]) == 1
    def reset_turn(self):
        if self.new_cell and self.new_letter:
            r, c = self.new_cell
            self.board[r][c] = ""
        self.selected = []
        self.new_cell = None
        self.new_letter = None
        self.new_index = None
    def full_path(self):
        path = self.selected[:]
        if self.new_cell is not None:
            index = self.new_index
            if index is None:
                index = len(path)
            path.insert(index, self.new_cell)
        return path
    def current_word(self):
        return "".join(self.board[r][c] for r, c in self.full_path()).lower()
    def last_cell(self):
        path = self.full_path()
        return path[-1] if path else None
    def can_add_cell(self, r, c):
        cell = (r, c)
        if not self.is_filled(r, c):
            return False
        if cell in self.selected:
            return False
        if self.new_cell is not None and self.new_letter is None:
            return False
        if not self.selected and self.new_cell is None:
            return True
        last = self.last_cell()
        return last is None or self.is_near(cell, last)
    def add_cell(self, r, c):
        if not self.can_add_cell(r, c):
            return False, "Выберите соседнюю клетку."
        self.selected.append((r, c))
        return True, "Клетка добавлена."
    def can_choose_new_cell(self, r, c):
        if self.new_cell is not None:
            return False
        if not self.is_empty(r, c):
            return False
        if not self.selected:
            return True
        last = self.last_cell()
        return last is None or self.is_near((r, c), last)
    def choose_new_cell(self, r, c):
        if not self.can_choose_new_cell(r, c):
            return False, "Новая клетка должна быть пустой и соседней."
        self.new_cell = (r, c)
        self.new_index = len(self.selected)
        return True, "Новая клетка выбрана."
    def set_letter(self, letter):
        if self.new_cell is None:
            return False, "Сначала выберите пустую клетку."
        if self.new_letter:
            r, c = self.new_cell
            self.board[r][c] = ""
        self.new_letter = letter.lower()
        r, c = self.new_cell
        self.board[r][c] = self.new_letter
        return True, "Буква поставлена."
    def check_word(self):
        if self.new_cell is None:
            return False, "Сначала выберите пустую клетку."
        if self.new_letter is None:
            return False, "Сначала выберите букву."
        if not self.selected:
            return False, "Выберите остальные буквы слова."
        word = self.current_word()
        if len(word) < 2:
            return False, "Слово слишком короткое."
        if word in self.used_words:
            return False, "Это слово уже использовалось."
        if word not in self.dictionary:
            return False, "Слова нет в словаре."
        return True, word
    def submit(self):
        ok, result = self.check_word()
        if not ok:
            return False, result
        word = result
        player = self.current_player
        self.used_words.add(word)
        self.player_words[player].append(word)
        self.scores[player] += len(word)
        self.selected = []
        self.new_cell = None
        self.new_letter = None
        self.new_index = None
        self.pass_count = 0
        self.change_player()
        return True, word
    def pass_turn(self):
        self.reset_turn()
        self.pass_count += 1
        self.change_player()
    def change_player(self):
        self.current_player = 2 if self.current_player == 1 else 1
    def board_is_full(self):
        return all(all(cell != "" for cell in row) for row in self.board)
    def is_finished(self):
        return self.board_is_full() or self.pass_count >= 2
    def winner_text(self):
        s1 = self.scores[1]
        s2 = self.scores[2]
        if s1 > s2:
            return f"Победил Игрок 1\nСчёт: {s1} : {s2}"
        if s2 > s1:
            return f"Победил Игрок 2\nСчёт: {s1} : {s2}"
        return f"Ничья\nСчёт: {s1} : {s2}"
class BaldaApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Балда")
        self.root.geometry(f"{WIDTH}x{HEIGHT}")
        self.root.minsize(MIN_W, MIN_H)
        self.root.configure(bg=BG_COLOR)
        self.main_font = tkfont.Font(family="Arial", size=10)
        self.big_font = tkfont.Font(family="Arial", size=16, weight="bold")
        self.title_font = tkfont.Font(family="Arial", size=24, weight="bold")
        self.root.option_add("*Font", self.main_font)
        self.root.bind("<Configure>", self.resize_font)
        self.dictionary = load_dictionary()
        self.size = 5
        self.game = None
        self.buttons = []
        self.letter_var = tk.StringVar(value="")
        self.show_menu()
    def resize_font(self, event=None):
        scale = min(self.root.winfo_width() / WIDTH, self.root.winfo_height() / HEIGHT)
        self.main_font.configure(size=max(8, min(12, int(10 * scale))))
        self.big_font.configure(size=max(12, min(18, int(16 * scale))))
        self.title_font.configure(size=max(18, min(28, int(24 * scale))))
    def clear(self):
        for widget in self.root.winfo_children():
            widget.destroy()
    def button(self, parent, text, command, width=18, height=1):
        return tk.Button(
            parent,
            text=text,
            width=width,
            height=height,
            command=command,
            bg=BUTTON_COLOR,
            fg=BUTTON_TEXT,
            activebackground=BUTTON_HOVER,
            activeforeground=BUTTON_TEXT,
            relief="flat",
            cursor="hand2",
            font=self.main_font,
            bd=0
        )
    def show_menu(self):
        self.clear()
        frame = tk.Frame(self.root, padx=20, pady=20, bg=BG_COLOR)
        frame.pack(expand=True, fill=tk.BOTH)
        center = tk.Frame(frame, bg=BG_COLOR)
        center.place(relx=0.5, rely=0.5, anchor="center")
        tk.Label(center, text="ИГРА «БАЛДА»", font=self.title_font, bg=BG_COLOR, fg=DARK_GREEN).pack(pady=(0, 30))
        menu_box = tk.Frame(center, bg=PANEL_COLOR, padx=40, pady=30, highlightbackground="#bbf7d0", highlightthickness=2)
        menu_box.pack()
        self.button(menu_box, "Играть", self.show_modes, width=22, height=2).pack(pady=8)
        self.button(menu_box, "Правила", self.show_rules, width=22, height=2).pack(pady=8)
        self.button(menu_box, "Выход", self.root.destroy, width=22, height=2).pack(pady=8)
        def show_modes(self):
            self.clear()
            frame = tk.Frame(self.root, padx=20, pady=20, bg=BG_COLOR)
            frame.pack(expand=True, fill=tk.BOTH)
            tk.Label(frame, text="Выбор режима игры", font=self.title_font, bg=BG_COLOR, fg=DARK_GREEN).pack(pady=20)
            box = tk.LabelFrame(frame, text="Размер поля", padx=20, pady=20, bg=PANEL_COLOR, fg=DARK_GREEN,
                                highlightbackground="#bbf7d0", highlightthickness=2)
            box.pack(pady=20)
            size_var = tk.IntVar(value=self.size)
            for value in (5, 6, 7):
                tk.Radiobutton(
                    box,
                    text=f"{value} x {value}",
                    variable=size_var,
                    value=value,
                    bg=PANEL_COLOR,
                    fg=BUTTON_TEXT,
                    activebackground=PANEL_COLOR,
                    selectcolor=BUTTON_COLOR,
                    command=lambda v=size_var: self.set_size(v.get())
                ).pack(anchor="w", pady=5)
            bottom = tk.Frame(frame, bg=BG_COLOR)
            bottom.pack(pady=20)
            self.button(bottom, "Начать игру", self.start_game).grid(row=0, column=0, padx=10)
            self.button(bottom, "Назад в меню", self.show_menu).grid(row=0, column=1, padx=10)

        def set_size(self, value):
            self.size = value

        def start_game(self):
            self.game = BaldaGame(self.size, self.dictionary)
            self.show_game()

        def show_game(self):
            self.clear()
            self.buttons = []
            top = tk.Frame(self.root, padx=5, pady=5, bg=DARK_GREEN)
            top.pack(fill=tk.X)
            self.info_label = tk.Label(top, font=self.main_font, bg=DARK_GREEN, fg="white")
            self.info_label.pack(side=tk.LEFT, padx=10)
            self.button(top, "Правила игры", self.show_rules, width=13).pack(side=tk.RIGHT, padx=4)
            self.button(top, "Выход в меню", self.confirm_exit, width=13).pack(side=tk.RIGHT, padx=4)
            main = tk.Frame(self.root, padx=5, pady=5, bg=BG_COLOR)
            main.pack(expand=True, fill=tk.BOTH)
            self.create_left_panel(main)
            self.create_right_panel(main)
            self.create_center_panel(main)
            self.refresh()

        def create_left_panel(self, parent):
            left = tk.Frame(parent, bg=BG_COLOR)
            left.pack(side=tk.LEFT, fill=tk.Y, padx=4)
            letter_box = tk.LabelFrame(left, text="Выбранная буква", padx=5, pady=5, bg=PANEL_COLOR, fg=DARK_GREEN,
                                       highlightbackground="#bbf7d0", highlightthickness=1)
            letter_box.pack(fill=tk.X, pady=4)
            tk.Label(letter_box, textvariable=self.letter_var, font=self.big_font, width=4, bg=PANEL_COLOR,
                     fg=ACCENT).pack()
            self.button(letter_box, "Сбросить ход", self.cancel_turn, width=14).pack(pady=4)
            self.action_box = tk.LabelFrame(left, text="Ход Игрока 1", padx=5, pady=5, bg=PANEL_COLOR, fg=DARK_GREEN,
                                            highlightbackground="#bbf7d0", highlightthickness=1)
            self.action_box.pack(fill=tk.X, pady=4)
            self.button(self.action_box, "Подтвердить", self.submit_word, width=14).pack(fill=tk.X, pady=3)
            self.button(self.action_box, "Пас", self.pass_turn, width=14).pack(fill=tk.X, pady=3)

            def create_right_panel(self, parent):
                right = tk.Frame(parent, bg=BG_COLOR)
                right.pack(side=tk.RIGHT, fill=tk.Y, padx=4)
                score_box = tk.LabelFrame(right, text="Очки", padx=5, pady=5, bg=PANEL_COLOR, fg=DARK_GREEN,
                                          highlightbackground="#bbf7d0", highlightthickness=1)
                score_box.pack(fill=tk.X, pady=4)
                self.score_label = tk.Label(score_box, font=self.big_font, bg=PANEL_COLOR, fg=ACCENT)
                self.score_label.pack()
                lists = tk.Frame(right, bg=BG_COLOR)
                lists.pack(fill=tk.BOTH, expand=True)
                self.list_p1 = self.create_word_list(lists, "Слова Игрока 1")
                self.list_p2 = self.create_word_list(lists, "Слова Игрока 2")

            def create_word_list(self, parent, title):
                box = tk.LabelFrame(parent, text=title, padx=5, pady=5, bg=PANEL_COLOR, fg=DARK_GREEN,
                                    highlightbackground="#bbf7d0", highlightthickness=1)
                box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=2)
                listbox = tk.Listbox(box, width=14, height=16, bg="#ffffff", fg=BUTTON_TEXT, relief="flat",
                                     highlightthickness=1, highlightbackground="#bbf7d0")
                listbox.pack(fill=tk.BOTH, expand=True)
                return listbox

            def create_center_panel(self, parent):
                center = tk.Frame(parent, bg=BG_COLOR)
                center.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=5)
                self.turn_label = tk.Label(center, text="Ходит Игрок 1", font=self.big_font, fg=DARK_GREEN, bg=BG_COLOR)
                self.turn_label.pack(pady=3)
                self.word_label = tk.Label(center, bg=BG_COLOR, fg=BUTTON_TEXT)
                self.word_label.pack(pady=3)
                tk.Label(center,
                         text="Выбирайте буквы по порядку. Новую букву можно вставить в начало, середину или конец слова.",
                         bg=BG_COLOR,
                         fg=BUTTON_TEXT).pack(pady=2)
                self.board_frame = tk.Frame(center, bg=BOARD_BORDER, padx=5, pady=5)
                self.board_frame.pack(pady=8)
                self.create_board()
                keyboard = tk.LabelFrame(center, text="Экранная клавиатура", padx=5, pady=5, bg=PANEL_COLOR,
                                         fg=DARK_GREEN, highlightbackground="#bbf7d0", highlightthickness=1)
                keyboard.pack(pady=5)
                self.create_keyboard(keyboard)

            def create_board(self):
                for r in range(self.game.size):
                    row = []
                    for c in range(self.game.size):
                        btn = tk.Button(
                            self.board_frame,
                            text=self.game.board[r][c].upper(),
                            width=3,
                            height=1,
                            font=self.big_font,
                            bg=BOARD_FILLED if self.game.board[r][c] else BOARD_EMPTY,
                            fg=BUTTON_TEXT,
                            activebackground=BUTTON_HOVER,
                            relief="solid",
                            bd=1,
                            highlightthickness=1,
                            highlightbackground=BOARD_BORDER,
                            highlightcolor=BOARD_BORDER,
                            cursor="hand2",
                            command=lambda rr=r, cc=c: self.click_cell(rr, cc)
                        )
                        btn.grid(row=r, column=c, padx=2, pady=2)
                        row.append(btn)
                    self.buttons.append(row)

            def create_keyboard(self, parent):
                for i, letter in enumerate(RUS_LETTERS):
                    tk.Button(
                        parent,
                        text=letter,
                        width=2,
                        height=1,
                        bg=BUTTON_COLOR,
                        fg=BUTTON_TEXT,
                        activebackground=BUTTON_HOVER,
                        relief="solid",
                        bd=1,
                        highlightthickness=1,
                        highlightbackground="#86efac",
                        cursor="hand2",
                        command=lambda l=letter: self.select_letter(l)
                    ).grid(row=i // 11, column=i % 11, padx=1, pady=1)
    def click_cell(self, r, c):
        cell = (r, c)
        if self.game.selected and self.game.selected[-1] == cell and self.game.new_cell is None:
            self.game.selected.pop()
            self.refresh()
            return
        if self.game.new_cell == cell:
            if self.game.new_letter:
                rr, cc = self.game.new_cell
                self.game.board[rr][cc] = ""
            self.game.new_cell = None
            self.game.new_letter = None
            self.game.new_index = None
            self.letter_var.set("")
            self.refresh()
            return
        if self.game.is_filled(r, c):
            if self.game.new_cell is not None and self.game.new_letter is None:
                messagebox.showwarning("Ошибка", "Сначала выберите букву на экранной клавиатуре.")
                return
            ok, msg = self.game.add_cell(r, c)
        else:
            ok, msg = self.game.choose_new_cell(r, c)
        if not ok:
            messagebox.showwarning("Ошибка", msg)
        self.refresh()
    def select_letter(self, letter):
        ok, msg = self.game.set_letter(letter)
        if not ok:
            messagebox.showwarning("Ошибка", msg)
            return
        self.letter_var.set(letter)
        self.refresh()
    def submit_word(self):
        ok, result = self.game.submit()
        if not ok:
            messagebox.showerror("Ошибка", result)
            self.refresh()
            return
        messagebox.showinfo("Успех", f"Слово принято: {result}")
        self.letter_var.set("")
        self.refresh()
        if self.game.is_finished():
            self.finish_game()
    def cancel_turn(self):
        self.game.reset_turn()
        self.letter_var.set("")
        self.refresh()
    def pass_turn(self):
        self.game.pass_turn()
        self.letter_var.set("")
        self.refresh()
        if self.game.is_finished():
            self.finish_game()
    def finish_game(self):
        messagebox.showinfo("Игра окончена", self.game.winner_text())
        self.show_menu()
    def confirm_exit(self):
        if messagebox.askyesno("Выход", "Вернуться в главное меню? Текущая партия будет завершена."):
            self.show_menu()