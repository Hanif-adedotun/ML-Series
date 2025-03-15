import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from datetime import datetime
from dotenv import load_dotenv

def send_news_email(news_data):
    """
    Send an email with news summary.
    
    Args:
        news_data (str): Markdown formatted news data. If None, uses default test data.
    """
    load_dotenv('../.env')
    
    smtp_server = os.environ['SMTP_KEY']
    smtp_port = int(os.environ['SMTP_PORT'])
    sender_email = os.environ['SENDER_EMAIL']
    receiver_email = os.environ['RECEIVER_EMAIL']
    password = os.environ['PASSWORD']

    # Create the email message
    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"Today's News Summary (test 2) - {datetime.now().strftime('%Y-%m-%d')}"
    msg["From"] = sender_email
    msg["To"] = receiver_email

    # Get the absolute path to the email template
    current_dir = os.path.dirname(os.path.abspath(__file__))
    email_template_path = os.path.join(current_dir, "../static/email.html")

    # Use provided data or default test data
    data = news_data 
    
    test_data = '''
    - **Bento Africa Temporarily Halts Operations**: Bento Africa has suspended its operations after rehiring staff to handle a backlog of tasks. This comes after the company faced protests over delayed January salaries.  
    - **Marasoft Denies Fraud Allegations**: Marasoft has denied fraud allegations but failed to provide evidence, blaming "disgruntled" ex-employees for the claims.  
    - **Nigerian Fintechs Revamp Operations**: Moniepoint, OPay, and PalmPay have improved their data collection and compliance measures following a 2024 ban.  
    - **Lemfi Acquires Bureau Buttercrane**: Lemfi has completed the acquisition of Irish currency exchange Bureau Buttercrane, marking its entry into the European market.  
    - **NIBSS Bets on QR Codes**: The Nigeria Inter-Bank Settlement System (NIBSS) is promoting QR codes as a cash alternative for small-value payments.  
    - **Safaricom and Kenyan Banks Propose Pesalink**: Safaricom and Kenyan commercial banks are pushing for Pesalink to overhaul the national payment system.  
    - **Moniepoint Mirrors Jack Dorsey's Square**: Moniepoint has launched a new POS system inspired by Jack Dorsey's Square.  
    - **Stitch Acquires ExiPay**: South African fintech Stitch has acquired ExiPay to expand into in-person payments.
    '''

    # Read the HTML template and inject dynamic content
    with open(email_template_path, "r") as file:
        html_content = file.read()
        
        # Find the content div and inject dynamic content
        content_div_start = html_content.find('<div class="content">')
        content_div_end = html_content.find('</div>', content_div_start)
        
        # Add header
        new_header = f'''<div class="header"> 
        <h1>News Summary for {datetime.now().strftime('%A, %dth %B, %Y')}</h1>
        </div>'''
        
        # Build new content HTML
        new_content = '<div class="content">'
        for item in news_data['items']:
            new_content += f'''
            <div class="headline">{item['headline']}</div>
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
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        print("Email sent successfully!")
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False
    finally:
        server.quit()