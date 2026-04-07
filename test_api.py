import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

llm = ChatOpenAI(model_name="gpt-4o-mini")

response = llm.invoke("Hello, how are you?")
print(response.content)