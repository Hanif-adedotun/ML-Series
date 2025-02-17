import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from datetime import datetime
from dotenv import load_dotenv
load_dotenv('../.env')

smtp_server = os.environ['SMTP_KEY']  # SMTP server from env
smtp_port = int(os.environ['SMTP_PORT'])  # Port for TLS from env
sender_email = os.environ['SENDER_EMAIL']  # Sender email from env
receiver_email = os.environ['RECEIVER_EMAIL']  # Recipient email from env
password = os.environ['PASSWORD']  # Email password from env

# Create the email message
msg = MIMEMultipart("alternative")
msg["Subject"] = f"Today's News Summary (Test) - {datetime.now().strftime('%Y-%m-%d')}"
msg["From"] = sender_email
msg["To"] = receiver_email

# Get the absolute path to the email template
current_dir = os.path.dirname(os.path.abspath(__file__))
email_template_path = os.path.join(current_dir, "../static/email.html")


data = f'''

- **Bento Africa Temporarily Halts Operations**: Bento Africa has suspended its operations after rehiring staff to handle a backlog of tasks. This comes after the company faced protests over delayed January salaries.  
- **Marasoft Denies Fraud Allegations**: Marasoft has denied fraud allegations but failed to provide evidence, blaming "disgruntled" ex-employees for the claims.  
- **Nigerian Fintechs Revamp Operations**: Moniepoint, OPay, and PalmPay have improved their data collection and compliance measures following a 2024 ban.  
- **Lemfi Acquires Bureau Buttercrane**: Lemfi has completed the acquisition of Irish currency exchange Bureau Buttercrane, marking its entry into the European market.  
- **NIBSS Bets on QR Codes**: The Nigeria Inter-Bank Settlement System (NIBSS) is promoting QR codes as a cash alternative for small-value payments.  
- **Safaricom and Kenyan Banks Propose Pesalink**: Safaricom and Kenyan commercial banks are pushing for Pesalink to overhaul the national payment system.  
- **Moniepoint Mirrors Jack Dorsey’s Square**: Moniepoint has launched a new POS system inspired by Jack Dorsey’s Square.  
- **Stitch Acquires ExiPay**: South African fintech Stitch has acquired ExiPay to expand into in-person payments.

'''


# Read the HTML template and inject dynamic content
with open(email_template_path, "r") as file:
    html_content = file.read()
    
    # Example dynamic content array (replace with your actual data)
    # news_items = [
    #     {
    #         'headline': 'Bento Africa Temporarily Halts Operations',
    #         'description': 'Bento Africa has suspended its operations after rehiring staff...'
    #     },
    #     {
    #         'headline': 'Marasoft Denies Fraud Allegations',
    #         'description': 'Marasoft has denied fraud allegations but failed to provide evidence...'
    #     }
    # ]
    
    # Convert markdown data to news_items format
    news_items = []
    for line in data.strip().split('\n'):
        if line.startswith('- **'):
            # Split headline and description
            headline_end = line.find('**:')
            headline = line[4:headline_end]  # Remove '- **' from start
            description = line[headline_end+3:].strip()  # Remove '**: ' and trim
            news_items.append({
                'headline': headline,
                'description': description
            })
    
    # Find the content div and inject dynamic content
    content_div_start = html_content.find('<div class="content">')
    content_div_end = html_content.find('</div>', content_div_start)
    
    # Add header
    new_header = f'''<div class="header"> 
    <h1>News Summary for {datetime.now().strftime('%A, %dth %B, %Y')}</h1>
    </div>'''
    
    
    # Build new content HTML
    new_content = '<div class="content">'
    for item in news_items:
        new_content += f'''
        <div class="headline">Headline: {item['headline']}</div>
        <div class="description">{item['description']}</div>
        <br>
        '''
    new_content += '</div>'
    
    # Replace original content with new content
    html_content = html_content[:content_div_start] + new_header + new_content + html_content[content_div_end:]
     
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