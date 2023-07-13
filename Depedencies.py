import hashlib, binascii, os
import tkinter as tk

class Msg:

    def __init__(self, msg):
        self.msg = msg
        self.encrypted = 0

    def getMsg(self):
        return self.msg

    def getKey(self, password : str): #make sure password is a str
        pin = "salt"
        key = hashlib.pbkdf2_hmac('sha512', password.encode(), #binary preprestation of password
                                  pin.encode(), #binary represtation of pin
                                  200000) #number of iterations
        key = int(binascii.hexlify(key), 16) #make it a hex number
        return key

    def encrypt(self, password):
        key = self.getKey(password)
        arr = list(self.msg) #turn string into array of characters
        for i in range(0, len(arr)):
            arr[i] = ord(arr[i]) #turn characters into ascii integers
            arr[i] *= key #multiply the ascii value by the key
            arr[i] = hex(arr[i]) #make the integer hex
        self.msg = ''.join(arr) #turns array into string
        self.encrypted += 1

    def decrypt(self, password):
        if self.encrypted > 0:
            key = self.getKey(password)
            arr = self.msg.split('0x')
            for i in range(1, len(arr)):
                arr[i] = int(arr[i], 16) / key
                arr[i] = int(arr[i])
                arr[i] = chr(arr[i])
            self.msg = ''.join(arr)
            self.encrypted -= 1

class DataEntry:

    def __init__(self, master, row, new, string, name, data):
        # new is whether to make a new object or load one
        # string is the string to load from if not new
        self.master = master
        if new:
            self.name = name
            self.data = data
        else:
            self.data = Msg('')
            fromString(string)

        width = 30
        height = 4

        self.frame = tk.Frame(master)
        self.frame.grid(row = row, column = 0)

        self.label = tk.Label(self.frame, text = self.name, font = ('Arial', 16))
        self.label.grid(row = 0, column = 0)

        self.display = tk.Text(self.frame, width = width, height = height, font = ('Arial', 12))
        self.display.grid(row = 0, column = 1, padx = 5, pady = 5)
        self.display.insert(tk.END, self.data.getMsg())

    def toString(self): #for saving to file
        string = self.name + ' ' + self.data + 'X'
        return string

    def fromString(self, string): #for loading from file
        string = string.split(' ')
        self.name = string[0]
        self.data = Msg(string[1])

    def setName(self, name):
        self.name = name
        self.label.config(text = self.name)

    def setData(self, data):
        self.data = data
        self.display.delete(tk.START, tk.END)
        self.display.insert(tk.END, self.data.getMsg())
