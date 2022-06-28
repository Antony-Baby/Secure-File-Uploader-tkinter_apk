import mysql.connector
print("Content-Type: text/html\n\n")
import sys
sys.path.append(r"C:\Users\Antony\AppData\Local\Programs\Python\Python37/python.exe")
from sfu_data import sqlconfig as conf
from sfu_data import method_type

print(method_type.emp_emails)

print(conf.password)
mydb = mysql.connector.connect(
    host=conf.host,
    user=conf.user,
    password=conf.password
    # database=conf.database,
    # auth_plugin= conf.auth_plugin
)
cursor = mydb.cursor()
db= "sfu_db"
sql_Create_Db ="CREATE DATABASE "+db
sql_Create_Table_employee = '''CREATE TABLE `employee`(
   Emp_Id int(11) AUTO_INCREMENT PRIMARY KEY,
   Emp_Name varchar(40),
   Emp_Email varchar(40),
   Emp_Level varchar(10),
   Created_On Datetime not null default current_timestamp
)'''
sql_Create_Table_reference = '''CREATE TABLE `reference`(
   Doc_Name varchar(30),
   User_Email varchar(40),
   Key_Val varchar(200),
   Tocken int(4),
   DL varchar(10),
   Created Datetime not null default current_timestamp,
   Last_Updated Datetime not null default current_timestamp on update current_timestamp

)'''

sql_Create_Table_DL = '''CREATE TABLE `Emp_Dl`(
   DL_Name varchar(20),
   Emp_Email varchar(1000)
)'''

sql_insert_employee = """INSERT INTO `EMPLOYEE` (Emp_Name,Emp_Email,Emp_Level) 
   Values(%s,%s,%s)"""

val = [('Antony Baby','antonybabye@gmail.com','L1'),
   ('Jomet Joy','jometjoy.v@gmail.com','L1'),
   ('Test user','antonyqa7335@gmail.com','L2')
   ]

sql_insert_Dl = """INSERT INTO `Emp_DL` (DL_Name,Emp_Email) 
   Values(%s,%s)"""

dl_val= [
   ('ALL','["antonybabye@gmail.com", "jometjoy.v@gmail.com", "antonyqa7335@gmail.com"]'),
   ('Admin','["antonybabye@gmail.com", "jometjoy.v@gmail.com"]'),
   ('Temp','["antonyqa7335@gmail.com"]')
]

# cursor.execute(sql_Create_Db)
print("Database sfu_db created")
mydb = mysql.connector.connect(
    host=conf.host,
    user=conf.user,
    password=conf.password,
    database=db,
    auth_plugin= conf.auth_plugin
)

cursor = mydb.cursor()

# cursor.execute(sql_Create_Table_employee)
print("Table Employee created")
# cursor.execute(sql_Create_Table_reference)
print("Table reference created")
# cursor.execute(sql_Create_Table_DL)
print("Table Emp_DL created")
# cursor.close()
# cursor = mydb.cursor()
# cursor.executemany(sql_insert_employee,val)

cursor.executemany(sql_insert_Dl,dl_val)
mydb.commit()
print("insertion to employee table completed")


cursor.close()
mydb.close()
