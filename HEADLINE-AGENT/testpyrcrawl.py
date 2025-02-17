import os
from dotenv import load_dotenv
load_dotenv('.env')

from firecrawl import FirecrawlApp
from datetime import datetime
FIRE_CRAWL_KEY= os.environ['FIRE_CRAWL_KEY']
app = FirecrawlApp(api_key=FIRE_CRAWL_KEY)

from test_files.send_email import send_news_email

test_data = '''
Here are the latest technology headlines from TechCabal:

1. **Bento Africa Temporarily Halts Operations After Rehiring Staff to Handle Backlog**  
   - Bento Africa has temporarily shut down operations after rehiring staff to address a backlog of issues. This comes after the company faced protests over delayed January salaries.  

2. **Marasoft Denies Fraud Allegations but Fails to Provide Evidence**  
   - Marasoft has denied fraud allegations but has not shared any evidence to support its claims. The company has instead blamed "disgruntled" ex-employees for the allegations.  

3. **Nigerian Fintechs Revamp Operations with Better Data Collection and Compliance**  
   - Moniepoint, OPay, and PalmPay have improved their data collection and compliance measures in response to the 2024 ban on unlicensed fintech operations in Nigeria.  

4. **Lemfi Completes Acquisition of Bureau Buttercrane, Expands into Europe**  
   - Lemfi has acquired Irish currency exchange company Bureau Buttercrane, marking its entry into the European market.  

5. **NIBSS Bets on QR Codes for Small-Value Payments**  
   - The Nigeria Inter-Bank Settlement System (NIBSS) is promoting QR codes as a cash alternative for small-value payments.  

6. **Safaricom and Kenyan Banks Propose Pesalink for National Payments Overhaul**  
   - Safaricom and Kenyan commercial banks have proposed the use of Pesalink for a national payments overhaul in Kenya.  

7. **Moniepoint Unveils New POS Device Inspired by Jack Dorsey’s Square**  
   - Moniepoint has launched a new POS device that mirrors Jack Dorsey’s Square, aiming to enhance payment solutions in Nigeria.  

8. **Stitch Acquires ExiPay to Expand into In-Person Payments**  
   - South African fintech company Stitch has acquired ExiPay to expand its services into in-person payments.  

These are the latest developments in the technology and fintech sectors across Africa. Let me know if you'd like more details on any of these stories!
'''


send_news_email(test_data)

# crawl_result = app.crawl_url('https://techcabal.com', params={
#      'limit': 1,
#      'maxDepth': 1,
#      'includePaths': [ datetime.now().strftime('%Y/%m/%d') ],
#      'scrapeOptions': {
#           'formats': [ 'markdown' ],
#      }
# })
# data = crawl_result['data'][0]
# # Split markdown content into lines and take first 20
# markdown_lines = data['markdown'].split('\n')

# # Extract sections starting with # startups and # FinTech
# result = []
# start_collecting = False
# for line in markdown_lines:
#     if line.startswith('# startups') or line.startswith('# FinTech'):
#         start_collecting = True
#     if start_collecting:
#         result.append(line)
#         if line.startswith('#') and not (line.startswith('# startups') or line.startswith('# FinTech')):
#             break
       
# print(' '.join(result))

# Here are the latest technology headlines from TechCabal:

# - **Bento Africa Temporarily Halts Operations**: Bento Africa has suspended its operations after rehiring staff to handle a backlog of tasks. This comes after the company faced protests over delayed January salaries.  
# - **Marasoft Denies Fraud Allegations**: Marasoft has denied fraud allegations but failed to provide evidence, blaming "disgruntled" ex-employees for the claims.  
# - **Nigerian Fintechs Revamp Operations**: Moniepoint, OPay, and PalmPay have improved their data collection and compliance measures following a 2024 ban.  
# - **Lemfi Acquires Bureau Buttercrane**: Lemfi has completed the acquisition of Irish currency exchange Bureau Buttercrane, marking its entry into the European market.  
# - **NIBSS Bets on QR Codes**: The Nigeria Inter-Bank Settlement System (NIBSS) is promoting QR codes as a cash alternative for small-value payments.  
# - **Safaricom and Kenyan Banks Propose Pesalink**: Safaricom and Kenyan commercial banks are pushing for Pesalink to overhaul the national payment system.  
# - **Moniepoint Mirrors Jack Dorsey’s Square**: Moniepoint has launched a new POS system inspired by Jack Dorsey’s Square.  
# - **Stitch Acquires ExiPay**: South African fintech Stitch has acquired ExiPay to expand into in-person payments.  