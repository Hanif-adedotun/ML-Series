import os
from dotenv import load_dotenv
load_dotenv('.env')

from firecrawl import FirecrawlApp
from datetime import datetime
FIRE_CRAWL_KEY= os.environ['FIRE_CRAWL_KEY']
app = FirecrawlApp(api_key=FIRE_CRAWL_KEY)


crawl_result = app.crawl_url('https://techcabal.com', params={
     'limit': 1,
     'maxDepth': 1,
     'includePaths': [ datetime.now().strftime('%Y/%m/%d') ],
     'scrapeOptions': {
          'formats': [ 'markdown' ],
     }
})
data = crawl_result['data'][0]
# Split markdown content into lines and take first 20
markdown_lines = data['markdown'].split('\n')

# Extract sections starting with # startups and # FinTech
result = []
start_collecting = False
for line in markdown_lines:
    if line.startswith('# startups') or line.startswith('# FinTech'):
        start_collecting = True
    if start_collecting:
        result.append(line)
        if line.startswith('#') and not (line.startswith('# startups') or line.startswith('# FinTech')):
            break
       
print(' '.join(result))

# Here are the latest technology headlines from TechCabal:

# - **Bento Africa Temporarily Halts Operations**: Bento Africa has suspended its operations after rehiring staff to handle a backlog of tasks. This comes after the company faced protests over delayed January salaries.  
# - **Marasoft Denies Fraud Allegations**: Marasoft has denied fraud allegations but failed to provide evidence, blaming "disgruntled" ex-employees for the claims.  
# - **Nigerian Fintechs Revamp Operations**: Moniepoint, OPay, and PalmPay have improved their data collection and compliance measures following a 2024 ban.  
# - **Lemfi Acquires Bureau Buttercrane**: Lemfi has completed the acquisition of Irish currency exchange Bureau Buttercrane, marking its entry into the European market.  
# - **NIBSS Bets on QR Codes**: The Nigeria Inter-Bank Settlement System (NIBSS) is promoting QR codes as a cash alternative for small-value payments.  
# - **Safaricom and Kenyan Banks Propose Pesalink**: Safaricom and Kenyan commercial banks are pushing for Pesalink to overhaul the national payment system.  
# - **Moniepoint Mirrors Jack Dorsey’s Square**: Moniepoint has launched a new POS system inspired by Jack Dorsey’s Square.  
# - **Stitch Acquires ExiPay**: South African fintech Stitch has acquired ExiPay to expand into in-person payments.  