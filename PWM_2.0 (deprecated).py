import tkinter as tk
import os, hashlib, binascii
from tkinter import filedialog


def getKey(password : str):
    pin = "salt"
    key = hashlib.pbkdf2_hmac('sha512', password.encode() #binary preprestation of password
                             , pin.encode() #binary represtation of pin
                             , 200000) #number of iterations
    key = int(binascii.hexlify(key), 16) #make it a hex number
    return key

def encrypt(msg, password):
    key = getKey(password)
    arr = list(msg) #turn string into array of characters
    for i in range(0, len(arr)):
        arr[i] = ord(arr[i]) #turn characters into ascii integers
        arr[i] *= key #multiply the ascii value by the key
        arr[i] = hex(arr[i]) #make the integer hex
        arr[i] = str(arr[i])[2:] #removes the 0x at the start of a hex number
    msg = ''.join(arr) #turns array into string
    return msg

def decrypt(msg, password):
    key = getKey(password)
    arr = msg.split()
    for i in range(0, len(arr)):
        arr[i] = int(arr[i], 16) / key
        arr[i] = int(arr[i])
        arr[i] = chr(arr[i])
    msg = ''.join(arr)
    return msg

def load(filename):
    file = open(filename, 'r')
    msg = file.read()
    file.close()
    return msg

def save(filename, msg):
    file = open(filename, 'w')
    file.write(msg)
    file.close()

def makeNewFile(filename, password):
    msg = "True\n"
    msg = encrypt(msg, password)
    file = open(filename, 'w')
    file.write(msg)
    file.close()


class GUI:

    def __init__(self, root, width, height):
        self.root = root
        self.width = width
        self.height = height
        self.path = os.getcwd()
        self.file = ''
        self.password = ''
        self.newFile = False #if it is a new file
        self.showVar = False #whether or not to show the password
        self.mainUISetup()
        '''
    def fileSelectUI(self):
        self.fileWindow = tk.Toplevel(root, width = int(self.width/2), height = int(self.height/2))
        self.fileWindow.focus_set()
        self.fileWindow.protocol("WM_DELETE_WINDOW", self.root.destroy)
        self.fileWindow.title("Select File")

        text = tk.Label(self.fileWindow, text = "Please select file", font = ("Arial", 20))
        text.grid(row = 0, column = 0, columnspan = 2)

        fileList = fileExplorer(self.fileWindow, self.path, 50, 20, ('Arial', 16))

        self.fileWindow.bind("<Double-Button-1>", lambda event, var1 = fileList, var2 = text: self.selection(var1, var2))

    def selection(self, fileList, text):
        selection = fileList.getSelection()
        if selection == "++new file++":
            self.newFile = True
            text.config(text = "Select the created file")
        if not (" (folder)" in selection or selection == "---back---" or selection == "++new file++") and selection:
            self.file = selection
            self.getPassword()'''

    def getPassword(self):
        self.passwordWindow = tk.Toplevel(root, width = int(self.width/2), height = int(self.height/2))
        self.passwordWindow.focus_set()
        self.passwordWindow.title("Enter Password")

        text = tk.Label(self.passwordWindow, text = "Enter Password:", font = ("Arial", 20))
        text.grid(row = 0, column = 0, pady = 10)

        self.passEntry = tk.Entry(self.passwordWindow, font = ("Arial", 20), width = 20, show = '*')
        self.passEntry.grid(row = 0, column = 1, pady = 10)

        self.show = tk.Button(self.passwordWindow, text = 'Show', font = ("Arial", 16), width = 12, command = self.switchPassEntry)
        self.show.grid(row = 0, column = 2, pady = 10)

        accept = tk.Button(self.passwordWindow, text = 'Accept', font = ("Arial", 16), width = 12, command = self.testPassword)
        accept.grid(row = 0, column = 3, pady = 10)

    def testPassword(self):
        start = ''
        self.password = self.passEntry.get()
        if self.newFile == False:
            start = decrypt(load(self.file), self.password, '100').splitlines()[0].strip()
        if start == 'True':
            self.passwordWindow.destroy()
            self.fileWindow.destroy()
            self.mainUISetup()
        if self.newFile == True:
            makeNewFile(self.file, self.password)
            self.passwordWindow.destroy()
            self.fileWindow.destroy()
            self.mainUISetup()

    def switchPassEntry(self):
        if self.showVar == False:
            self.show.config(text = 'Hide')
            self.passEntry.config(show = '')
            self.showVar = True
        else:
            self.show.config(text = 'Show')
            self.passEntry.config(show = '*')
            self.showVar = False

    def mainUISetup(self):
        self.mainUI = tk.Toplevel(root, width = self.width, height = self.height)
        self.mainUI.focus_set()
        self.mainUI.protocol("WM_DELETE_WINDOW", self.root.destroy)
        self.mainUI.title("PWM")

        controls = tk.Frame(self.mainUI, width = self.width, height = int(self.height*0.2))
        controls.grid(row = 0, column = 0)

        displays = tk.Frame(self.mainUI, width = self.width, height = int(self.height*0.8))
        displays.grid(row = 1, column = 0)

        itemScroll = tk.Scrollbar(displays, orient = tk.VERTICAL)
        itemScroll.grid(row = 0, column = 1, sticky = 'ns')

        self.itemSelection = tk.Listbox(displays, width = 40, height = 30, yscrollcommand = itemScroll.set)
        self.itemSelection.grid(row = 0, column = 0)

        itemScroll.config(command = self.itemSelection.yview)

        displayScroll = tk.Scrollbar(displays, orient = tk.VERTICAL)
        displayScroll.grid(row = 0, column = 3, sticky = 'ns')

        self.display = tk.Text(displays, width = 120, height = 30, yscrollcommand = displayScroll.set)
        self.display.grid(row = 0, column = 2)

        displayScroll.config(command = self.display.yview)

        openButton = tk.Button(controls, text = 'Open', width = 12, cursor = 'hand2', command = self.fileSelect)
        openButton.grid(row = 0, column = 0)

        newButton = tk.Button(controls, text = 'New', width = 12, cursor = 'hand2', command = self.makeNewFile)
        newButton.grid(row = 1, column = 0)

        encryptButton = tk.Button(controls, text = 'Encrypt', width = 12, cursor = 'hand2', command = self.encrypt)
        encryptButton.grid(row = 0, column = 1)

    def fileSelect(self):
        self.file = filedialog.askopenfilename(initialdir = self.path, title = 'Select File',
                                               filetypes = (("Text", "*.txt"), ("All Files", "*.*")))

    def makeNewFile(self):
        self.createFileWindow = tk.Toplevel(root, width = int(self.width/2), height = int(self.height/2))
        self.createFileWindow.focus_set()
        self.createFileWindow.title("New File")

        label = tk.Label(self.createFileWindow, text = "File Name:", font = ("Arial", 16))
        label.grid(row = 0, column = 0, pady = 6)

        newFileEntry = tk.Entry(self.createFileWindow, width = 20, font = ("Arial", 16))
        newFileEntry.grid(row = 0, column = 1, pady = 6)

        otherLabel = tk.Label(self.createFileWindow, text = "Password:", font = ("Arial", 16))
        otherLabel.grid(row = 1, column = 0, pady = 6)

        newPasswordEntry = tk.Entry(self.createFileWindow, width = 20, font = ("Arial", 16))
        newPasswordEntry.grid(row = 1, column = 1, pady = 6)

        accept = tk.Button(self.createFileWindow, text = "Accept", font = ("Arial", 12), command = lambda: self.acceptNewFile(newFileEntry, newPasswordEntry))
        accept.grid(row = 2, column = 2, pady = 4, padx = 6)

        cancel = tk.Button(self.createFileWindow, text = "Cancel", font = ("Arial", 12), command = self.createFileWindow.destroy)
        cancel.grid(row = 2, column = 0, pady = 4, padx = 6)

    def acceptNewFile(self, fileEntry, passwordEntry):
        filename = fileEntry.get()
        password = passwordEntry.get()
        makeNewFile(filename, password)
        self.createFileWindow.destroy()

    def encrypt(self):
        msg = self.display.get('1.0', tk.END)
        password = self.password
        ## TODO:

root = tk.Tk()
width = 1366
height = 720
root.withdraw()
p = GUI(root, width, height)
root.mainloop()
