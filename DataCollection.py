#!/usr/bin/env python
# coding: utf-8


import pandas as pd
import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Progressbar
import time
import random
import json
import os
#curr_work_dir = os.path.abspath(os.path.dirname(sys.executable))

try:
    if getattr(sys, 'frozen', False):
        curr_work_dir = os.path.abspath(os.path.dirname(sys.executable))
    elif __file__:
        curr_work_dir = os.path.abspath(os.path.dirname(__file__))
except:
    curr_work_dir = os.path.abspath(os.path.dirname(os.getcwd()))



PASSWORD = "bridport20"
NR_PASSWORD_ENTRIES = 35
NR_SETTEXTS_ENTRIES = 20

frame_width = 500
frame_height = 400



class UserSaver:
    
    def __init__ (self, name, email, further_contact, consent):
        self.name = name
        self.email = email
        self.further_contact = further_contact
        self.consent = consent
        
        self.filename = name + ".json"
        self.filename = os.path.normpath(curr_work_dir + "/" + self.filename)
    def save_user(self):
        data = {}
        data=({
            "name"            : self.name,
            "email"           : self.email,
            "further_contact" : self.further_contact,
            "consent"         : self.consent })
        
        with open(self.filename, "w", encoding="utf8") as outfile:
            json.dump(data, outfile)
    


class DataSaver:
    
    def __init__ (self, name, data):
        self.filename = name + ".xlsx"
        self.filename = os.path.normpath(curr_work_dir + "/" + self.filename)
        self.data = data
        
    def save_data(self):
        writer = pd.ExcelWriter(self.filename, engine = "xlsxwriter")
        
        try:
            read_data = pd.read_excel(self.filename, encoding="utf8")
            self.data = pd.concat([self.data, read_data])
        except:
            pass
        self.data.to_excel(writer, sheet_name = "Sheet1", index = False, encoding="utf8")
        
        writer.save()
            


class Recorder:
    
    def __init__ (self):
        self.name = ""
        self.email = ""
        self.further_contact = False
        self.consent = False
        
        self.entry = 0
        self.password_start_entry = 0
        self.settexts_start_entry = 0
        self.curr_database = pd.DataFrame()
        self.password_database = pd.DataFrame()
        self.settexts_database = pd.DataFrame()
        self.keys_used = set()
        
        self.texts = []
        self.selected_texts = []
        self.window = None
        
    def get_password_entry(self):
        try:
            filename = "password_" + self.name + ".xlsx"
            filename = os.path.normpath(curr_work_dir + "/" + filename)
            read_data = pd.read_excel(filename, encoding="utf8")
            return (max(read_data["entry"]) + 1)
        except:
            return 0
        
    def get_settexts_entry(self):
        try:
            filename = "settexts_" + self.name + ".xlsx"
            filename = os.path.normpath(curr_work_dir + "/" + filename)
            read_data = pd.read_excel(filename, encoding="utf8")
            return (max(read_data["entry"]) + 1)
        except:
            return 0
        
    def destroy_widgets(self):
        self.curr_database = self.curr_database[0:0]
        for widget in self.window.winfo_children():
            widget.destroy()
        
    def record_user(self):
        self.window = Tk()
        self.window.geometry(str(frame_width)+"x"+str(frame_height))
        self.window.title("Keyboard Dynamics Data Collection")
        
        lbl_welcome = Label(self.window, text = "Thank you for willing to participate! You will be asked to fill a specific password and then type suggested text.", font = ("Arial", 15), wraplength = frame_width)
        lbl_welcome.grid(column = 0, row = 0, sticky = W)
        
        lbl_name = Label(self.window, text = "Please enter your first name and last name", font = ("Arial Bold", 15), wraplength = frame_width)
        lbl_name.grid(column = 0, row = 1, sticky = W)

        txt_name = Entry(self.window, width = 10)
        txt_name.grid(column = 0, row = 2, sticky = W+E)
        txt_name.focus()
        
        lbl_email = Label(self.window, text = "Please enter your email", font = ("Arial Bold", 15), wraplength = frame_width)
        lbl_email.grid(column = 0, row = 3, sticky = W)
        
        txt_email = Entry(self.window, width = 10)
        txt_email.grid(column = 0, row = 4, sticky = W+E)
        
        lbl_contact = Label(self.window, text = "Can we contact you further (if needed)?", font = ("Arial Bold", 15), wraplength = frame_width)
        lbl_contact.grid(column = 0, row = 5, sticky = W)
        
        contact = IntVar()
        rad_yes = Radiobutton(self.window, text = "Yes", value = 2, variable = contact)
        rad_no = Radiobutton(self.window, text = "No", value = 1, variable = contact)
        rad_yes.grid(column = 0, row = 6, sticky = W)
        rad_no.grid(column = 0, row = 7, sticky = W)
        
        lbl_agree = Label(self.window, text = "I agree that my data will be disclosed to the author of the experiment, and anonymized data will be available publicly. Close the window if you do not agree.", font = ("Arial", 15), wraplength = frame_width)
        lbl_agree.grid(column = 0, row = 8, sticky = W)
        
        agree = IntVar()
        rad_agree = Radiobutton(self.window,text = "I agree", value = 1, variable = agree)
        rad_agree.grid(column = 0, row = 9, sticky = W)
        
        btn_start = Button(self.window, text = "Start", bg = "blue", command = lambda: self.check_entered_user(txt_name, txt_email, contact, agree))
        btn_start.grid(column = 0, row = 10, sticky = W+E)
    
        self.window.mainloop()
        
    def is_valid_name(self, name):
        regex = "([A-Za-z]|-){2,25}"
        
        name_parts = name.split(" ")
        if (len(name_parts) > 5):
            return False
        for part in name_parts:
            if (not re.fullmatch(regex, part, re.I)):
                return False
        return True
        
    def is_valid_email(self, email):
        regex = "^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,4})+$"
        if(re.search(regex,email)):   
            return True
        else:  
            return False
        
    def check_entered_user(self, txt_name, txt_email, contact, agree):
        done = ((len(txt_name.get()) > 0) and
                (self.is_valid_name(txt_name.get())) and
                (len(txt_email.get()) > 0) and
                (self.is_valid_email(txt_email.get())) and
                (contact.get() == 2 or contact.get() == 1) and
                (agree.get() == 1))
        if (done):
            self.name = txt_name.get()
            self.email = txt_email.get()
            further_contact = True if (contact.get() == 2) else False
            consent = True if (agree.get() == 1) else False
            user = UserSaver(self.name, self.email, further_contact, consent)
            user.save_user()
            
            self.password_intro()
        else:
            if (not self.is_valid_name(txt_name.get())):
                messagebox.showerror("Error", "Don't try to be funnny, enter your name, please :) \n Please only use letters of Latin alphabet.")
            elif (not self.is_valid_email(txt_email.get())):
                messagebox.showerror("Error", "Please enter a legitimate email address.")
            else:
                messagebox.showerror("Error", "Please enter all requested information.")
        
    def password_intro(self):
        self.destroy_widgets()
        
        self.password_start_entry = self.get_password_entry()
        self.entry = self.password_start_entry
        
        lbl1 = Label(self.window, text = "In this section you are asked to enter the following password " + str(NR_PASSWORD_ENTRIES) + " times", font = ("Arial", 15), wraplength = frame_width)
        lbl1.grid(column = 0, row = 0, sticky = W)
        
        lbl_password = Label(self.window, text = PASSWORD, font = ("Arial Bold", 20), wraplength = frame_width)
        lbl_password.grid(column = 0, row = 1, sticky = W+E)
        
        lbl2 = Label(self.window, text = "Please enter the password with your normal pace. Press Enter when done.", font = ("Arial", 15), wraplength = frame_width)
        lbl2.grid(column = 0, row = 2, sticky = W)
        
        lbl_donot = Label(self.window, text = "DO NOT: use your mouse/trackpad, copy/paste, use arrow buttons.", font = ("Arial", 15), wraplength = frame_width)
        lbl_donot.grid(column = 0, row = 3, sticky = W)
        
        lbl_do = Label(self.window, text = "DO: enter the password only by pressing buttons that correspond to the characters in the password.", font = ("Arial", 15), wraplength = frame_width)
        lbl_do.grid(column = 0, row = 4, sticky = W)
        
        lbl3 = Label(self.window, text = "The password will be displayed the entire time.", font = ("Arial", 12), wraplength = frame_width)
        lbl3.grid(column = 0, row = 5, sticky = W)
        
        btn_start = Button(self.window, text = "Start", bg = "blue", command = self.password_record)
        btn_start.grid(column = 0, row = 6, sticky = W+E)
        
    def on_key_press(self, event, txt, is_password):
        if (event.char == "\r"):
            return
        #TODO:: if we're now also not allowing shift, we gotta check for it too
        if (event.keysym == "BackSpace" and is_password):
            messagebox.showerror("Error", "You have hit BackSpace. Try again.")
            self.clear_for_reentry(txt)
            return
        new_event = {"entry"    : self.entry,
                     "time"     : time.time(), 
                     "key_code" : event.keycode, 
                     "key_char" : event.char,
                     "key"      : event.keysym,
                     "event"    : "KeyPress"}
        self.curr_database = self.curr_database.append(new_event, ignore_index = True)
        if (not event.char in self.keys_used):
            self.keys_used.add(event.keysym)
    
    def on_key_release(self, event, txt, is_password):
        if (event.char == "\r"):
            return
        if (event.keysym == "BackSpace" and is_password):
            messagebox.showerror("Error", "You have hit BackSpace. Try again.")
            self.clear_for_reentry(txt)
            return
        
        new_event = {"entry"    : self.entry,
                     "time"     : time.time(), 
                     "key_code" : event.keycode,
                     "key_char" : event.char,
                     "key"      : event.keysym,
                     "event"    : "KeyRelease"}
        self.curr_database = self.curr_database.append(new_event, ignore_index = True)
        if (not event.char in self.keys_used):
            self.keys_used.add(event.keysym)
        
    def get_faulty_indices(self, data):
        faulty_indices = []
        for i in range(1, len(data)):
            if (data.iloc[i]["event"] == data.iloc[i-1]["event"]):
                if (data.iloc[i]["event"] == "KeyPress"):
                    faulty_indices.append(data.index[i])
                else:
                    faulty_indices.append(data.index[i-1])
                    
        return faulty_indices
    
    def filter_data(self):
        self.curr_database.sort_values(by = "time", inplace = True)
        self.curr_database.reset_index(drop = True, inplace = True)
        
        for key in self.keys_used:
            key_data = self.curr_database[self.curr_database["key"] == key]
            faulty_indices = self.get_faulty_indices(key_data)
            self.curr_database.drop(faulty_indices, inplace = True)
            
        self.curr_database.reset_index(drop = True, inplace = True)
        
    def clear_for_reentry(self, password_txt):
        password_txt.delete(0, 'end')
        password_txt.focus()
        self.curr_database = self.curr_database[0:0]
        
    def on_return_password(self, window, event, password_txt, bar):
        if (password_txt.get() != PASSWORD):
            messagebox.showerror("Error", "Entered password is wrong. Try again.")
            self.clear_for_reentry(password_txt)
            return
            
        self.filter_data()
        self.password_database = pd.concat([self.password_database, self.curr_database])
        self.clear_for_reentry(password_txt)
        self.entry += 1
        progress = ((self.entry - self.password_start_entry) / NR_PASSWORD_ENTRIES) * 100
        bar["value"] = progress
        if ((self.entry - self.password_start_entry) >= NR_PASSWORD_ENTRIES):
            self.save_password_data()
            self.curr_database = None
            self.curr_database = pd.DataFrame()
            #self.settext_intro() uncomment if collecting free-texts
            self.thankyou_screen() # comment if collecting free-texts
        
    def password_record(self):
        self.destroy_widgets()
        
        lbl_password = Label(self.window, text = "Password:   " + PASSWORD, font = ("Arial Bold", 15), wraplength = frame_width)
        lbl_password.grid(column = 0, row = 0, sticky = W)
        
        txt = Entry(self.window, width = 10)
        txt.grid(column = 0, row = 1, sticky = W+E)
        txt.focus()
        
        bar = Progressbar(self.window, length = frame_width)
        bar.grid(column = 0, row = 2, sticky = W+E)
        bar["value"] = 0
        
        self.window.bind("<KeyPress>", lambda event: self.on_key_press(event, txt, True))
        self.window.bind("<KeyRelease>", lambda event: self.on_key_release(event, txt, True))
        self.window.bind("<Return>", lambda event: self.on_return_password(self.window, event, txt, bar))
        
    def settext_intro(self):
        self.destroy_widgets()
        
        self.settexts_start_entry = self.get_settexts_entry()
        self.entry = self.settexts_start_entry
        
        lbl1 = Label(self.window, text = "You have completed the password stage!!!", font = ("Arial Bold", 15), wraplength = frame_width)
        lbl1.grid(column = 0, row = 0, sticky = W)
        
        lbl2 = Label(self.window, text = "In the next section you are asked to enter " + str(NR_SETTEXTS_ENTRIES) + " very short texts.", font = ("Arial", 15), wraplength = frame_width)
        lbl2.grid(column = 0, row = 1, sticky = W)
        
        lbl3 = Label(self.window, text = "Please enter the text with your normal pace. Press Enter when done.", font = ("Arial", 15), wraplength = frame_width)
        lbl3.grid(column = 0, row = 2, sticky = W)
        
        lbl_donot = Label(self.window, text = "DO NOT: use your mouse/trackpad, copy/paste.", font = ("Arial", 15), wraplength = frame_width)
        lbl_donot.grid(column = 0, row = 3, sticky = W)
        
        lbl_do = Label(self.window, text = "DO: enter the texts exactly like they are displayed. You can use backspace and arrow buttons to correct possible mistakes.", font = ("Arial", 15), wraplength = frame_width)
        lbl_do.grid(column = 0, row = 4, sticky = W)
        
        lbl_note = Label(self.window, text = "Immediately press enter when you are finished with writing the sentence. Do not try to reread it before pressing Enter.", font = ("Arial Bold", 15), wraplength = frame_width)
        lbl_note.grid(column = 0, row = 5, sticky = W)
        
        lbl4 = Label(self.window, text = "The text will be displayed while you are entering it.", font = ("Arial", 12), wraplength = frame_width)
        lbl4.grid(column = 0, row = 6, sticky = W)
        
        lbl5 = Label(self.window, text = "Please read the texts carefully before typing them.", font = ("Arial Bold", 20), fg = "red", wraplength = frame_width)
        lbl5.grid(column = 0, row = 7, sticky = W)
        
        lbl6 = Label(self.window, text = "If you find any problems, please report them via WhatsApp +31643850097 or email to m.turchina@student.tue.nl", font = ("Arial", 12), wraplength = frame_width)
        lbl6.grid(column = 0, row = 8, sticky = W)
        
        btn_start = Button(self.window, text = "Start", bg = "blue", command = self.settext_record)
        btn_start.grid(column = 0, row = 9, sticky = W+E)
        
    def select_texts(self):
        filename = os.path.normpath(curr_work_dir + "/corpusbulk.txt")
        self.texts = [line.rstrip('\n') for line in open(filename, encoding="utf8")]
        self.texts = [line.rstrip(' ') for line in self.texts]
        remaining_texts = list(range(len(self.texts)))
        selected_texts = []
        for _ in range(NR_SETTEXTS_ENTRIES):
            index = random.randrange(0, len(remaining_texts))
            selected_texts.append(remaining_texts[index])
            remaining_texts.pop(index)
        return selected_texts
    
    def on_return_settext(self, window, event, txt, lbl, bar):
        true_text = self.selected_texts[self.entry - self.settexts_start_entry][1]
        if (txt.get() != true_text):
            messagebox.showerror("Error", "Entered text is wrong. Try again.")
            self.clear_for_reentry(txt)
            return
            
        self.filter_data()
        self.curr_database["text"] = self.selected_texts[self.entry - self.settexts_start_entry][0]
        self.settexts_database = pd.concat([self.settexts_database, self.curr_database])
        self.clear_for_reentry(txt)
        self.entry += 1
        progress = ((self.entry - self.settexts_start_entry) / NR_SETTEXTS_ENTRIES) * 100
        bar["value"] = progress
        if ((self.entry - self.settexts_start_entry) >= NR_SETTEXTS_ENTRIES):
            self.save_settexts_data()
            self.thankyou_screen()
        else:
            curr_text = self.selected_texts[self.entry- self.settexts_start_entry][1]
            lbl_display = Label(self.window, text = curr_text, font = ("Arial Bold", 15))
            lbl_display.grid(column = 0, row = 1, sticky = W+E)
    
    def settext_record(self):
        self.destroy_widgets()
        
        selected_texts_indices = self.select_texts()
        self.selected_texts = [(i, self.texts[i]) for i in selected_texts_indices]
        
        lbl_text = Label(self.window, text = "Text:   ", font = ("Arial Bold", 15), wraplength = frame_width)
        lbl_text.grid(column = 0, row = 0, sticky = W)
        curr_text = self.selected_texts[self.entry - self.settexts_start_entry][1]
        lbl_display = Label(self.window, text = curr_text, font = ("Arial Bold", 15), wraplength = frame_width)
        lbl_display.grid(column = 0, row = 1, sticky = W)
        
        txt = Entry(self.window, width = 10)
        txt.grid(column = 0, row = 2, sticky = W+E)
        txt.focus()
        
        bar = Progressbar(self.window, length = frame_width)
        bar.grid(column = 0, row = 3, sticky = W+E)
        bar["value"] = 0
        
        self.window.bind("<KeyPress>", lambda event: self.on_key_press(event, txt, False))
        self.window.bind("<KeyRelease>", lambda event: self.on_key_release(event, txt, False))
        self.window.bind("<Return>", lambda event: self.on_return_settext(self.window, event, txt, lbl_display, bar))
        
    def thankyou_screen(self):
        self.destroy_widgets()
        
        lbl_done = Label(self.window, text = "You are done :) for now...", font = ("Arial Bold", 20), wraplength = frame_width)
        lbl_done.grid(column = 0, row = 0, sticky = W+E)
        
        lbl_thx = Label(self.window, text = "Thank you very much for participation!!!", font = ("Arial Bold", 17), wraplength = frame_width)
        lbl_thx.grid(column = 0, row = 1, sticky = W+E)
        
        lbl_contact2 = Label(self.window, text = "Would be ABSOLUTELY AMAZING if you could repeat all that for at least 4 more times with at least 2-3 hours between the sessions :)", font = ("Arial Bold", 15), wraplength = frame_width)
        lbl_contact2.grid(column = 0, row = 2, sticky = W)
        
        # change to 2 excel files when collecting free-texts
        lbl_contact1 = Label(self.window, text = "You should now see 1 excel files and 1 json. When you have completed all your sessions, please send them via WhatsApp to +31643850097 or email to m.turchina@student.tue.nl", font = ("Arial Bold", 15), wraplength = frame_width)
        lbl_contact1.grid(column = 0, row = 3, sticky = W)
        
    def save_password_data(self):
        filename = "password_" + self.name
        password_saver = DataSaver(filename, self.password_database)
        password_saver.save_data()
        
    def save_settexts_data(self):
        filename = "settexts_" + self.name
        settexts_saver = DataSaver(filename, self.settexts_database)
        settexts_saver.save_data()
             
recorder = Recorder()
recorder.record_user()
