import os
import tkinter as tk

class fileExplorer:

    def __init__(self, root, path, width, height, font):
        #root: where fileList is located
        #path is the inital path to display
        #width and height is the dimensions of the box in characters and lines
        #font is the font and size of the text e.g. ('Arial', 16)

        scroll = tk.Scrollbar(root, orient = tk.VERTICAL)
        scroll.grid(row = 1, column = 1, sticky = 'ns')

        self.fileList = tk.Listbox(root, width = width, height = height, yscrollcommand = scroll.set, font = font)
        self.fileList.grid(row = 1, column = 0)

        scroll.config(command = self.fileList.yview)

        self.fileList.bind("<Double-Button-1>", self.selection)

        self.root = root
        self.path = path
        self.selection = ''
        self.font = font
        self.listFiles()

    def listFiles(self):
        self.fileList.delete(0, tk.END)
        self.fileList.insert(tk.END, "++new file++")
        self.fileList.insert(tk.END, "---back---")
        os.chdir(self.path)
        for file in os.listdir(self.path):
            if os.path.isdir(file):
                self.fileList.insert(tk.END, str(file).replace('\n', '') + " (folder)")
            if not os.path.isdir(file):
                self.fileList.insert(tk.END, str(file).replace('\n', ''))

    def selection(self, event):
        item = self.fileList.get(tk.ACTIVE)
        self.selection = item
        if " (folder)" in item or item == "---back---" or item == "++new file++":
            self.changePath(event)

    def getSelection(self):
        return self.selection

    def changePath(self, event):
        if "++new file++" == self.fileList.get(tk.ACTIVE):
            self.newFile()
        if " (folder)" in self.fileList.get(tk.ACTIVE):
            #move forward
            folder = self.fileList.get(tk.ACTIVE)
            folder = folder.replace(" (folder)", '')
            newPath = self.path + '\\' + folder
            self.path = newPath

        if "---back---" == self.fileList.get(tk.ACTIVE):
            #move back
            slashPos = len(self.path)
            for i in range(len(self.path) -1, 0, -1):
                if self.path[i] == '\\': #find the position of the last \
                    slashPos = i
                    break
            self.path = self.path[0:slashPos]

        self.listFiles()

    def newFile(self):
        self.inputWindow = tk.Toplevel(self.root)
        self.inputWindow.focus_set()
        self.inputWindow.title("Enter Name")

        text = tk.Label(self.inputWindow, text = "File Name:", font = self.font)
        text.grid(row = 0, column = 0, pady = 10)

        self.entry = tk.Entry(self.inputWindow, font = self.font)
        self.entry.grid(row = 0, column = 1, pady = 10)

        acceptButton = tk.Button(self.inputWindow, text = 'Accept', font = self.font, command = self.makeFile)
        acceptButton.grid(row = 0, column = 2, pady = 10)

    def makeFile(self):
        filename = self.entry.get()
        file = open(filename, 'w')
        file.write('')
        file.close()
        self.inputWindow.destroy()
        self.listFiles()
