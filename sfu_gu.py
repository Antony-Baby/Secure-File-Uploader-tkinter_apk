from cProfile import label
import subprocess
import os
import shutil
import tkinter
from turtle import color, down
#pip install cryptography
from cryptography.fernet import Fernet
import json
import random
from server import checkforelement, checkinjsonstring
from connector import sfu_database
from sfu_data import method_type as mt
from sendmail import sendmail
import time
# from colorama import Back, Fore, init
import tkinter as tk
from tkinter import ttk



root = tk.Tk()
root.geometry("700x600")
file_upload_location = os.getcwd() + "/upload_location/"
reference_file = json.loads(open(os.getcwd() + "/Data/reference_file.json","r").read())
employees = sfu_database(mt.emp_emails,"")
file_download_location = os.getcwd() + "/Downloads/"


class download:
    def __init__(self):
        self.label_filename = tk.Label(root,text="Please enter file name to download (without path) :")
        self.label_filename.place(x=100,y=200)
        self.inp_filename =tk.Entry(root)
        self.inp_filename.place(x=200,y=200)
        self.label_u_email = tk.Label(root,text="please enter your email address to verify : ")
        self.label_u_email.place(x=100,y=250)
        self.inp_u_email =tk.Entry(root)
        self.inp_u_email.place(x=200,y=250)
        self.label_send = tk.Button(root,text="Send OTP for validation", command=self.verifyuser)
        self.label_send.place(x=200,y=300)

    def update_otp(r_data):
        d_str = json.dumps(r_data, indent = 4)
        with open(os.getcwd() + "/Data/reference_file.json","w") as f:
            f.write(d_str)

    def generate_otp():
        otp = random.randrange(10000,99999)
        return otp

    def send_otp(r_file,f_name):
        r_file[f_name]={ 
                "author" : str(download.generate_otp()),
                "user" : str(download.generate_otp())
        }
        download.update_otp(r_file)
        return r_file

    def verifyuser(self):
        self.file_name = str(self.inp_filename.get())
        if checkforelement(sfu_database(mt.files,self.file_name),self.file_name):
            self.doc = (sfu_database(mt.one_file,self.file_name))
            u_email = str(self.inp_u_email.get())
            if checkforelement(employees,u_email):
                DL_list = sfu_database(mt.dl_users,self.file_name)
                self.author = self.doc[1].casefold()==u_email
                if checkinjsonstring(DL_list,u_email) or self.author:
                # print(DL_list[0])
                # if u_email in DL_list or author:
                    self.otp1 = download.send_otp(reference_file,(self.file_name))
                    self.start = time.time()
                    # sendmail("author",self.doc[1],reference_file,file_name)
                    self.label_otp1 = tk.Label(root,text="Enter the OTP send to the author id "+self.otp1[self.file_name]["author"])
                    self.label_otp1.place(x=100,y=350)
                    self.inp_otp1 = tk.Entry(root)
                    self.inp_otp1.place(x=200,y=350)
                    self.btn_otp1 = tk.Button(root,text="Verify",command=self.verifyotp1)
                    self.btn_otp1.place(x=200,y=400)
                else:
                    # sendmail("warning",self.doc[1],u_email,file_name)
                    print("\n...You are not authorized to access this file. Please contact admin for access...")
                    self.lable_message =tk.Label(root,text="You are not authorized to access this file. Please contact admin for access...")
                    self.lable_message.place(x=100,y=400)
            else:
                # sendmail("warning",self.doc[1],u_email,file_name)
                print("\n..Sorry! You are not a registered user, Please contact admin...")
                self.lable_message =tk.Label(root,text="Sorry! You are not a registered user, Please contact admin...")
                self.lable_message.place(x=100,y=400)
        else:
            print("\nInvalid File")
            self.lable_message =tk.Label(root,text="Invalid File")
            self.lable_message.place(x=100,y=400)   
    
    def verifyotp1(self):
        e_otp = str(self.inp_otp1.get())
        self.end=time.time()
        t = (format(self.end-self.start))
        if float(t) > 60 :
            print("\n ... Timeout >>session expired !...")
            exit()
        if e_otp == reference_file[self.file_name]["author"]:
            if not self.author:
                # sendmail("user",u_email,reference_file,file_name)
                self.label_otp2 = tk.Label(root,text="enter the otp send to the user id "+self.otp1[self.file_name]["user"] )
                self.label_otp2.place(x=100,y=450)
                self.inp_otp2 = tk.Entry(root)
                self.inp_otp2.place(x=200,y=450)
                self.btn_otp2 = tk.Button(root,text="Verify",command=self.file_download)
                self.btn_otp2.place(x=200,y=500)
            else:
                self.file_download()
        else:
            print("\nInvalid Otp")
            self.lable_message =tk.Label(root,text="Invalid Otp")
            self.lable_message.place(x=100,y=400)

    def file_download(self):
        if not self.author:
            # sendmail("user",u_email,reference_file,file_name)
            e2_otp = str(self.inp_otp2.get())
            if e2_otp == reference_file[self.file_name]["user"]:
                pass
            else:
                print("Invalid otp 2")
                self.lable_message =tk.Label(root,text="Invalid Otp 2")
                self.lable_message.place(x=100,y=550)
                exit()
        print("\n....Decrypting File....")
        shutil.copy(file_upload_location+self.file_name, file_download_location)
        key = self.doc[2]
        fernet = Fernet(key)
        # copy to a download loc and decrypt
        # opening the encrypted file
        with open(file_download_location + self.file_name, 'rb') as enc_file:
            encrypted = enc_file.read()
        # decrypting the file
        decrypted = fernet.decrypt(encrypted)
        with open(file_download_location + self.file_name, 'wb') as dec_file:
            dec_file.write(decrypted)
        count = self.doc[3]
        # print("\n....File Downloaded....")
        self.lable_message =tk.Label(root,text="File downloaded")
        self.lable_message.place(x=100,y=550)
        # reference_file[file_name]["otp"] = ""
        count +=1
        r_file = {
            "tocken" : count, 
            "doc_name" : self.file_name
        }
        res =sfu_database(mt.update_tocken,r_file)
        exit()
            

if __name__ == "__main__":
    # file_uploader()
    download()
    root.mainloop()
    # SFPMain()