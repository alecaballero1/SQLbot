# main_streamlit_script.py

#libraries needed
import streamlit as st
from langchain.sql_database import SQLDatabase
from langchain.llms import OpenAI
from langchain_experimental.sql import SQLDatabaseChain
from langchain.prompts import PromptTemplate
from langchain.prompts.chat import HumanMessagePromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from langchain.prompts import PromptTemplate
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.memory import ConversationBufferMemory
from langchain.agents.agent_types import AgentType
from langchain.agents import create_sql_agent
from openai import OpenAI
import streamlit as st
import pandas as pd

def main():
    st.set_page_config(page_title="Chat with your sql!", page_icon=":cake:")

    st.header("Chat with your sql files :cake:")
    user_input = st.text_input("Ask a question about your file ✩°｡ ⋆⸜ ✮")

    uploaded_file = st.file_uploader("Upload your SQL file", type=["sql"])

    if uploaded_file is not None:
        st.button("Process")

    # Inicia el chat bot
    api_key = st.secrets["OPENAI_API_KEY"]
    

    # Lógica de interacción con el bot
    if user_input:
        st.write("Bot: Welcome, ask questions right away! Type 'exit' to end the chat.")
        convo = []
        
        context_m = chat_bot.retrieve_context(user_input)

        # Prompt and user message 
        prompt = f"""You are a data analysis specialist checking a SQL file.
        You have to answer user's doubts and questions, as well as providing relevant information.
        If you dont know, just say you dont know. Be precise!
        {context_m}
        Question: {user_input}
        Answer:"""

        convo.append({'role': 'system', 'content': prompt})
        convo.append({'role': 'user', 'content': user_input})

        # Conversation with the model
        answer = chat_bot.get_completion(prompt)
        st.write(f"Bot: {answer}")

if __name__ == "__main__":
    main()
