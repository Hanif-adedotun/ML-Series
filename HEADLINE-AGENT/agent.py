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
import json
from langchain_core.messages import AnyMessage, HumanMessage, SystemMessage, ToolMessage, BaseMessage

from firecrawl import FirecrawlApp
from datetime import datetime

from langgraph.prebuilt import ToolNode
from langgraph.graph import StateGraph, MessagesState, START, END

from pydantic import BaseModel, Field
from typing import List


from test_files.send_email import send_news_email

TAVILY_API_KEY = os.environ['TAVILY_API_KEY']
GROQ_API_KEY = os.environ['GROQ_KEY']
GNEWS_API_KEY = os.environ['GNEWS_KEY']
FIRE_CRAWL_KEY= os.environ['FIRE_CRAWL_KEY']

class HeadlineItem(BaseModel):
     headline: str = Field(description="The news headline")
     description: str = Field(description="A brief description of the news")

class HeadlineResponse(BaseModel):
    items: List[HeadlineItem] = Field(description="List of news headlines with descriptions")


@tool
def get_technology_news(query: str) -> list:
    """Get the latest technology news headlines from Techcabal"""
    app = FirecrawlApp(api_key=FIRE_CRAWL_KEY)
    crawl_result = app.crawl_url('https://techcabal.com', params={
        'limit': 2,
        'maxDepth': 5,
        'includePaths': [ datetime.now().strftime('%Y/%m/%d') ],
        'scrapeOptions': {
            'formats': [ 'markdown'],
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
    return ' '.join(result)

# system prompt is used to inform the tools available to when to use each
SYSTEM_PROMPT = """Act as a helpful assistant.
    Use the tools at your disposal to perform tasks as needed.
        - get_technology_news: whenever user asks to get the latest technology headline.
        - search_web: whenever user asks for information on current events or if you don't know the answer.
    Use the tools only if you don't know the answer.
    Always respond with structured data in the format: 
    - headline: The news headline
    - description: A brief description of the news
    
    IMPORTANT
    - Ensure your response is not generic, add important information to the headlines.
    - Retain important infomation of the headline, e.g Company Name, Product name, Country, these are IMPORTANT DETAILS
    """
    
     
@tool
def search_web(query: str) -> list:
    """Search the web for a query"""
    tavily_search = TavilySearchResults(api_key=TAVILY_API_KEY, max_results=2, search_depth='advanced', max_tokens=1000)
    results = tavily_search.invoke(query)
    return results

llm = ChatGroq(
    api_key=GROQ_API_KEY,
    model="llama-3.3-70b-versatile")

tools = [search_web, get_technology_news]
llm_with_tools = llm.bind_tools(tools, tool_choice="auto").with_structured_output(HeadlineResponse)

tool_node = ToolNode(tools)

def call_model(state: MessagesState):
     messages = state["messages"]
     messages = [SystemMessage(content=SYSTEM_PROMPT)] + messages
     response = llm_with_tools.invoke(messages)
     # Convert HeadlineResponse to a HumanMessage
     formatted_response = "Today's Technology Headlines:\n\n"
     for item in response.items:
         formatted_response += f"• {item.headline}\n   {item.description}\n\n"
     return {"messages": [HumanMessage(content=formatted_response)]}

def call_tools(state: MessagesState) -> Literal["tools", END]:
    messages = state["messages"]
    last_message = messages[-1]
    # Check if the message has tool_calls attribute and if it has any calls
    if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
        return "tools"
    return END

def email_sender(state):
     print('Email Sender')
     last_message = state['messages'][-1]
    
     if isinstance(last_message.content, str):
        email_content = last_message.content
        if email_content is None:
            print('No email content to send')
            return
        print('Email content:', email_content)
        # Parse the email content into structured format
        headlines = []
        current_headline = None
        current_description = None
        
        for line in email_content.split('\n'):
            line = line.strip()
            if line.startswith('•'):
                # If we have a previous headline, save it
                if current_headline and current_description:
                    headlines.append({
                        "headline": current_headline,
                        "description": current_description.strip()
                    })
                # Start new headline
                parts = line[1:].strip().split('\n')
                current_headline = parts[0].strip()
                current_description = ""
            elif line and current_headline:
                current_description += line + " "
        
        # Add the last headline if exists
        if current_headline and current_description:
            headlines.append({
                "headline": current_headline,
                "description": current_description.strip()
            })
        
        # Send email with structured data
        print("headlines", headlines)
        send_news_email({
          "items": headlines})
     else:
         print('No formatted response available for email sending')
    
             

# initialize the workflow from StateGraph
workflow = StateGraph(MessagesState)

# add a node named LLM, with call_model function. This node uses an LLM to make decisions based on the input given
workflow.add_node("LLM", call_model)

# Add send email edge
workflow.add_node('email_sender', email_sender)

# Our workflow starts with the LLM node
workflow.add_edge(START, "LLM")

# Add a tools node
workflow.add_node("tools", tool_node)

# Add a conditional edge from LLM to call_tools function. It can go tools node or end depending on the output of the LLM. 
workflow.add_conditional_edges("LLM", call_tools)

# tools node sends the information back to the LLM
workflow.add_edge("tools", "LLM")

# Structure response from LLM to email sender
workflow.add_edge("LLM", "email_sender")

# Email sender till end
workflow.add_edge('email_sender', END)

agent = workflow.compile()

print(agent.get_graph().draw_mermaid())

for chunk in agent.stream(
    {"messages": [("user", "What are the top 10 latest technology headlines today? Generate a user readable response")]},
    stream_mode="values",):
    chunk["messages"][-1].pretty_print()
    