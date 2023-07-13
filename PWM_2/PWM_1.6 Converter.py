from random import randint
import hashlib, binascii

import tkinter as tk
from tkinter import filedialog
from SMsg import SMsg

def NewEncryption(msg, password):
    text = SMsg(64)
    text.encrypt(msg, password)
    return text.get_formatted_cypher_text()

def encrypting(msg, password, pin):
    passkey = hashlib.pbkdf2_hmac('sha512', str.encode(password), pin.encode(), 10000)
    passkey = int(binascii.hexlify(passkey),16)
    msg = list(msg)
    for i in range(0, len(msg)):
        msg[i] = ord(msg[i])
    for i in range(0, len(msg)):
        msg[i] = msg[i]*passkey
        msg[i] = hex(msg[i])
        msg[i] = msg[i][2:]
        msg[i] = ' '+ str(msg[i])
    msg = ''.join(msg)
    msg = msg[1:] #Gets rid of a space at the start
    return msg

def decrypting(msg, password, pin):
    passkey = hashlib.pbkdf2_hmac('sha512', str .encode(password), pin.encode(), 10000)
    passkey = int(binascii.hexlify(passkey),16)
    msg = msg.split()
    for i in range(0, len(msg)):
        msg[i] = int(msg[i], 16)/passkey
        msg[i] = int(msg[i])
    for i in range(0, len(msg)):
        msg[i] = chr(msg[i])
    msg = ''.join(msg)
    return msg

root = tk.Tk()
root.withdraw()

filePath = filedialog.askopenfilename()

file = open(filePath, 'r')
text = file.read()
file.close()

print(filePath)
password = input("Password: ")
pin = input("Pin: ")

plainText = decrypting(text, password, pin)
# Remove trailing new lines
while (plainText[-1] == '\n'):
    plainText = plainText[:-1]
print(plainText)

password = input("New Password: ")

msg = SMsg(64)
msg.encrypt(plainText, password)
cypherText = msg.get_formatted_cypher_text()

filePath = filePath[:-4] # remove .txt
filePath += "NEW.txt"
print(filePath)

file = open(filePath, 'w')
file.write(cypherText)
file.close()

print("------ Testing ------")

file = open(filePath, 'r')
text = file.read()
file.close()

msg.load_text(text)

password = input("Reenter Password: ")
print(msg.decrypt(password))