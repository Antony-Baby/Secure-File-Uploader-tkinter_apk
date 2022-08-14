
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
    sql_DLnames = "Select DL_Name from Emp_DL"

class method_type:
    files = "fetch_files"
    emp_emails = "user_emails"
    update_ref ="update_reference"
    one_file = "single_doc_details"
    update_tocken ="update_tocken"
    dl_users ="dl_user_list"
    dls = "dl_list"

class Images_GUI:
    bg_Home ="Data/title.jpg"
    bg_Upload= "Data/bg2.jpg"
    bg_download= "Data/bg1.jpg"
    btn_upload = "Data/upload.png"
    btn_download = "Data/download.png"
    btn_exit = "Data/exit.png"
    btn_home = "Data/home.png"

class GUI_size:

    # wi_width = winfo_screenwidth
    f_width= 1250
    f_heigh = 600
    btn_large= 40
    btn_small = 15
    btn_med=25
    lbl_large = 40
    lbl_small = 10
    lbl_med = 20
    txt_large = 50
    txt_small = 15
    txt_med = 30

