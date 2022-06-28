class sqlconfig:
    host="localhost"
    user="sfu"
    password="Project_sfu@123"
    auth_plugin='mysql_native_password'

class sqls:
    sql_insert_ref = "INSERT INTO `reference`(Doc_Name,User_Email,Key_val,Tocken,DL) VALUES (%s, %s,%s,%s,%s)"
    sql_doc_names = "SELECT Doc_Name FROM `reference`"
    sql_emp_emails="SELECT Emp_Email FROM `employee`"
    sql_retrieveonedoc ="Select * from `reference` where Doc_Name=%s"
    sql_update_tocken ="UPDATE `reference` SET `Tocken`= %s WHERE `Doc_Name`=%s "
    sql_retrieveDLuserlist = "Select Emp_Email from Emp_DL where DL_Name=(Select DL from reference where Doc_Name=%s)"

class method_type:
    files = "fetch_files"
    emp_emails = "user_emails"
    update_ref ="update_reference"
    one_file = "single_doc_details"
    update_tocken ="update_tocken"
    dl_users ="dl_user_list"
