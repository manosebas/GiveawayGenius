import tkinter as tk

def log_message(text_log, message):
    text_log.insert(tk.END, message + '\n')
    text_log.see(tk.END)
