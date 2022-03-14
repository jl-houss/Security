from tkinter import *
from src.controller import config

def center_window(w, h, window: Tk):
    ws = window.winfo_screenwidth()
    hs = window.winfo_screenheight()
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)
    window.geometry('%dx%d+%d+%d' % (w, h, x, y))


def clear(frame: Frame):
    for widget in frame.winfo_children():
        widget.destroy()


def click(event: Event, entries: dict, hide=""):
    leave_all(entries)
    entry = event.widget
    if not entry.get() or entry.get() == entries[entry]:
        entry.delete(0, 'end')
        entry.config(fg='black', show=hide)
    entry.focus()


def leave(entry: Entry, placeholder: str):
    if entry.get() == "":
        entry.delete(0, 'end')
        entry.insert(0, placeholder)
        entry.config(fg='grey', show="")


def leave_all(entries: dict):
    for entry in entries:
        leave(entry, entries[entry])
    config.app.focus()
