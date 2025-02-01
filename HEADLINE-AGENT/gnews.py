import json
import requests

apikey="bd0bb534703f15911f28967f7ff1b1bd"
category="technology"
# general, world, nation, business, technology, entertainment, sports, science and health
url = f"https://gnews.io/api/v4/top-headlines?category={category}&lang=en&country=us&max=10&apikey={apikey}"

response = requests.get(url)
data = response.json()
articles = data["articles"]
    
print(len(articles))

for i in range(len(articles)):
     # articles[i].title
     print(f"Title: {articles[i]['title']}")
     # articles[i].description
     print(f"Description: {articles[i]['description']}")
     # You can replace {property} below with any of the article properties returned by the API.
     # articles[i].{property}
     print(f"Content:  {articles[i]['content']}")

     # Delete this line to display all the articles returned by the request. Currently only the first article is displayed.
     break