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

from langgraph.prebuilt import ToolNode
from langgraph.graph import StateGraph, MessagesState, START, END

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
tool_node = ToolNode(tools)

llm_with_tools = llm.bind_tools(tools)

def call_model(state: MessagesState):
     messages = state["messages"]
     response = llm_with_tools.invoke(messages)
     return {"messages": [response]}

def call_tools(state: MessagesState) -> Literal["tools", END]:
    messages = state["messages"]
    last_message = messages[-1]
    if last_message.tool_calls:
        return "tools"
    return END

# initialize the workflow from StateGraph
workflow = StateGraph(MessagesState)

# add a node named LLM, with call_model function. This node uses an LLM to make decisions based on the input given
workflow.add_node("LLM", call_model)

# Our workflow starts with the LLM node
workflow.add_edge(START, "LLM")

# Add a tools node
workflow.add_node("tools", tool_node)

# Add a conditional edge from LLM to call_tools function. It can go tools node or end depending on the output of the LLM. 
workflow.add_conditional_edges("LLM", call_tools)

# tools node sends the information back to the LLM
workflow.add_edge("tools", "LLM")

agent = workflow.compile()

for chunk in agent.stream(
    {"messages": [("user", "What is the latest business and technology headlines today?")]},
    stream_mode="values",):
    chunk["messages"][-1].pretty_print()