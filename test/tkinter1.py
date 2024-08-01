import tkinter as tk
from tkinter import messagebox

def on_open():
    messagebox.showinfo("Menu", "Open clicked")

def on_save():
    messagebox.showinfo("Menu", "Save clicked")

def on_exit():
    root.quit()

root = tk.Tk()
root.title("Tkinter Menu Example")

menu = tk.Menu(root)
root.config(menu=menu)

file_menu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Open", command=on_open)
file_menu.add_command(label="Save", command=on_save)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=on_exit)

root.mainloop()
