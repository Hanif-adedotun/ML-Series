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
def get_technology_news(query: str) -> list:
     """Get the latest technology news headlines from GNews"""
     endpoint = f"https://gnews.io/api/v4/top-headlines?category=technology&lang=en&country=us&max=10&apikey={GNEWS_API_KEY}"
     response = requests.get(endpoint)
     if response.status_code == 200:
          return response.json().get('articles', [])
     return []

@tool
def get_business_news(query: str) -> list:
     """Get the latest business news headlines from GNews"""
     endpoint = f"https://gnews.io/api/v4/top-headlines?category=business&lang=en&country=us&max=10&apikey={GNEWS_API_KEY}"
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

tools = [search_web, get_technology_news, get_business_news]
llm_with_tools = llm.bind_tools(tools)


# system prompt is used to inform the tools available to when to use each
system_prompt = """Act as a helpful assistant.
    Use the tools at your disposal to perform tasks as needed.
        - get_technology_news: whenever user asks to get the latest technology headline.
        - get_business_news: whenever user asks to get the latest business headline.
        - search_web: whenever user asks for information on current events or if you don't know the answer.
    Use the tools only if you don't know the answer.
    """
    
# we can initialize the agent using the llama3 model, tools, and system prompt.
agent = create_react_agent(model=llm, tools=tools, state_modifier=system_prompt)

# Lets query the agent to see the result.
def print_stream(stream):
    for s in stream:
        message = s["messages"][-1]
        if isinstance(message, tuple):
            print(message)
        else:
            message.pretty_print()

inputs = {"messages": [("user", "What is the latest business and technology headlines today")]}

print_stream(agent.stream(inputs, stream_mode="values"))