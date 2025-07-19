# News Headlines Agent - Streamlit App

A Streamlit application that fetches the latest technology news headlines and allows users to send them via email with custom credentials.

## Features

- 🔍 **Real-time News**: Fetches latest technology news from Techcabal
- 🌐 **Web Search**: Searches the web for current events and information
- 📧 **Email Integration**: Send news headlines via email with custom SMTP settings
- 🎨 **Beautiful UI**: Modern, responsive Streamlit interface
- 📊 **Multiple Recipients**: Send to multiple email addresses
- 🔐 **Secure**: Custom email credentials (no hardcoded secrets)

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Environment Variables

Create a `.env` file in the project root with the following variables:

```env
TAVILY_API_KEY=your_tavily_api_key
GROQ_KEY=your_groq_api_key
GNEWS_KEY=your_gnews_api_key
FIRE_CRAWL_KEY=your_firecrawl_api_key
```

### 3. Run the Streamlit App

```bash
streamlit run streamlit.py
```

The app will open in your browser at `http://localhost:8501`

## How to Use

### 1. Configure Email Settings (Sidebar)

- **SMTP Server**: Enter your email provider's SMTP server
  - Gmail: `smtp.gmail.com`
  - Outlook: `smtp-mail.outlook.com`
  - Yahoo: `smtp.mail.yahoo.com`
- **SMTP Port**: Usually `587` for TLS or `465` for SSL
- **Sender Email**: Your email address
- **Password/App Password**: Your email password or app password
- **Receiver Emails**: Enter email addresses (one per line)

### 2. Fetch News

- Enter your query in the text area
- Click "🚀 Get News Headlines" to fetch latest technology news
- View the results in the main area

### 3. Send Email

- After fetching news, click "📧 Send Email" to send the headlines
- The email will be sent using your configured SMTP settings

## Email Configuration Tips

### Gmail Setup

1. Enable 2-factor authentication
2. Generate an App Password
3. Use `smtp.gmail.com` with port `587`
4. Use the App Password instead of your regular password

### Outlook Setup

1. Use `smtp-mail.outlook.com` with port `587`
2. Use your regular email password

### Security Best Practices

- Use App Passwords instead of regular passwords
- Don't share your credentials
- Consider using environment variables for sensitive data

## Features

- **Real-time Technology News**: Fetches from Techcabal
- **Web Search Integration**: Searches for current events
- **Beautiful HTML Email Templates**: Professional-looking emails
- **Multiple Recipient Support**: Send to multiple email addresses
- **Error Handling**: Comprehensive error messages
- **Responsive Design**: Works on desktop and mobile

## File Structure

```
HEADLINE-AGENT/
├── streamlit.py          # Main Streamlit application
├── agent.py              # News agent with LangGraph
├── requirements.txt      # Python dependencies
├── .env                  # Environment variables (create this)
├── static/
│   └── email.html       # Email template
└── test_files/
    └── send_email.py    # Email sending utilities
```

## Troubleshooting

### Common Issues

1. **Email Authentication Failed**

   - Check your SMTP settings
   - Ensure you're using the correct password/app password
   - Verify your email provider's SMTP settings

2. **API Key Errors**

   - Ensure all API keys are set in `.env` file
   - Check that API keys are valid and have sufficient credits

3. **Import Errors**
   - Install all dependencies: `pip install -r requirements.txt`
   - Ensure you're in the correct directory

### Getting API Keys

- **Tavily**: Sign up at [tavily.com](https://tavily.com)
- **Groq**: Sign up at [groq.com](https://groq.com)
- **GNews**: Sign up at [gnews.io](https://gnews.io)
- **Firecrawl**: Sign up at [firecrawl.dev](https://firecrawl.dev)

## License

This project is open source and available under the MIT License.
