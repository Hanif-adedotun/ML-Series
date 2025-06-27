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
    receiver_emails = os.environ['RECEIVER_EMAIL'].split(',')
    password = os.environ['PASSWORD']

    # Create the email message
    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"Today's News Summary new - {datetime.now().strftime('%Y-%m-%d')}"
    msg["From"] = sender_email
    msg["To"] = ', '.join(receiver_emails)  # Join emails for the "To" header

    # Get the absolute path to the email template
    current_dir = os.path.dirname(os.path.abspath(__file__))
    email_template_path = os.path.join(current_dir, "../static/email.html")

    # Use provided data or default test data
    data = news_data 

    # Read the HTML template and inject dynamic content
    with open(email_template_path, "r") as file:
        html_content = file.read()
        
        # Find the content div and inject dynamic content
        content_div_start = html_content.find('<div class="content">')
        content_div_end = html_content.find('</div>', content_div_start)
        
        # Add header
        new_header = f'''<div class="date"> 
        <p>News Summary for {datetime.now().strftime('%A, %dth %B, %Y')}</p>
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
        server.sendmail(sender_email, receiver_emails, msg.as_string())
        print("Email sent successfully!")
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False
    finally:
        server.quit()
        
if __name__ == "__main__":   
    headlines = [{'headline': 'New AI Model Released', 'description': 'A new AI model has been released, capable of learning and adapting at an unprecedented rate.'}, {'headline': 'Breakthrough in Quantum Computing', 'description': 'Scientists have made a major breakthrough in quantum computing, paving the way for faster and more secure processing.'}, {'headline': '5G Networks Expand Globally', 'description': '5G networks are expanding globally, providing faster and more reliable internet connectivity to millions of people.'}]
    send_news_email({
            "items": headlines})