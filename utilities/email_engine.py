import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
from utils import print_log, red, green, reset, get_details_from_env_file

def send_email_with_attachment(time_stamp, attachment_paths):
    try:
        # Create the email
        subject = "ASC ALERT: New OCR Output"
        body = f'''Found different OCR output. Please check the Details.
        Last Updated : {time_stamp}
        '''
        user_info = get_details_from_env_file()
        sender_email = "merlinsbrownbeard@gmail.com"
        sender_password = "pmmt hybl jcnj aqyr"
        recepient_email = user_info.get_email()
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recepient_email
        msg['Subject'] = subject

        # Attach the email body
        msg.attach(MIMEText(body, 'plain'))

        # Attach the files
        for attachment_path in attachment_paths:
            if attachment_path and os.path.isfile(attachment_path):
                filename = os.path.basename(attachment_path)
                with open(attachment_path, 'rb') as attachment:
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f'attachment; filename={filename}')
                msg.attach(part)

        # Set up the SMTP server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)

        # Send the email
        text = msg.as_string()
        server.sendmail(sender_email, recepient_email, text)
        print_log("=====================================================================================================")
        print_log(f"{green}Email sent successfully!{reset}", "info")
        print_log("=====================================================================================================")
        server.quit()
    except Exception as e:
        print_log(f"{red}An error occurred while sending the email: {e}", "error")
        print_log("=====================================================================================================")

def send_TLE_email():
    try:
        # Create the email
        subject = "ASC ALERT: TLE"
        body = f'''The program took too long to execute. Please check the Details.
        '''
        user_info = get_details_from_env_file()
        sender_email = "merlinsbrownbeard@gmail.com"
        sender_password = "pmmt hybl jcnj aqyr"
        recepient_email = user_info.get_email()
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recepient_email
        msg['Subject'] = subject

        # Attach the email body
        msg.attach(MIMEText(body, 'plain'))

        # Set up the SMTP server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)

        # Send the email
        text = msg.as_string()
        server.sendmail(sender_email, recepient_email, text)
        print_log("=====================================================================================================")
        print_log(f"{green}TLE mail sent successfully!{reset}", "info")
        print_log("=====================================================================================================")
        server.quit()
    except Exception as e:
        print_log(f"{red}An error occurred while sending the email: {e}", "error")
        print_log("=====================================================================================================")