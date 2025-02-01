# Import the keys
import os
from dotenv import load_dotenv
load_dotenv('.env')

# Import the required libraries and methods
import requests
from typing import List, Literal
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI

TAVILY_API_KEY = os.environ['TAVILY_API_KEY']
GROQ_API_KEY = os.environ['GROQ_KEY']
GNEWS_API_KEY = os.environ['GNEWS_KEY']

@tool
def get_news(query: str) -> list:
     endpoint = f"https://gnews.io/api/v4/top-headlines?category={query}&lang=en&country=us&max=10&apikey={apikey}"
     response = requests.get(endpoint)
     if response.status_code == 200:
          return response.json().get('articles', [])
     return []
     
@tool
def search_web(query: str) -> list:
    """Search the web for a query"""
    tavily_search = TavilySearchResults(api_key=TAVILY_API_KEY, max_results=2, search_depth='advanced', max_tokens=1000)
    results = tavily_search.invoke(query)
    return results