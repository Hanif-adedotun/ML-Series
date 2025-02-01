# Import the keys
import os
from dotenv import load_dotenv
load_dotenv('.env')

# Import the required libraries and methods
import requests
from typing import List, Literal
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.tools import tool
from langchain_groq import ChatGroq

from langgraph.prebuilt import create_react_agent

TAVILY_API_KEY = os.environ['TAVILY_API_KEY']
GROQ_API_KEY = os.environ['GROQ_KEY']
GNEWS_API_KEY = os.environ['GNEWS_KEY']

@tool
def get_news(query: str) -> list:
     """Get the latest technology news headlines from GNews"""
     endpoint = f"https://gnews.io/api/v4/top-headlines?category=technology&lang=en&country=us&max=10&apikey={apikey}"
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

llm = ChatGroq(
    api_key=GROQ_API_KEY,
    model="deepseek-r1-distill-llama-70b")

tools = [search_web, get_news]
llm_with_tools = llm.bind_tools(tools)

prompt = """
    Given only the tools at your disposal, mention tool calls for the following tasks:
    Do not change the query given for any search tasks
        1. Get the latest technology news headlines
        2. Find recent business news updates
        3. Search for the most important tech industry developments this week
        4. Look up recent mergers and acquisitions in the tech sector
    """

results = llm_with_tools.invoke(prompt)

print(results.tool_calls)

query = "Get the latest technology news headlines"
response = llm.invoke(query)
print(response.content)