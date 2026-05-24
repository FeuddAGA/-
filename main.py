import tkinter as tk
from tkinter import ttk, messagebox
import random
import json
import os

# ---------- Данные ----------
quotes = [
    {
        "text": "Будь собой, остальные роли уже заняты.",
        "author": "Оскар Уайльд",
        "theme": "Мотивация"
    },
    {
        "text": "Знание — сила.",
        "author": "Фрэнсис Бэкон",
        "theme": "Образование"
    },
    {
        "text": "Жизнь — это то, что происходит, пока ты строишь планы.",
        "author": "Джон Леннон",
        "theme": "Жизнь"
    },
    {
        "text": "Никогда не сдавайся.",
        "author": "Уинстон Черчилль",
        "theme": "Мотивация"
    }
]

history = []
JSON_FILE = "quotes_history.json"


# ---------- Функции ----------
def generate_quote():
    author_filter = author_combobox.get()
    theme_filter = theme_combobox.get()

    filtered_quotes = quotes

    # Фильтрация по автору
    if author_filter != "Все":
        filtered_quotes = [
            q for q in filtered_quotes
            if q["author"] == author_filter
        ]

    # Фильтрация по теме
    if theme_filter != "Все":
        filtered_quotes = [
            q for q in filtered_quotes
            if q["theme"] == theme_filter
        ]

    if not filtered_quotes:
        messagebox.showwarning(
            "Ошибка",
            "Нет цитат по выбранному фильтру!"
        )
        return

    quote = random.choice(filtered_quotes)

    quote_text.set(f'"{quote["text"]}"')
    author_text.set(f'— {quote["author"]}')
    theme_text.set(f'Тема: {quote["theme"]}')

    history.append(quote)

    history_listbox.insert(
        tk.END,
        f'{quote["author"]}: {quote["text"]}'
    )


def add_quote():
    text = quote_entry.get().strip()
    author = author_entry.get().strip()
    theme = theme_entry.get().strip()

    # Проверка пустых строк
    if not text or not author or not theme:
        messagebox.showerror(
            "Ошибка",
            "Все поля должны быть заполнены!"
        )
        return

    new_quote = {
        "text": text,
        "author": author,
        "theme": theme
    }

    quotes.append(new_quote)

    update_filters()

    quote_entry.delete(0, tk.END)
    author_entry.delete(0, tk.END)
    theme_entry.delete(0, tk.END)

    messagebox.showinfo(
        "Успех",
        "Цитата добавлена!"
    )


def save_history():
    with open(JSON_FILE, "w", encoding="utf-8") as file:
        json.dump(history, file, ensure_ascii=False, indent=4)

    messagebox.showinfo(
        "Сохранено",
        "История сохранена!"
    )


def load_history():
    if not os.path.exists(JSON_FILE):
        return

    with open(JSON_FILE, "r", encoding="utf-8") as file:
        loaded_history = json.load(file)

    history.clear()
    history_listbox.delete(0, tk.END)

    for quote in loaded_history:
        history.append(quote)
        history_listbox.insert(
            tk.END,
            f'{quote["author"]}: {quote["text"]}'
        )


def update_filters():
    authors = ["Все"] + sorted(
        list(set(q["author"] for q in quotes))
    )

    themes = ["Все"] + sorted(
        list(set(q["theme"] for q in quotes))
    )

    author_combobox["values"] = authors
    theme_combobox["values"] = themes


# ---------- GUI ----------
root = tk.Tk()
root.title("Random Quote Generator")
root.geometry("700x600")

quote_text = tk.StringVar()
author_text = tk.StringVar()
theme_text = tk.StringVar()

# Заголовок
title_label = tk.Label(
    root,
    text="Генератор случайных цитат",
    font=("Arial", 18, "bold")
)
title_label.pack(pady=10)

# Фильтры
filter_frame = tk.Frame(root)
filter_frame.pack(pady=10)

tk.Label(filter_frame, text="Автор:").grid(row=0, column=0)

author_combobox = ttk.Combobox(
    filter_frame,
    state="readonly"
)
author_combobox.grid(row=0, column=1)

tk.Label(filter_frame, text="Тема:").grid(row=0, column=2)

theme_combobox = ttk.Combobox(
    filter_frame,
    state="readonly"
)
theme_combobox.grid(row=0, column=3)

update_filters()

author_combobox.set("Все")
theme_combobox.set("Все")

# Отображение цитаты
quote_label = tk.Label(
    root,
    textvariable=quote_text,
    wraplength=500,
    font=("Arial", 14),
    fg="blue"
)
quote_label.pack(pady=10)

author_label = tk.Label(
    root,
    textvariable=author_text,
    font=("Arial", 12)
)
author_label.pack()

theme_label = tk.Label(
    root,
    textvariable=theme_text,
    font=("Arial", 10)
)
theme_label.pack()

# Кнопка генерации
generate_button = tk.Button(
    root,
    text="Сгенерировать цитату",
    command=generate_quote,
    bg="lightgreen"
)
generate_button.pack(pady=10)

# История
tk.Label(
    root,
    text="История цитат:"
).pack()

history_listbox = tk.Listbox(
    root,
    width=80,
    height=10
)
history_listbox.pack(pady=5)

# Добавление новой цитаты
tk.Label(
    root,
    text="Добавить новую цитату"
).pack(pady=5)

quote_entry = tk.Entry(root, width=60)
quote_entry.pack()
quote_entry.insert(0, "Текст цитаты")

author_entry = tk.Entry(root, width=60)
author_entry.pack()
author_entry.insert(0, "Автор")

theme_entry = tk.Entry(root, width=60)
theme_entry.pack()
theme_entry.insert(0, "Тема")

add_button = tk.Button(
    root,
    text="Добавить цитату",
    command=add_quote,
    bg="lightblue"
)
add_button.pack(pady=10)

# Сохранение/загрузка
button_frame = tk.Frame(root)
button_frame.pack()

save_button = tk.Button(
    button_frame,
    text="Сохранить историю",
    command=save_history
)
save_button.grid(row=0, column=0, padx=5)

load_button = tk.Button(
    button_frame,
    text="Загрузить историю",
    command=load_history
)
load_button.grid(row=0, column=1, padx=5)

load_history()

root.mainloop()