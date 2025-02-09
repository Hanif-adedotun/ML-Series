import os
from dotenv import load_dotenv
load_dotenv('.env')

from firecrawl import FirecrawlApp
from datetime import datetime
FIRE_CRAWL_KEY= os.environ['FIRE_CRAWL_KEY']
app = FirecrawlApp(api_key=FIRE_CRAWL_KEY)
crawl_result = app.crawl_url('https://techcabal.com', params={
     'limit': 2,
     'maxDepth': 1,
     'includePaths': [ datetime.now().strftime('%Y/%m/%d') ],
     'scrapeOptions': {
          'formats': [ 'markdown' ],
     }
})
data = crawl_result['data'][0]
print(data['markdown'])

