import streamlit as st
import os
from dotenv import load_dotenv
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
import tempfile
import json

# Import the agent functionality
from agent import agent, HeadlineResponse, HeadlineItem

# Load environment variables
load_dotenv('.env')

# Page configuration
st.set_page_config(
    page_title="News Headlines Agent",
    page_icon="📰",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 1.5rem;
        color: #2c3e50;
        margin-bottom: 1rem;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .error-box {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .info-box {
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def send_email_with_custom_credentials(news_data, smtp_server, smtp_port, sender_email, password, receiver_emails):
    """
    Send email with custom credentials provided by the user
    """
    try:
        # Create the email message
        msg = MIMEMultipart("alternative")
        msg["Subject"] = f"Today's Technology News Summary - {datetime.now().strftime('%Y-%m-%d')}"
        msg["From"] = sender_email
        msg["To"] = ', '.join(receiver_emails)

        # Get the email template path
        current_dir = os.path.dirname(os.path.abspath(__file__))
        email_template_path = os.path.join(current_dir, "static/email.html")

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
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_emails, msg.as_string())
        server.quit()
        
        return True, "Email sent successfully!"
        
    except Exception as e:
        return False, f"Failed to send email: {str(e)}"

def main():
    # Main header
    st.markdown('<h1 class="main-header">📰 News Headlines Agent</h1>', unsafe_allow_html=True)
    
    # Sidebar for email configuration
    st.sidebar.markdown("## 📧 Email Configuration")
    
    # Email settings
    smtp_server = st.sidebar.text_input("SMTP Server", value="smtp.gmail.com", help="e.g., smtp.gmail.com for Gmail")
    smtp_port = st.sidebar.number_input("SMTP Port", value=587, min_value=1, max_value=65535, help="Usually 587 for TLS or 465 for SSL")
    sender_email = st.sidebar.text_input("Sender Email", help="Your email address")
    password = st.sidebar.text_input("Password/App Password", type="password", help="Your email password or app password")
    
    # Receiver emails
    receiver_emails_input = st.sidebar.text_area(
        "Receiver Emails (one per line)", 
        help="Enter email addresses, one per line"
    )
    
    # Parse receiver emails
    receiver_emails = [email.strip() for email in receiver_emails_input.split('\n') if email.strip()] if receiver_emails_input else []
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<h2 class="section-header">🎯 Get Latest Technology News</h2>', unsafe_allow_html=True)
        
        # Query input
        query = st.text_area(
            "What would you like to know about?",
            value="What are the top 10 latest technology headlines today? Generate a user readable response",
            height=100,
            help="Ask for technology news, current events, or any information you need"
        )
        
        # Action buttons
        col1_1, col1_2 = st.columns(2)
        
        with col1_1:
            if st.button("🚀 Get News Headlines", type="primary", use_container_width=True):
                if not query.strip():
                    st.error("Please enter a query!")
                else:
                    with st.spinner("Fetching latest news headlines..."):
                        try:
                            # Run the agent
                            result = agent.invoke({
                                "messages": [("user", query)]
                            })
                            
                            # Extract the last message content
                            last_message = result["messages"][-1]
                            content = last_message.content
                            
                            # Store the result in session state
                            st.session_state.news_content = content
                            st.session_state.news_data = parse_news_content(content)
                            
                            st.success("News headlines fetched successfully!")
                            
                        except Exception as e:
                            st.error(f"Error fetching news: {str(e)}")
        
        with col1_2:
            if st.button("📧 Send Email", use_container_width=True):
                if 'news_data' not in st.session_state:
                    st.error("Please fetch news headlines first!")
                elif not all([smtp_server, smtp_port, sender_email, password, receiver_emails]):
                    st.error("Please fill in all email configuration fields!")
                else:
                    with st.spinner("Sending email..."):
                        success, message = send_email_with_custom_credentials(
                            st.session_state.news_data,
                            smtp_server,
                            smtp_port,
                            sender_email,
                            password,
                            receiver_emails
                        )
                        
                        if success:
                            st.success(message)
                        else:
                            st.error(message)
    
    with col2:
        st.markdown('<h3 class="section-header">📊 Quick Stats</h3>', unsafe_allow_html=True)
        
        if 'news_data' in st.session_state:
            st.metric("Headlines Found", len(st.session_state.news_data['items']))
            st.metric("Date", datetime.now().strftime('%Y-%m-%d'))
        else:
            st.info("No news data available yet")
    
    # Display results
    if 'news_content' in st.session_state:
        st.markdown('<h2 class="section-header">📰 Latest Headlines</h2>', unsafe_allow_html=True)
        
        # Display the formatted content
        st.markdown(st.session_state.news_content)
        
        # Show structured data
        with st.expander("📋 View Structured Data"):
            st.json(st.session_state.news_data)
    
    # Instructions and help
    with st.expander("ℹ️ How to use this app"):
        st.markdown("""
        ### Getting Started:
        1. **Configure Email Settings** (in sidebar):
           - Enter your SMTP server details
           - Provide your email credentials
           - Add recipient email addresses
        
        2. **Fetch News**:
           - Enter your query in the text area
           - Click "Get News Headlines" to fetch latest technology news
        
        3. **Send Email**:
           - After fetching news, click "Send Email" to send the headlines
        
        ### Email Configuration Tips:
        - **Gmail**: Use `smtp.gmail.com` with port `587`
        - **Outlook**: Use `smtp-mail.outlook.com` with port `587`
        - **Yahoo**: Use `smtp.mail.yahoo.com` with port `587`
        - Use App Passwords for better security
        
        ### Features:
        - Real-time technology news from Techcabal
        - Web search for current events
        - Beautiful HTML email templates
        - Multiple recipient support
        """)

def parse_news_content(content):
    """
    Parse the news content into structured format for email
    """
    headlines = []
    current_headline = None
    current_description = None
    
    for line in content.split('\n'):
        line = line.strip()
        if line.startswith('•'):
            # If we have a previous headline, save it
            if current_headline and current_description:
                headlines.append({
                    "headline": current_headline,
                    "description": current_description.strip()
                })
            # Start new headline
            parts = line[1:].strip().split('\n')
            current_headline = parts[0].strip()
            current_description = ""
        elif line and current_headline:
            current_description += line + " "
    
    # Add the last headline if exists
    if current_headline and current_description:
        headlines.append({
            "headline": current_headline,
            "description": current_description.strip()
        })
    
    return {"items": headlines}

if __name__ == "__main__":
    main()
