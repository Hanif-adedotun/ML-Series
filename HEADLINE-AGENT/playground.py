import os
from dotenv import load_dotenv
load_dotenv('.env')

GROQ_API_KEY = os.environ['GROQ_KEY']

from langchain_groq import ChatGroq

llm = ChatGroq(
    api_key=GROQ_API_KEY,
    model="deepseek-r1-distill-llama-70b")

print(llm)