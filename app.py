import streamlit as st
import os
import requests
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain
from langchain.memory import ConversationBufferMemory
from langchain.agents import load_tools
from langchain.agents import initialize_agent
from dotenv import load_dotenv

from llama_index import SimpleDirectoryReader
from llama_index import GPTVectorStoreIndex
import llama_index
from llama_index import GPTVectorStoreIndex, TwitterTweetReader

load_dotenv()
print(os.getenv('OPENAI_API_KEY'))
os.getenv('OPENAI_API_KEY')
st.title("Llama Press")
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Welcome to Llama Press, How may I help you?"):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

def chat(p):
    query = p
    reader = TwitterTweetReader(os.getenv('BEARER_TOKEN'))
    documents = reader.load_data(["ANI"])
    documents1 = reader.load_data(["ZeeNews"])
    documents2 = reader.load_data(["TV9Bharatvarsh"])
    documents3 = reader.load_data(["Republic_Bharat"])
    documents4 = reader.load_data(["AajTak"])
    
    agent = llama_index.GPTVectorStoreIndex.from_documents(documents1+documents+documents2+documents3+documents4)
    chat_engine = agent.as_chat_engine(verbose=True)
    response = chat_engine.chat(query)
    return response

result = chat(prompt)
response = f"Echo: {result}"
with st.chat_message("assistant"):
    st.markdown(response)
st.session_state.messages.append({"role": "assistant", "content": response})