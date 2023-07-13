from random import randint
from os import remove
global msg
msg = ''
global loaded
loaded = False
from time import process_time

def key(password):
    password = list(password)
    for i in range(0, len(password)):
        password[i] = ord(password[i])
    key = 1
    for i in range(0, len(password)):
        key *= password[i]
    return key

def encrypthex():
    global loaded
    global msg
    if loaded == True:
        pass
    else:
        msg = input("Enter secure data: ")
    password = input("Enter password: ")
    passkey = key(password)
    msg = list(msg)
    for i in range(0, len(msg)):
        msg[i] = ord(msg[i])
    for i in range(0, len(msg)):
        msg[i] = msg[i]*passkey
        msg[i] = hex(msg[i])
        msg[i] = msg[i][2:]
        msg[i] = ' '+str(msg[i])
    data = ''.join(msg)
    data = data[1:]
    data = "H"+str(data)
    if input("Print? "):
        print(data)
    loaded = True
    msg = data
    try:
        if input("Save? "):
            file = open(input("File: "), "w")
            file.write(data)
            file.close()
    except:
        print("Invalid Filename")

def encryptnorm():
    global loaded
    global msg
    if loaded == True:
        pass
    else:
        msg = input("Enter secure data: ")
    password = input("Enter password: ")
    passkey = key(password)
    msg = list(msg)
    for i in range(0, len(msg)):
        msg[i] = ord(msg[i])
    for i in range(0, len(msg)):
        msg[i] = msg[i]*passkey
        msg[i] = (msg[i])
        msg[i] = ' '+str(msg[i])
    data = ''.join(msg)
    data = data[1:]
    if input("Print? "):
        print(data)
    loaded = True
    msg = data
    try:
        if input("Save? "):
            file = open(input("File: "), "w")
            file.write(data)
            file.close()
    except:
        print("Invalid Filename")

def encrypt():
    if input("hex? "):
        encrypthex()
    else:
        encryptnorm()

def decryptnorm():
    global loaded
    global msg
    try:
        password = input("Enter password: ")
        passkey = key(password)
        msg = msg.split()
        for i in range(0, len(msg)):
            msg[i] = int(msg[i])/passkey
            msg[i] = int(msg[i])
        for i in range(0, len(msg)):
            msg[i] = chr(msg[i])
        data = ''.join(msg)
        msg = data
        if input("Print? "):
            print(data)
    except:
        print("An error occured.")

def decrypthex():
    global loaded
    global msg
    try:
        password = input("Enter password: ")
        passkey = key(password)
        msg = msg[1:]
        msg = msg.split()
        for i in range(0, len(msg)):
            msg[i] = int(msg[i], 16)/passkey
            msg[i] = int(msg[i])
        for i in range(0, len(msg)):
            msg[i] = chr(msg[i])
        data = ''.join(msg)
        msg = data
        if input("Print? "):
            print(data)
    except:
        print("An error occured.")

def decrypt():
    global loaded
    global msg
    if loaded:
        pass
    elif input("Load? "):
        try:
            file = open(input("File: "), "r")
            msg = str(file.read())
            file.close()
        except:
            print("Invalid Filename")
    else:
        msg = input("Enter data: ")
    if msg[0].lower() == "h":
        decrypthex()
    else:
        decryptnorm()


def string_gen():
    global msg
    global loaded
    digits = int(input("How many digits: "))
    start = process_time()
    password = []
    for i in range(0, digits):
        password.append(chr(randint(33,126)))
    data = ''.join(password)
    msg = data
    loaded = True
    end = process_time()
    print(end-start)
    if input("Print? "):
        print(data)
    if input("Save? "):
        file = open(input("File: "), "w")
        file.write(data)
        file.close()

def number_gen():
    global msg
    global loaded
    digits = int(input("How many digits: "))
    number = []
    for i in range(0, digits):
        number.append(str(randint(0,10)))
    data = ''.join(number)
    msg = data
    loaded = True
    if input("Print? "):
        print(data)
    if input("Save? "):
        file = open(input("File: "), "w")
        file.write(data)
        file.close()

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

option = input()
option = option.lower()
while option:
    if option == "encrypt":
        encrypt()

    elif option == "decrypt":
        decrypt()

    elif option == "string":
        string_gen()

    elif option == "number":
        number_gen()

    elif option == "delete":
        try:
            remove(input("File: "))
        except:
            print("File not found")

    elif option == "load":
        try:
            load()
        except:
            print("File not found")

    elif option == "clear":
        msg = None
        loaded = False

    else:
        print("Nice try!")

    option = input()
