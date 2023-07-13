import tkinter as tk
from random import randint
from os import remove
global msg
msg = ''
global loaded
loaded = False
global password
password = ''
global boolhex
boolhex = True
global filename
filename = ''
global datashown
datashown = False
global passshown
passshown = False

def key():
    global password
    temppassword = password
    temppassword = list(temppassword)
    for i in range(0, len(temppassword)):
        temppassword[i] = ord(temppassword[i])
    key = 1
    for i in range(0, len(temppassword)):
        key *= temppassword[i]
    return key

def encrypthex():
    global loaded
    global msg
    global display
    passkey = key()
    msg = list(msg)
    for i in range(0, len(msg)):
        msg[i] = ord(msg[i])
    for i in range(0, len(msg)):
        print("1:"+str(msg[i]))
        msg[i] = msg[i]*passkey
        print("2:"+str(msg[i]))
        msg[i] = hex(msg[i])
        print("3:"+str(msg[i]))
        msg[i] = msg[i][2:]
        print("4:"+str(msg[i]))
        msg[i] = ' '+str(msg[i])
        print("5:"+str(msg[i]))
    print(msg)
    data = ''.join(msg)
    print("7:"+str(data))
    data = data[1:]
    data = "H"+str(data)
    loaded = True
    msg = data
    update()

def encryptnorm():
    global loaded
    global msg
    global display
    passkey = key()
    msg = list(msg)
    for i in range(0, len(msg)):
        msg[i] = ord(msg[i])
    for i in range(0, len(msg)):
        msg[i] = msg[i]*passkey
        msg[i] = ' '+str(msg[i])
    data = ''.join(msg)
    data = data[1:]
    loaded = True
    msg = data
    update()

def encrypt():
    global boolhex
    if boolhex:
        encrypthex()
    else:
        encryptnorm()

def decryptnorm():
    global loaded
    global msg
    global display
    passkey = key()
    msg = msg.split()
    for i in range(0, len(msg)):
        msg[i] = int(msg[i])/passkey
        msg[i] = int(msg[i])
    for i in range(0, len(msg)):
        msg[i] = chr(msg[i])
    data = ''.join(msg)
    msg = data
    update()

def decrypthex():
    global loaded
    global msg
    global display
    passkey = key()
    msg = msg[1:]
    msg = msg.split()
    for i in range(0, len(msg)):
        msg[i] = int(msg[i], 16)/passkey
        msg[i] = int(msg[i])
    for i in range(0, len(msg)):
        msg[i] = chr(msg[i])
    data = ''.join(msg)
    msg = data
    update()

def decrypt():
    global msg
    if msg[0].lower() == "h":
        decrypthex()
    else:
        decryptnorm()

def string_gen():
    global msg
    digits = get_digits()
    password = []
    for i in range(0, digits):
        password.append(chr(randint(33,126)))
    data = ''.join(password)
    msg = data
    update()
    root.focus_set()

def number_gen():
    global msg
    digits = get_digits()
    number = []
    for i in range(0, digits):
        number.append(str(randint(0,10)))
    data = ''.join(number)
    msg = data
    update()
    root.focus_set()

def get_digits():
    global digit_entry
    digits = digit_entry.get()
    digits = int(digits)
    return digits

def load():
    global loaded
    file = open(input("File: "), "r")
    data = file.read()
    file.close()
    global msg
    msg = data
    loaded = True
    if input("Print? "):
        print(data)

def dataget():
    global data_entry
    global msg
    msg = data_entry.get()
    root.focus_set()
    update()

def passget():
    global pass_entry
    global password
    password = pass_entry.get()
    root.focus_set()
    update()

def changehex():
    global boolhex
    boolhex = not boolhex
    update()

def update():
    global boolhex
    global display
    global msg
    global hex_button
    if boolhex:
        hex_button.config(bg='green')
    else:
        hex_button.config(bg='red')
    display.delete('1.0', float(len(display.get('1.0', '2.0'))))
    display.insert('1.0', msg)

def save():
    global msg
    global filename
    get_filename()
    file = open(filename, 'w')
    file.write(msg)
    file.close()
    update()

def load():
    global msg
    global filename
    get_filename()
    file = open(filename, 'r')
    msg = str(file.read())
    file.close()
    update()

def get_filename():
    global file_entry
    global filename
    filename = file_entry.get()
    root.focus_set()

def delete():
    global msg
    global filename
    get_filename()
    remove(filename)
    update()

def clear():
    global msg
    global password
    global filename
    global data_entry
    global pass_entry
    global file_entry
    global digit_entry
    global display
    msg = ''
    password = ''
    filename = ''
    data_entry.delete(0,len(data_entry.get()))
    pass_entry.delete(0,len(pass_entry.get()))
    file_entry.delete(0,len(file_entry.get()))
    digit_entry.delete(0,len(digit_entry.get()))
    display.delete('1.0','3.0')
    update()
    root.focus_set()

def datashow():
    global data_entry
    global datashown
    if datashown:
        data_entry.config(show = '*')
        datashown = False
    else:
        data_entry.config(show = '')
        datashown = True

def passshow():
    global pass_entry
    global passshown
    if passshown:
        pass_entry.config(show = '*')
        passshown = False
    else:
        pass_entry.config(show = '')
        passshown = True

root = tk.Tk()
root.title("UI")

buttonframe = tk.Frame(root)
buttonframe.grid(row = 0, column = 0, columnspan = 5)

global display
display = tk.Text(root, width = 100, height = 50)
display.grid(row = 4, column = 0)

label1 = tk.Label(buttonframe, text = "Data:")
label1.grid(row = 0, column = 0)

global data_entry
data_entry = tk.Entry(buttonframe, show = "*")
data_entry.grid(row = 0, column = 1)

Data_accept = tk.Button(buttonframe, text = "Accept", command = dataget, cursor = 'hand2')
Data_accept.grid(row = 0, column = 2)

data_show = tk.Button(buttonframe, text = "Show", command = datashow, cursor = 'hand2')
data_show.grid(row = 0, column = 4)

label2 = tk.Label(buttonframe, text = "Password:")
label2.grid(row = 1, column = 0)

global pass_entry
pass_entry = tk.Entry(buttonframe, show = "*")
pass_entry.grid(row = 1, column = 1)

pass_accept = tk.Button(buttonframe, text = "Accept", command = passget, cursor = 'hand2')
pass_accept.grid(row = 1, column = 2)

pass_show = tk.Button(buttonframe, text = "Show", command = passshow, cursor = 'hand2')
pass_show.grid(row = 1, column = 4)

encrypt_button = tk.Button(buttonframe, text = "Encrypt", command = encrypt, cursor = 'hand2')
encrypt_button.grid(row = 0, column = 3)

hex_button = tk.Button(buttonframe, text = "Hex", command = changehex,
                       cursor = 'hand2', bg = 'green')
hex_button.grid(row = 4, column = 3)

decrypt_button = tk.Button(buttonframe, text = "Decrypt", command = decrypt, cursor = 'hand2')
decrypt_button.grid(row = 1, column = 3)

file_label = tk.Label(buttonframe, text = "Filename:")
file_label.grid(row = 2, column = 0)

global file_entry
file_entry = tk.Entry(buttonframe)
file_entry.grid(row = 2, column = 1)

save_button = tk.Button(buttonframe, text = "Save", command = save, cursor = 'hand2')
save_button.grid(row = 2, column = 2)

load_button = tk.Button(buttonframe, text = "Load", command = load, cursor = 'hand2')
load_button.grid(row = 2, column = 3)

clear_button = tk.Button(buttonframe, text = "Clear", command = clear, cursor = 'hand2')
clear_button.grid(row = 4, column = 2)

digit_label = tk.Label(buttonframe, text = "Digits:",)
digit_label.grid(row = 3, column = 0)

global digit_entry
digit_entry = tk.Entry(buttonframe)
digit_entry.grid(row = 3, column = 1)

string_button = tk.Button(buttonframe, text = "String", command = string_gen, cursor = 'hand2')
string_button.grid(row = 3, column = 3)

number_button = tk.Button(buttonframe, text = "Number", command = number_gen, cursor = 'hand2')
number_button.grid(row = 3, column = 2)

remove_button = tk.Button(buttonframe, text = "Delete", command = delete, cursor = 'hand2')
remove_button.grid(row = 2, column = 4)

root.mainloop()
