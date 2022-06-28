import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def sendmail(type,email,r_file,file_name):
    from_address = "beingjoe98@gmail.com"
    # to_address = "antonybabye@gmail.com"
    to_address = email
    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Test email"
    msg['From'] = from_address
    msg['To'] = to_address
    # Create the message (HTML).
    if type.casefold()=="author":
        otp = r_file[file_name][type]
        html = """
        Hi User,
            One time password for verifying the admin approvel is """+otp+""" 
            
            Please note : By providing this OTP , You are agreed to provide access/approval to Download the file """+file_name+""" 
                to the user account """+ email
  
    elif type.casefold()=="user":
        otp = r_file[file_name][type]
        html ="User OTP for verification is "+ otp
    elif type.casefold()=="warning":
        email = r_file
        html = "Hi Admin, \n\n there is an unauthorized user attempt from the account "+ email+" to access the file "+ file_name
    # Record the MIME type - text/html.
    part1 = MIMEText(html, 'html')
    # Attach parts into message container
    msg.attach(part1)
    # Credentials
    username = 'beingjoe98@gmail.com'  
    password = 'kajbesphisgrkltq'  
    # Sending the email
    ## note - this smtp config worked for me, I found it googling around, you may have to tweak the # (587) to get yours to work
    server = smtplib.SMTP('smtp.gmail.com', 587) 
    server.ehlo()
    server.starttls()
    server.login(username,password)  
    server.sendmail(from_address, to_address, msg.as_string())  
    server.quit()