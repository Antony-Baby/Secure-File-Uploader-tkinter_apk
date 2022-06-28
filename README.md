# Secure File Uploader

Stack : Python3
DB : MySQL (XAMPP)

This is a POC for secure file uploading, user can upload files to a location with encryption and will be able to download on OTP verification.

# Setup

Either follow the steps manually or Run "pip install -r requirements.txt "
    Note : this is only for library installation. You have to do Mysql configs sep(installation and configuration and db creation(config.py)) and folder creation manually
 
<ol>
    <li> ** Install libraries and create folder ** 
        <ol>
            <li>pip install cryptography<li>
            <li>mkdir upload_location<li>
            <li>mkdir Downloads<li>
        </ol>
        </li>
    <li>** To config MySQL Database **
    <ol>
    <li>install and config any mysql db //Here We are using XAMPP Cross platform for mysql(MariaDB)</li>
    <li>Update the sqlcofig values of sfu_data.py file</li>
    <li>pip install mysql-connector-python</li>
    <li>run the config.py file create database and tables (python config.py)</li>
    </ol>
    </li>
</ol>

<ol>
    <li> ** Install libraries and create folder ** 
        <ol>
            <li>pip install cryptography<li>
            <li>mkdir upload_location<li>
            <li>mkdir Downloads<li>
        </ol>
        </li>
    <li>** To config MySQL Database **
    <ol>
    <li>install and config any mysql db //Here We are using XAMPP Cross platform for mysql(MariaDB)</li>
    <li>Update the sqlcofig values of sfu_data.py file</li>
    <li>pip install mysql-connector-python</li>
    <li>run the config.py file create database and tables (python config.py)</li>
    </ol>
    </li>
</ol>
<!-- pip install fastapi
pip install uvicorn -->


# To Execute
* python3 sfu.py

TODO
* Email sending for OTP
* validations

