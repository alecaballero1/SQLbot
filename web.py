# main_streamlit_script.py

import streamlit as st
from chat_bot import ChatBot

import streamlit as st
from chat_bot import ChatBot

def main():
    st.set_page_config(page_title="Chat with your sql!", page_icon=":cake:")

    st.header("Chat with your sql files :cake:")
    user_input = st.text_input("Ask a question about your file ✩°｡ ⋆⸜ ✮")

    uploaded_file = st.file_uploader("Upload your SQL file", type=["sql"])

    if uploaded_file is not None:
        # Procesar el archivo SQL y utilizarlo como base de datos
        sql_content = uploaded_file.read().decode("utf-8")

        # Inicia el chat bot con el contenido del archivo SQL
        chat_bot = ChatBot(sql_content)

        st.button("Process")

        # Resto de la lógica de interacción con el bot...
    else:
        st.warning("Please upload an SQL file.")

if __name__ == "__main__":
    main()
