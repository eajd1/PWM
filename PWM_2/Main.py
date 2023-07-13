# Created: 19/01/2023
# Last Updated: 19/01/2023
# By Ethan Denis

import tkinter as tk
from tkinter import filedialog
from SMsg import SMsg
from random import randint
from getpass import getpass
from Edit import Edit

root = tk.Tk()
root.withdraw()
# Magic from the interwebs to fix the filedialog not showing
root.call('wm', 'attributes', '.', '-topmost', True)

global plainText
plainText = ''

def string_gen(digits):
    digits = int(digits)
    msg = []
    for i in range(0, digits):
        msg.append(chr(randint(33, 126)))
    msg = ''.join(msg)
    return msg

def print_msg(msg : str, title : str):
    if (input("Show " + title + "? (press enter for no) ")):
        print('')
        print(title)
        print("\\/")
        print(msg)
        print('/\\')

def open_file():
    filePath = filedialog.askopenfilename()

    try:
        file = open(filePath, 'r')
        text = file.read()
        file.close()
        print("Opened File: " + filePath)

        msg = SMsg(64)
        msg.load_text(text)

        print_msg(msg.get_formatted_cypher_text(), "Cypher Text")

        password = getpass("Enter Password: ")
        text = msg.decrypt(password)
        print_msg(text, "Decrypted Text")

        if (input("Save this text to memory? (press enter for no) ")):
            global plainText 
            plainText = text
    except:
        print("Failed to open file")

def new_file():
    text = ''
    if (input("Use loaded text? (press enter to enter new text) ")):
        text = plainText
    else:
        text = input("Message to encrypt:\n")

    print_msg(text, "Text to Encrypt")

    password = getpass("Enter Password: ")

    msg = SMsg(64)
    msg.encrypt(text, password)

    cypherText = msg.get_formatted_cypher_text()
    print_msg(cypherText, "Cypher Text")

    filePath = filedialog.asksaveasfilename()

    try:
        file = open(filePath, 'w')
        file.write(cypherText)
        file.close()
        print("Successfully Saved File to " + filePath)
    except:
        print("Failed to save file")

def append_file():
    filePath = filedialog.askopenfilename()

    try:
        file = open(filePath, 'r')
        text = file.read()
        file.close()
        print("Opened File: " + filePath)

        msg = SMsg(64)
        msg.load_text(text)

        password = getpass("Enter Password: ")
        text = msg.decrypt(password)
        print_msg(text, "Decrypted Text")

        appending = ''
        if (input("Use loaded text? (press enter to enter new text) ")):
            appending = plainText
        else:
            appending = "\n" + input("Enter text to append:\n")

        text += appending
        print_msg(text, "New Text")

        if (input("Save? (press enter for no) ")):
            password = getpass("Enter Password: ")
            msg.encrypt(text, password)
            print_msg(msg.get_formatted_cypher_text(), "Encrypted Text")

            filePath = filedialog.asksaveasfilename()
            try:
                file = open(filePath, 'w')
                file.write(msg.get_formatted_cypher_text())
                file.close()
                print("Successfully Saved File to " + filePath)
            except:
                print("Failed to save file")
    except:
        print("Failed to open file")

def load_text():
    filePath = filedialog.askopenfilename()

    try:
        file = open(filePath, 'r')
        text = file.read()
        file.close()
        print("Opened File: " + filePath)

        print_msg(text, "Loaded Text")
        
        if (input("Save this text to memory? (press enter for no) ")):
            global plainText 
            plainText = text
    except:
        print("Failed to open file")

def edit_file():
    filePath = filedialog.askopenfilename()

    try:
        file = open(filePath, 'r')
        text = file.read()
        file.close()
        print("Opened File: " + filePath)

        msg = SMsg(64)
        msg.load_text(text)

        password = getpass("Enter Password: ")
        text = msg.decrypt(password)
        print_msg(text, "Decrypted Text")
        
        edit = Edit(text)
        edit.edit_mode()
        text = edit.get_text()
        print_msg(text, "Edited Text")

        if (input("Save? (press enter for no) ")):
            password = getpass("Enter Password: ")
            msg.encrypt(text, password)
            print_msg(msg.get_formatted_cypher_text(), "Encrypted Text")

            filePath = filedialog.asksaveasfilename()
            try:
                file = open(filePath, 'w')
                file.write(msg.get_formatted_cypher_text())
                file.close()
                print("Successfully Saved File to " + filePath)
            except:
                print("Failed to save file")

    except:
        print("Failed to open file")


choice = input("""Open file / New File / Append File / Edit File /
Load Plain Text / Show Saved Text / Generate Password
(press enter to exit): """)
while (choice):

    match choice[0].lower():
        case 'o':
            open_file()
        
        case 'n':
            new_file()

        case 'a':
            append_file()

        case 'l':
            load_text()

        case 's':
            print_msg(plainText, "Text in Memory")

        case 'g':
            digits = input("How many digits: ")
            try:
                digits = int(digits)
                print_msg(string_gen(digits), "Generated String")
            except:
                print("Enter a number")

        case 'e':
            edit_file()
                
    choice = input("""Open file / New File / Append File / Edit File /
Load Plain Text / Show Saved Text / Generate Password
(press enter to exit): """)