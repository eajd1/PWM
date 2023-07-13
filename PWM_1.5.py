#Current Version 09/jan/2020
#First Version late 2018
#By Ethan Denis

import tkinter as tk
from random import randint
import os, hashlib, binascii, smtplib, ssl

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

def save_msg(msg, filename):
    file = open(filename, 'w')
    file.write(msg)
    file.close()

def load_msg(filename):
    file = open(filename, 'r')
    msg = file.read()
    file.close()
    return msg

def string_gen(digits):
    digits = int(digits)
    msg = []
    for i in range(0, digits):
        msg.append(chr(randint(33, 126)))
    msg = ''.join(msg)
    return msg

def number_gen(digits):
    digits = int(digits)
    msg = []
    for i in range(0, digits):
        msg.append(str(randint(0,10)))
    msg = ''.join(msg)
    return msg


class PWM:

    def __init__(self, master):
        self.master = master

        self.input_frame = tk.Frame(master)
        self.input_frame.grid(row = 0, column = 0)

        self.output_frame = tk.Frame(master)
        self.output_frame.grid(row = 1, column = 0)

        self.display_scroll = tk.Scrollbar(self.output_frame, orient = tk.VERTICAL)
        self.display_scroll.grid(row = 0, column = 1, sticky = 'ns')

        self.display = tk.Text(self.output_frame, width = 100, height = 30, yscrollcommand = self.display_scroll.set, font = ('Arial'))
        self.display.grid(row = 0, column = 0, sticky = 'ns')

        self.display_scroll.config(command = self.display.yview)

        self.pass_label = tk.Label(self.input_frame, text = 'Password:')
        self.pass_label.grid(row = 0, column = 0)

        self.pass_entry = tk.Entry(self.input_frame, show = '*', width = 40)
        self.pass_entry.grid(row = 0, column = 1, columnspan = 3)

        self.pass_show = tk.Button(self.input_frame, text = "Show",
                                   command = self.show_password,
                                   cursor = 'hand2',
                                   width = 10)
        self.pass_show.grid(row = 0, column = 6)

        self.pass_hide = tk.Button(self.input_frame, text = "Hide",
                                   command = self.hide_password,
                                   cursor = 'hand2',
                                   width = 10)
        self.pass_hide.grid(row = 0, column = 7)

        self.encrypt_button = tk.Button(self.input_frame, text = 'Encrypt',
                                        command = self.encrypt,
                                        cursor = 'hand2',
                                        width = 10)
        self.encrypt_button.grid(row = 0, column = 4)

        self.decrypt_button = tk.Button(self.input_frame, text = 'Decrypt',
                                        command = self.decrypt,
                                        cursor = 'hand2',
                                        width = 10)
        self.decrypt_button.grid(row = 0, column = 5)

        self.file_label = tk.Label(self.input_frame, text = 'Filename:')
        self.file_label.grid(row = 1, column = 0)

        self.file_var = tk.StringVar(master, value = '')

        self.file_entry = tk.Entry(self.input_frame, width = 40, textvariable = self.file_var)
        self.file_entry.grid(row = 1, column = 1, columnspan = 3)

        self.save_button = tk.Button(self.input_frame, text = 'Save',
                                     command = self.save_msg_b,
                                     cursor = 'hand2',
                                     width = 10)
        self.save_button.grid(row = 1, column = 4)

        self.load_button = tk.Button(self.input_frame, text = 'Load',
                                     command = self.load_msg_b,
                                     cursor = 'hand2',
                                     width = 10)
        self.load_button.grid(row = 1, column = 5)

        self.digit_label = tk.Label(self.input_frame, text = 'Digits:')
        self.digit_label.grid(row = 2, column = 0)

        self.digit_entry = tk.Entry(self.input_frame, width = 13)
        self.digit_entry.grid(row = 2, column = 1)

        self.string_button = tk.Button(self.input_frame, text = 'String',
                                       command = self.string_gen_b,
                                       cursor = 'hand2',
                                       width = 10)
        self.string_button.grid(row = 2, column = 2)

        self.number_button = tk.Button(self.input_frame, text = 'Number',
                                       command = self.number_gen_b,
                                       cursor = 'hand2',
                                       width = 10)
        self.number_button.grid(row = 2, column = 3)

        self.clear_button = tk.Button(self.input_frame, text = 'Clear',
                                      command = self.clear_b,
                                      cursor = 'hand2',
                                      width = 10)
        self.clear_button.grid(row = 1, column = 6)

        self.remove_button = tk.Button(self.input_frame, text = 'Remove',
                                       command = self.remove_b,
                                       cursor = 'hand2',
                                       width = 10)
        self.remove_button.grid(row = 1, column = 7)

        self.pin_label = tk.Label(self.input_frame, text = 'Pin:')
        self.pin_label.grid(row = 2, column = 4)

        self.pin_entry = tk.Entry(self.input_frame, width = 12, show = '*')
        self.pin_entry.grid(row = 2, column = 5)

        self.send = tk.Button(self.input_frame, text = 'Send', width = 10,
                              command = self.email_details, cursor = 'hand2')
        self.send.grid(row = 2, column = 7)

        #Optional Files Display
        self.file_display_scroll = tk.Scrollbar(self.output_frame, orient = tk.VERTICAL)
        self.file_display_scroll.grid(row = 0, column = 3, sticky = 'ns')

        self.file_display = tk.Listbox(self.output_frame, width = 50, height = 34, yscrollcommand = self.file_display_scroll.set)
        self.file_display.grid(row = 0, column = 2, sticky = 'ns')

        self.file_display_scroll.config(command = self.file_display.yview)

        self.file_list_button = tk.Button(self.input_frame, text = 'List Files',
                                   command = self.list_files,
                                   cursor = 'hand2',
                                   width = 10)
        self.file_list_button.grid(row = 0, column = 14)

        self.path_label = tk.Label(self.input_frame, text = 'Path to Display:')
        self.path_label.grid(row = 0, column = 8)

        default_path = os.getcwd()
        self.path_var = tk.StringVar(master, value = default_path)
        self.make_var = tk.StringVar(master, value = '')

        self.path_entry = tk.Entry(self.input_frame, width = 54, textvariable = self.path_var)
        self.path_entry.grid(row = 0, column = 9, columnspan = 5)

        self.create_dir_button = tk.Button(self.input_frame, width = 16, text = 'Make Directory',
                                           command = self.create_dir, cursor = 'hand2')
        self.create_dir_button.grid(row = 1, column = 10)

        self.remove_dir_button = tk.Button(self.input_frame, width = 16, text = 'Remove Directory',
                                           command = self.remove_dir_check, cursor = 'hand2')
        self.remove_dir_button.grid(row = 1, column = 11, columnspan = 3)

        self.path_make_entry = tk.Entry(self.input_frame, width = 42, textvariable = self.make_var)
        self.path_make_entry.grid(row = 2, column = 9, columnspan = 3)

        self.path_make_label = tk.Label(self.input_frame, text = 'Path to Make:')
        self.path_make_label.grid(row = 2, column = 8)

        self.back_folder = tk.Button(self.input_frame, text = 'Backward', width = 10,
                                     command = self.go_back, cursor = 'hand2')
        self.back_folder.grid(row = 1, column = 14)

        self.files_var = tk.BooleanVar()
        self.files_var.set(True)
        self.check_all_files = tk.Checkbutton(self.input_frame, text = 'All files?',
                                              variable = self.files_var,
                                              command = self.list_files)
        self.check_all_files.grid(row = 1, column = 9)

        self.list_files()

        #Bindings
        self.pass_entry.bind("<Return>", self.encrypt_event)
        self.pass_entry.bind("<Shift-Return>", self.decrypt_event)
        self.pass_entry.bind("<Escape>", self.reset_focus)

        self.file_entry.bind("<Return>", self.load_msg_event)
        self.file_entry.bind("<Shift-Return>", self.save_msg_event)
        self.file_entry.bind("<Escape>", self.reset_focus)

        self.digit_entry.bind("<Return>", self.string_gen_event)
        self.digit_entry.bind("<Shift-Return>", self.number_gen_event)
        self.digit_entry.bind("<Escape>", self.reset_focus)

        self.path_entry.bind("<Return>", self.list_files_event)
        self.path_entry.bind("<Escape>", self.reset_focus)

        self.path_make_entry.bind("<Return>", self.create_dir_event)
        self.path_make_entry.bind("<Shift-Return>", self.remove_dir_check_event)
        self.path_make_entry.bind("<Escape>", self.reset_focus)

        self.file_display.bind("<Double-Button-1>", self.set_file)
        self.file_display.bind("<Return>", self.set_file)
        self.master.bind("<Escape>",self.go_back_event)

    def reset_focus(self, event):
        self.master.focus_set()

    def encrypt(self):
        msg = self.display.get('1.0',tk.END)
        password = self.pass_entry.get()
        pin = self.pin_entry.get()
        self.msg = encrypting(msg, password, pin)
        if len(self.msg) > 10000:
            newmsg = self.msg[:10000]+'...'
        else:
            newmsg = self.msg
        self.display.delete('1.0',tk.END)
        self.display.insert(tk.END, newmsg)
        root.focus_set()

    def encrypt_event(self, event):
        msg = self.display.get('1.0',tk.END)
        password = self.pass_entry.get()
        pin = self.pin_entry.get()
        self.msg = encrypting(msg, password, pin)
        if len(self.msg) > 10000:
            newmsg = self.msg[:10000]+'...'
        else:
            newmsg = self.msg
        self.display.delete('1.0',tk.END)
        self.display.insert(tk.END, newmsg)

    def decrypt(self):
        password = self.pass_entry.get()
        pin = self.pin_entry.get()
        newmsg = decrypting(self.msg, password, pin)
        self.display.delete('1.0',tk.END)
        self.display.insert(tk.END, newmsg)
        root.focus_set()

    def decrypt_event(self, event):
        password = self.pass_entry.get()
        pin = self.pin_entry.get()
        newmsg = decrypting(self.msg, password, pin)
        self.display.delete('1.0',tk.END)
        self.display.insert(tk.END, newmsg)

    def show_password(self):
        self.pass_entry.config(show = '')
        self.pin_entry.config(show = '')

    def hide_password(self):
        self.pass_entry.config(show = '*')
        self.pin_entry.config(show = '*')

    def save_msg_event(self, event):
        if self.file_entry.get() in os.listdir(self.path_entry.get()):
            self.confirm_window = tk.Toplevel(root)
            self.confirm_window.focus_set()
            self.confirm_window.bind("<Return>", self.save_msg_accept)
            text = tk.Label(self.confirm_window, text = 'File already exists, are you sure you want to overwrite?')
            text.grid(row = 0, column = 0, columnspan = 2)
            yes = tk.Button(self.confirm_window, text = 'Yes', command = self.save_msg,
                            cursor = 'hand2', width = '10')
            yes.grid(row = 1, column = 0)
            no = tk.Button(self.confirm_window, text = 'No', command = self.close_window,
                            cursor = 'hand2', width = '10')
            no.grid(row = 1, column = 1)
        else:
            self.save_msg()

    def save_msg_b(self):
        if self.file_entry.get() in os.listdir(self.path_entry.get()):
            self.confirm_window = tk.Toplevel(root)
            self.confirm_window.focus_set()
            self.confirm_window.bind("<Return>", self.save_msg_accept)
            text = tk.Label(self.confirm_window, text = 'File already exists, are you sure you want to overwrite?')
            text.grid(row = 0, column = 0, columnspan = 2)
            yes = tk.Button(self.confirm_window, text = 'Yes', command = self.save_msg,
                            cursor = 'hand2', width = '10')
            yes.grid(row = 1, column = 0)
            no = tk.Button(self.confirm_window, text = 'No', command = self.close_window,
                            cursor = 'hand2', width = '10')
            no.grid(row = 1, column = 1)
        else:
            self.save_msg()

    def save_msg_accept(self, event):
        msg = self.display.get('1.0',tk.END)
        filename = self.file_entry.get()
        save_msg(msg, filename)
        root.focus_set()
        self.list_files()
        self.confirm_window.destroy()

    def save_msg(self):
        filename = self.file_entry.get()
        save_msg(self.msg, filename)
        root.focus_set()
        self.list_files()
        try:
            self.confirm_window.destroy()
        except:
            pass

    def load_msg_b(self):
        filename = self.file_entry.get()
        self.msg = load_msg(filename)
        self.display.delete('1.0',tk.END)
        if len(self.msg) > 10000:
            msg = self.msg[:10000]+'...'
        else:
            msg = self.msg
        self.display.insert(tk.END, msg)
        root.focus_set()
        self.list_files()
        if self.pass_entry.get() and self.pin_entry.get():
            self.decrypt()

    def load_msg_event(self, event):
        filename = self.file_entry.get()
        self.msg = load_msg(filename)
        self.display.delete('1.0',tk.END)
        if len(self.msg) > 10000:
            msg = self.msg[:10000]+'...'
        else:
            msg = self.msg
        self.display.insert(tk.END, msg)
        root.focus_set()
        self.list_files()
        if self.pass_entry.get() and self.pin_entry.get():
            self.decrypt()

    def string_gen_b(self):
        digits = self.digit_entry.get()
        string = string_gen(digits)
        self.display.delete('1.0',tk.END)
        self.display.insert(tk.END, string)
        root.focus_set()

    def string_gen_event(self, event):
        digits = self.digit_entry.get()
        string = string_gen(digits)
        self.display.delete('1.0',tk.END)
        self.display.insert(tk.END, string)

    def number_gen_b(self):
        digits = self.digit_entry.get()
        num = number_gen(digits)
        self.display.delete('1.0',tk.END)
        self.display.insert(tk.END, num)
        root.focus_set()

    def number_gen_event(self, event):
        digits = self.digit_entry.get()
        num = number_gen(digits)
        self.display.delete('1.0',tk.END)
        self.display.insert(tk.END, num)

    def clear_b(self):
        self.display.delete('1.0',tk.END)
        self.pass_entry.delete(0, len(self.pass_entry.get()))
        self.file_entry.delete(0, len(self.file_entry.get()))
        self.digit_entry.delete(0, len(self.digit_entry.get()))
        self.pin_entry.delete(0, len(self.pin_entry.get()))
        root.focus_set()

    def remove_b(self):
        self.confirm_window = tk.Toplevel(root)
        self.confirm_window.focus_set()
        self.confirm_window.bind("<Return>", self.remove_file_event)

        text = tk.Label(self.confirm_window, text = 'Are you sure you want to remove the file?')
        text.grid(row = 0, column = 0, columnspan = 2)

        yes = tk.Button(self.confirm_window, text = 'Yes', command = self.remove_file,
                        cursor = 'hand2', width = '10')
        yes.grid(row = 1, column = 0)

        no = tk.Button(self.confirm_window, text = 'No', command = self.close_window,
                        cursor = 'hand2', width = '10')
        no.grid(row = 1, column = 1)

    def remove_file_event(self, event):
        filename = self.file_entry.get()
        os.remove(filename)
        root.focus_set()
        self.list_files()
        self.confirm_window.destroy()

    def remove_file(self):
        filename = self.file_entry.get()
        os.remove(filename)
        root.focus_set()
        self.list_files()
        self.confirm_window.destroy()

    def list_files(self):
        self.master.focus_set()
        files = []
        path = self.path_entry.get()
        os.chdir(path)

        for file in os.listdir(path):
            files.append(file)
        if self.files_var.get():
            self.list_all_files(files)
        else:
            self.list_default_files(files)

    def list_files_event(self, event):
        files = []
        path = self.path_entry.get()
        os.chdir(path)

        for file in os.listdir(path):
            files.append(file)
        if self.files_var.get():
            self.list_all_files(files)
        else:
            self.list_default_files(files)

    def list_default_files(self, files):
        self.file_display.delete(0,tk.END)
        total = 1
        for i in range(0, len(files)):
            if os.path.isdir(files[i].replace('\n','')):
                self.file_display.insert(tk.END, u'\u2220 '+files[i])
                total += 1
        for i in range(0, len(files)):
            if '.txt' in files[i] or '.' not in files[i] and not os.path.isdir(files[i].replace('\n','')):
                self.file_display.insert(tk.END, files[i])

    def list_all_files(self, files):
        self.file_display.delete(0,tk.END)
        total = 1
        for i in range(0, len(files)):
            if os.path.isdir(files[i].replace('\n','')):
                self.file_display.insert(tk.END, u'\u2220 '+files[i])
                total += 1
        for i in range(0, len(files)):
            if not os.path.isdir(files[i].replace('\n','')):
                self.file_display.insert(tk.END, files[i])

    def set_file(self, event):
        if '\u2220' in self.file_display.get(tk.ACTIVE):
            self.forward_folder()
        else:
            self.file_var.set(self.file_display.get(tk.ACTIVE))
            self.load_msg_b()

    def set_file_b(self):
        if '\u2220' in self.file_display.get(tk.ACTIVE):
            self.forward_folder()
        else:
            self.file_var.set(self.file_display.get(tk.ACTIVE))
            self.load_msg_b()

    def forward_folder(self):
        path = str(self.path_entry.get())
        folder = self.file_display.get(tk.ACTIVE)
        folder = folder[2:]
        newpath = path+'\\'+folder
        self.path_var.set(newpath)
        self.list_files()

    def create_dir(self):
        base_path = self.path_entry.get()
        os.makedirs(base_path+self.path_make_entry.get())
        self.list_files()

    def create_dir_event(self, event):
        base_path = self.path_entry.get()
        os.makedirs(base_path+self.path_make_entry.get())
        self.list_files_event(event)

    def remove_dir_check(self):
        self.confirm_window = tk.Toplevel(root)
        self.confirm_window.focus_set()
        self.confirm_window.bind("<Return>", self.remove_dir_event)

        text = tk.Label(self.confirm_window, text = 'Are you sure you want to remove the directory?')
        text.grid(row = 0, column = 0, columnspan = 3)

        yes = tk.Button(self.confirm_window, text = 'Yes', command = self.remove_dir,
                        cursor = 'hand2', width = '10')
        yes.grid(row = 1, column = 0)

        view_button = tk.Button(self.confirm_window, text = 'View contents', command = self.list_remove_files,
                                cursor = 'hand2', width = '10')
        view_button.grid(row = 1, column = 1)

        no = tk.Button(self.confirm_window, text = 'No', command = self.close_window,
                        cursor = 'hand2', width = '10')
        no.grid(row = 1, column = 2)

    def remove_dir_check_event(self, event):
        self.confirm_window = tk.Toplevel(root)
        self.confirm_window.focus_set()
        self.confirm_window.bind("<Return>", self.remove_dir_event)

        text = tk.Label(self.confirm_window, text = 'Are you sure you want to remove the directory?')
        text.grid(row = 0, column = 0, columnspan = 3)

        yes = tk.Button(self.confirm_window, text = 'Yes', command = self.remove_dir,
                        cursor = 'hand2', width = '10')
        yes.grid(row = 1, column = 0)

        view_button = tk.Button(self.confirm_window, text = 'View contents', command = self.list_remove_files,
                                cursor = 'hand2', width = '10')
        view_button.grid(row = 1, column = 1)

        no = tk.Button(self.confirm_window, text = 'No', command = self.close_window,
                        cursor = 'hand2', width = '10')
        no.grid(row = 1, column = 2)

    def list_remove_files(self):
        files = []
        path = self.path_entry.get()+self.path_make_entry.get()
        os.chdir(path)
        for file in os.listdir(path):
            files.append(file+'\n')
        self.list_all_files(files)

    def remove_dir_event(self, event):
        base_path = self.path_entry.get()
        os.chdir(base_path)
        os.removedirs(base_path+self.path_make_entry.get())
        self.list_files_event(event)
        self.confirm_window.destroy()

    def remove_dir(self):
        base_path = self.path_entry.get()
        os.chdir(base_path)
        os.removedirs(base_path+self.path_make_entry.get())
        self.list_files()
        self.confirm_window.destroy()

    def close_window(self):
        self.confirm_window.destroy()

    def go_back(self):
        self.master.focus_set()
        path = self.path_entry.get()
        slash = 0
        for i in range(0, len(path)):
            if path[i] == '\\' and i > slash:
                slash = i
        path = path[0:slash]
        if path == 'C:':
            self.back_folder.config(state = 'disabled')
        os.chdir(path)
        self.path_var.set(path)
        self.list_files()

    def go_back_event(self, event):
        self.go_back()

    def email_details(self):
        self.email_window = tk.Toplevel(root)
        self.email_window.focus_set()
        self.email_window.bind("<Escape>", self.close_email_event)
        self.email_window.bind("<Return>", self.send_email_event)

        self.send_label = tk.Label(self.email_window, text = 'Sender Email:')
        self.send_label.grid(row = 0, column = 0, pady = 10)
        self.send_entry = tk.Entry(self.email_window)
        self.send_entry.grid(row = 0, column = 1, pady = 10)

        self.send_pass_label = tk.Label(self.email_window, text = 'Password:')
        self.send_pass_label.grid(row = 0, column = 2, pady = 10)
        self.send_pass = tk.Entry(self.email_window, width = 26)
        self.send_pass.grid(row = 0, column = 3, columnspan = 2, pady = 10)

        self.reciever_label = tk.Label(self.email_window, text = 'Recipient Email:')
        self.reciever_label.grid(row = 1, column = 0, pady = 10)
        self.reciever_entry = tk.Entry(self.email_window)
        self.reciever_entry.grid(row = 1, column = 1, pady = 10)

        self.confirm_send = tk.Button(self.email_window, text = 'Send', width = 10,
                                      command = self.send_email, cursor = 'hand2')
        self.confirm_send.grid(row = 1, column = 3)
        self.cancel_send = tk.Button(self.email_window, text = 'Cancel', width = 10,
                                      command = self.email_window.destroy
                                     , cursor = 'hand2')
        self.cancel_send.grid(row = 1, column = 4)

    def close_email_event(self, event):
        self.email_window.destroy()

    def send_email_event(self, event):
        self.send_email()

    def send_email(self):
        port = 465
        password = self.send_pass.get()
        sender_email = self.send_entry.get()
        recipient_email = self.reciever_entry.get()
        message = self.display.get('1.0',tk.END)
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL('smtp.gmail.com', port, context = context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, recipient_email, message)
        self.email_window.destroy()


root = tk.Tk()
root.title('PWM')
p = PWM(root)
root.mainloop()
