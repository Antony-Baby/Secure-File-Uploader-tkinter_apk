import tkinter as tk
from tkinter import ttk
import subprocess
import os
import shutil
from turtle import color, title
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

root = tk.Tk()
root.geometry("700x600")
file_upload_location = os.getcwd() + "/upload_location/"
reference_file = json.loads(open(os.getcwd() + "/Data/reference_file.json","r").read())
employees = sfu_database(mt.emp_emails,"")
file_download_location = os.getcwd() + "/Downloads/"

class file_upload:
    
    def __init__(self) -> None:
               
        self.label_file = tk.Label(root,text="Enter the file name ")
        self.label_file.place(x=100,y=150)
        self.inp_file = tk.Entry(root)
        self.inp_file.place(x=200,y=150)
        self.label_email = tk.Label(root,text="Enter the email id ")
        self.label_email.place(x=100,y=200)
        self.inp_email = tk.Entry(root)
        self.inp_email.place(x=200,y=200)
        self.label_dl = tk.Label(root,text="Enter the User Group name ")
        self.label_dl.place(x=100,y=250)
        self.inp_dl = tk.Entry(root)
        self.inp_dl.place(x=200,y=250)
        self.inp_sub = tk.Button(root,text="Continue",command=self.file_uploader)
        self.inp_sub.place(x=250,y=300)
    def file_uploader(self):
        file_name_with_location = str(self.inp_file.get())
            # a = input("\n Please enter file name with full path : ")
        if os.path.exists(file_name_with_location):
            b = self.inp_email.get()
            user_email = str(b)
            if len(user_email) > 0:
                    if checkforelement(employees,user_email):
                        c=self.inp_dl.get()
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
                        self.label_success = tk.Label(root,text="Encryption Completed")
                        self.label_success.place(x=120,y=360)


                    else:
                        print("Given Email id not a registered Employee")
                        self.label_success = tk.Label(root,text="Given Email id not a registered Employee")
                        self.label_success.place(x=120,y=360)

            else:
                print("\nEmail id required")
                self.label_success = tk.Label(root,text="Email id required")
                self.label_success.place(x=120,y=360)


        else:
            self.label_success = tk.Label(root,text="Invalid File")
            self.label_success.place(x=120,y=360)


        
def SFPMain():
    os.system('color 0A')
    subprocess.call('cls',shell=True)
    # print(Fore.RED+banner)
    a = input("\n 1. Upload File\n 2. Download File \n Your input is: ")
    userinput = int(a)
    if (userinput == 1):
        print("\n....Upload Process Begin....")
        os.system('color 94')
        file_uploader()
    elif (userinput == 2):
        print("\n....Download Process Begin....")
        os.system('color E4')
        # file_download()
    else:
        raise Exception("Please provide correct input")
    con = str(input("\n Do you want to continue..?.(Y/N).  "))
    if(con.casefold()=='Y'):
      SFPMain()
    else:
      print("\n ...Thank You!!.... ")
      exit()


if __name__ == "__main__":
    # file_uploader()
    file_upload()
    root.mainloop()
    # SFPMain()