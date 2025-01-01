from newsapi import NewsApiClient
import os
import json  
import pandas as pd

key = os.getenv("NEWS_API")

# Init
newsapi = NewsApiClient(api_key='566e831cc7ab45798bc6275b82b081b8')

# get_sources = newsapi.get_sources()
# with open('dataset/news_sources.json', 'w') as json_file:
#     json.dump(get_sources, json_file)

all_articles = newsapi.get_everything(q='bitcoin',
                                      sources='bbc-news,the-verge',
                                      from_param='2024-12-01',
                                      to='2024-12-30',
                                      language='en',
                                      sort_by='relevancy',)



articles = all_articles['articles']
results = []

for article in articles:
    title = article.get('title', '')
    description = article.get('description', '')
    content = article.get('content', '')
    published_at = article.get('publishedAt', '')

    results.append({
        "title": title,
        "description": description,
        "content": content,
        "publishedAt": published_at
    })

df = pd.DataFrame(results)
df.to_csv('./dataset/newsapi_articles.csv', index=False)
