import os
from dotenv import load_dotenv
load_dotenv('.env')

GROQ_API_KEY = os.environ['GROQ_KEY']

from langchain_groq import ChatGroq

llm = ChatGroq(
    api_key=GROQ_API_KEY,
    model="deepseek-r1-distill-llama-70b")

print(llm)


# Install with pip install firecrawl-py
from firecrawl import FirecrawlApp

app = FirecrawlApp(api_key='fc-3b033f2de61649cc88361e30c82b27d8')

crawl_result = app.crawl_url('https://techcabal.com', params={
'limit': 10,
'maxDepth': 5,
'includePaths': [ '2025/02/05' ],
'scrapeOptions': {
	'formats': [ 'markdown' ],
  }
})

# returns { "jobId": "1234-5678-9101" }

# Check crawl status
# status = app.check_crawl_status(job_id)

# 200 - PENDING
# {
#     "status": "scraping", // Status of the job (scraping, completed, failed,cancelled)
#     "totalCount": 22, // Total number of pages
#     "creditsUsed": 17, // Total number of credits used
#     "expiresAt": "2024-01-01", // Date when the job expires
#     "next": "http://api.firecrawl.dev/v1/crawl/123-456?skip=17", // Next URL to fetch more results
#     "data": null // Data returned from the job (null when it is in progress)
# }

# 200 - SUCCESS
# {
#     "status": "completed",
#     "totalCount": 22,
#     "creditsUsed": 22,
#     "expiresAt": "2024-01-01",
#     "data": [
#         {
#           "markdown": "# Markdown Content",
#           "metadata": {
#               "title": "Mendable | AI for CX and Sales",
#               "description": "AI for CX and Sales",
#               "language": null,
#               "sourceURL": "https://www.mendable.ai/",
#               "statusCode": 200, // HTTP status code,
#               "error": "Error message", // (null if no error)
#         }
#     ]
# }
