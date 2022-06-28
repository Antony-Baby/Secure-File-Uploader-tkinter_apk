import mysql.connector
from server import all_files, employees, insert_references, retreiveDLusers, retreiveonedoc, update_references
# print("Content-Type: text/html\n\n")
import sys
sys.path.append(r"C:\Users\Antony\AppData\Local\Programs\Python\Python37/python.exe")
from sfu_data import sqlconfig as config

def sfu_database(method,params):
    mydb = mysql.connector.connect(
        host=config.host,
        user=config.user,
        password=config.password,
        database="sfu_db",
        auth_plugin= config.auth_plugin
    )
    cursor = mydb.cursor()

    if method.casefold()=="user_emails":
        res= employees(cursor)
    elif method.casefold()=="update_reference":
        res=insert_references(mydb,cursor,params)
    # elif method.casefold()=="check_element":
        # return checkforelement(mydb,cursor,params)
    elif method.casefold()=="fetch_files":
        res= all_files(cursor)
    elif method.casefold()=="single_doc_details":
        res= retreiveonedoc(cursor,params)
    elif method.casefold()=="update_tocken":
        res = update_references(mydb,cursor,params)
    elif method.casefold()=="dl_user_list":
        res= retreiveDLusers(cursor,params)
    elif method.casefold()=="":
        pass
    else:
        print("Invalid method")

    cursor.close()
    mydb.close()
    return res