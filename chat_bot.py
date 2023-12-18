# chat_bot.py

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

api_key = st.secrets["OPENAI_API_KEY"]
class ChatBot:
    def __init__(self, api_key, use_database=False, db_uri=None, sql_file=None):
        self.client = OpenAI(api_key=api_key)
        llm_name = "gpt-3.5-turbo"
        self.llm = ChatOpenAI(api_key=api_key, model_name=llm_name, temperature=0)

    #database or localhost
    if use_database and db_uri:
            self.db = SQLDatabase.from_uri(db_uri)
            self.db_chain = SQLDatabaseChain(llm=self.llm, database=self.db, verbose=True)
        elif sql_file:
            self.db = self.load_sql_file(sql_file)
            self.db_chain = SQLDatabaseChain(llm=self.llm, database=self.db, verbose=True)
        else:
            self.db = None
            self.db_chain = None

    #load sql file
    def load_sql_file(self, sql_file):
        try:
            df = pd.read_sql(sql_file, con=self.db.engine)
            db = SQLDatabase(data=df)
            return db
            
    def retrieve_context(self, query):
        db_context = self.db_chain(query)
        return db_context['result'].strip()

    def get_completion(self, prompt, model="gpt-3.5-turbo"):
        messages = [{"role": "user", "content": prompt}]
        response = self.client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=50,
            temperature=0
        )
        return response.choices[0].message.content

