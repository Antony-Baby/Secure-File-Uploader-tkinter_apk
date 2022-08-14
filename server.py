import mysql.connector
# print("Content-Type: text/html\n\n")
import sys
sys.path.append(r"C:\Users\Antony\AppData\Local\Programs\Python\Python37/python.exe")
from sfu_data import sqlconfig as config,sqls

def employees(cursor):
    # cursor.execute("SELECT COUNT(*) FROM information_schema.columns WHERE table_name= 'employee'")
    # cols = (cursor.fetchone())[0]
    cursor.execute(sqls.sql_emp_emails)
    # cursor.execute("SELECT Emp_Email FROM `employee`")
    Emp_Emails =cursor.fetchall()
    return Emp_Emails

def checkinjsonstring(Iterals,check):
    for row in Iterals:
        for col in row:
            if check in col.casefold():
                return True
        return False

def checkforelement(Iterals,check):
    for row in Iterals:
        if row[0].casefold()==check:
            return True
    return False

def all_files(cursor):
    cursor.execute(sqls.sql_doc_names)
    return cursor.fetchall()

def insert_references(mydb,cursor,ref_file):
    
    if checkforelement(all_files(cursor),ref_file['doc_name']):
        print("\n Document with same name is already available in the repo, please update the name or choose a different file")
    else:
        # if the entry with same name is not available insert new record
        # sql = "INSERT INTO `reference` VALUES (%s, %s,%s,%s,%s)"
        sql = sqls.sql_insert_ref
        val = (ref_file['doc_name'], ref_file['user_email'],ref_file['key'],ref_file['tocken'],ref_file['DL'])
        cursor.execute(sql,val)
        mydb.commit()
        return True

# for decript

def retreiveonedoc(cursor,filename):
    val =(filename,)
    cursor.execute(sqls.sql_retrieveonedoc,val)
    return (cursor.fetchall())[0]

def retreiveDLusers(cursor,filename):
    val =(filename,)
    cursor.execute(sqls.sql_retrieveDLuserlist,val)
    return ((cursor.fetchall()))

def retreiveDLNames(cursor):
    cursor.execute(sqls.sql_DLnames)
    return ((cursor.fetchall()))

def update_references(mydb,cursor,ref_file):
        sql = sqls.sql_update_tocken
        val = (ref_file['tocken'],ref_file['doc_name'])
        cursor.execute(sql,val)
        mydb.commit()
        return True

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
    elif method.casefold()=="dl_list":
        res= retreiveDLNames(cursor)
    else:
        print("Invalid method")

    cursor.close()
    mydb.close()
    return res


