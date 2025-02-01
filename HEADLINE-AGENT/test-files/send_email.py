import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import datetime

smtp_server = os.environ['SMTP_KEY']  # SMTP server from env
smtp_port = int(os.environ['SMTP_PORT'])  # Port for TLS from env
sender_email = os.environ['SENDER_EMAIL']  # Sender email from env
receiver_email = os.environ['RECEIVER_EMAIL']  # Recipient email from env
password = os.environ['PASSWORD']  # Email password from env

# Create the email message
msg = MIMEMultipart("alternative")
msg["Subject"] = f"Today's News Summary - {datetime.datetime.now().strftime('%Y-%m-%d')}"
msg["From"] = sender_email
msg["To"] = receiver_email

# Get the absolute path to the email template
current_dir = os.path.dirname(os.path.abspath(__file__))
email_template_path = os.path.join(current_dir, "../static/email.html")


# Read the HTML template
with open(email_template_path, "r") as file:
    html_content = file.read()

# Attach the HTML content to the email
part = MIMEText(html_content, "html")
msg.attach(part)

# Connect to the SMTP server and send the email
try:
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()  # Start TLS encryption
    server.login(sender_email, password)  # Log in to the SMTP server
    server.sendmail(sender_email, receiver_email, msg.as_string())  # Send the email
    print("Email sent successfully!")
except Exception as e:
    print(f"Failed to send email: {e}")
finally:
    server.quit()  # Close the connection