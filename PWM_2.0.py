import tkinter as tk
import os
from tkinter import filedialog
from Depedencies import Msg, DataEntry

msg = Msg("Hello World")
print(msg.getMsg())
msg.encrypt("test")
print(msg.getMsg())
msg.decrypt("test")
print(msg.getMsg())

root = tk.Tk()
root.title("PWM")
app = DataEntry(root, 0, True, "test data", None, None)
root.mainloop()
