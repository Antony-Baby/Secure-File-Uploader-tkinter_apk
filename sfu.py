from cProfile import label
import subprocess
from textwrap import wrap
import tkinter as tk
from tkinter import BOTTOM, END, Button, StringVar, ttk
import os
import shutil
from turtle import color
from typing_extensions import IntVar
#pip install cryptography
from cryptography.fernet import Fernet
import json
import random
from server import checkforelement, checkinjsonstring
from connector import sfu_database
from sfu_data import method_type as mt
from sendmail import sendmail
import time


banner = """ 
  ____  _____ ____ _   _ ____  _____   _____ ___ _     _____   _   _ ____  _     ___    _    ____  _____ ____  
/ ___|| ____/ ___| | | |  _ \| ____| |  ___|_ _| |   | ____| | | | |  _ \| |   / _ \  / \  |  _ \| ____|  _ \ 
\___ \|  _|| |   | | | | |_) |  _|   | |_   | || |   |  _|   | | | | |_) | |  | | | |/ _ \ | | | |  _| | |_) |
 ___) | |__| |___| |_| |  _ <| |___  |  _|  | || |___| |___  | |_| |  __/| |__| |_| / ___ \| |_| | |___|  _ < 
|____/|_____\____|\___/|_| \_\_____| |_|   |___|_____|_____|  \___/|_|   |_____\___/_/   \_\____/|_____|_| \_\ 

"""

root = tk.Tk()
root.geometry("700x600")
file_upload_location = os.getcwd() + "/upload_location/"
reference_file = json.loads(open(os.getcwd() + "/Data/reference_file.json","r").read())
employees = sfu_database(mt.emp_emails,"")
file_download_location = os.getcwd() + "/Downloads/"


def hide_menu():
  SFPMain.label_options.place_forget()
  SFPMain.btn_upload.place_forget()
  SFPMain.btn_download.place_forget()

class file_upload:
    def __init__(self) -> None:
        self.frame= tk.Frame(root,bg="blue",width=700,height=550)
        self.frame.pack(side=BOTTOM)
        hide_menu()
        # var = IntVar()
        self.label_file = tk.Label(self.frame,width=20,wraplength=200,padx=5,text="Enter the file name ")
        self.label_file.place(x=100,y=150)
        self.inp_file = tk.Entry(self.frame)
        self.inp_file.place(x=300,y=150)
        self.label_email = tk.Label(self.frame,width=20,wraplength=200,padx=5,text="Enter the email id ")
        self.label_email.place(x=100,y=200)
        self.inp_email = tk.Entry(self.frame)
        self.inp_email.place(x=300,y=200)
        self.label_dl = tk.Label(self.frame,width=20,wraplength=200,padx=5,text="Enter the User Group name ")
        self.label_dl.place(x=100,y=250)
        opts=[
          "ALL",
          "Admin",
          "Temp"
        ]
        self.dl = StringVar()
        self.dl.set("ALL")
        self.drp_dl = tk.OptionMenu(self.frame,self.dl,*opts)
        self.drp_dl.place(x=300,y=250)
        self.inp_sub = tk.Button(self.frame,text="Continue",command=self.file_uploader)
        self.inp_sub.place(x=250,y=300)
    def file_uploader(self):
        file_name_with_location = str(self.inp_file.get())
            # a = input("\n Please enter file name with full path : ")
        if os.path.exists(file_name_with_location):
            b = self.inp_email.get()
            user_email = str(b)
            if len(user_email) > 0:
                    if checkforelement(employees,user_email):
                        c=self.dl.get()
                        print(c)
                        DL=str(c)
                        print("\n....Saving File....")
                        shutil.copy(file_name_with_location, file_upload_location)
                        key = Fernet.generate_key() 
                        print("\n....Encrypting File....")
                        fernet = Fernet(key)
                        fObj = open(file_name_with_location,"r")
                        filename = (os.path.basename(fObj.name))
                        # reading uploaded file
                        with open(file_upload_location + filename, 'rb') as file:
                            original = file.read()
                        # encrypting the file
                        encrypted = fernet.encrypt(original)
                        # writing the encrypted data
                        with open(file_upload_location + filename, 'wb') as encrypted_file:
                            encrypted_file.write(encrypted)
                        print("\n....Encryption Completed....")
                        # self.label_success.place(x=120,y=360)
                        # update refence file
                        reference_file= {
                        "doc_name" : filename,
                        "user_email": user_email,
                        "DL": DL,
                        "key" : key.decode('UTF-8'),
                        "tocken" : 0
                        }
                        res =sfu_database(mt.update_ref,reference_file)
                        # update_reference(reference_file)
                        print("\n....Updated Reference File....")
                        print("\n....File Upload Completed....")
                        self.label_success = tk.Label(self.frame,text="Encryption Completed")
                        self.label_success.place(x=120,y=360)


                    else:
                        print("Given Email id not a registered Employee")
                        self.label_success = tk.Label(self.frame,text="Given Email id not a registered Employee")
                        self.label_success.place(x=120,y=360)

            else:
                print("\nEmail id required")
                self.label_success = tk.Label(self.frame,text="Email id required")
                self.label_success.place(x=120,y=360)


        else:
            self.label_success = tk.Label(self.frame,text="Invalid File")
            self.label_success.place(x=120,y=360)


class download:
    def __init__(self):
        hide_menu()
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

class SFPMain:
    # os.system('color 0A')
    # subprocess.call('cls',shell=True)
    # print(Fore.RED+banner)
    # a = input(Fore.BLUE+Back.BLACK+"\n 1. Upload File\n 2. Download File \n Your input is: ")
  def stop():
    pass
  def return_home():
    root.destroy()
    root.mainloop()
    SFPMain()

  label_options = tk.Label(root,text="Please choose the operation ")
  label_options.place(x=200,y=200)
  btn_upload = tk.Button(root,text="Upload File ", command=file_upload)
  btn_upload.place(x=200,y=250)
  btn_download = tk.Button(root,text="Download File ",command=download)
  btn_download.place(x=200,y=300)
  btn_exit = tk.Button(root,text="EXIT",command=root.destroy)
  btn_exit.place(x=320,y=10)
  btn_return = tk.Button(root,text="Home",command=return_home)
  btn_return.place(x=350,y=10)
    
    # con = str(input("\n Do you want to continue..?.(Y/N).  "))
    # if(con.casefold()=='Y'):
    #   SFPMain()
    # else:
    #   print("\n ...Thank You!!.... ")
    #   exit()

if __name__ == '__main__' :
    # Calling main function
    SFPMain()
    root.mainloop()
