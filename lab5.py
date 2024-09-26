import streamlit as st
from openai import OpenAI
import tiktoken
import pdfplumber
import __main__
import sys
import os

__main__.__dict__['__sqlite3_for_python__'] = __import__('pysqlite3')
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions

def lab5():
    st.title("Course Information Chatbot")

    model_to_use = 'gpt-4'

    if 'client' not in st.session_state:
        api_key = st.secrets["my_api_key"]
        st.session_state.client = OpenAI(api_key=api_key)

    if 'messages' not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "Hi! How can I help you with course information today?"}]

    def count_tokens(messages):
        encoding = tiktoken.encoding_for_model(model_to_use)
        return sum([len(encoding.encode(message["content"])) for message in messages])

    def update_conversation_buffer(max_tokens):
        full_history = st.session_state.messages
        while count_tokens(full_history) > max_tokens and len(full_history) > 1:
            full_history.pop(0)
        st.session_state.messages = full_history

    def convert_pdf_to_text(pdf_file):
        text = ""
        with pdfplumber.open(pdf_file) as pdf:
            for page in pdf.pages:
                text += page.extract_text()
        return text

    def initialize_chromadb(pdf_files):
        if 'Lab4_vectorDB' not in st.session_state:
            persistent_dir = "chroma_db"
            if not os.path.exists(persistent_dir):
                os.makedirs(persistent_dir)
            
            chroma_client = chromadb.PersistentClient(path=persistent_dir)
            embedding_func = embedding_functions.OpenAIEmbeddingFunction(
                api_key=st.secrets["my_api_key"],
                model_name="text-embedding-ada-002"
            )
            
            try:
                collection = chroma_client.get_or_create_collection(name="Lab4Collection", embedding_function=embedding_func)
            except Exception as e:
                st.error(f"Error creating/getting collection: {e}")
                return None
            
            for pdf_file in pdf_files:
                text = convert_pdf_to_text(pdf_file)
                metadata = {"filename": pdf_file.name}
                collection.add(
                    documents=[text],
                    metadatas=[metadata],
                    ids=[pdf_file.name]
                )
            
            st.session_state.Lab4_vectorDB = collection
        return st.session_state.Lab4_vectorDB

    uploaded_files = st.sidebar.file_uploader("Upload PDF files", accept_multiple_files=True, type=["pdf"])
    
    if len(uploaded_files) == 7:
        st.sidebar.write("Creating ChromaDB with the uploaded PDFs...")
        collection = initialize_chromadb(uploaded_files)
        if collection:
            st.sidebar.success("ChromaDB initialized with 7 PDF files.")
        else:
            st.sidebar.error("Failed to initialize ChromaDB.")
            return
    else:
        st.sidebar.warning("Please upload exactly 7 PDF files to proceed.")
        return

    # Rest of your code (chat interface, etc.)
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("What would you like to know about the course?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Query ChromaDB
        try:
            results = st.session_state.Lab4_vectorDB.query(
                query_texts=[prompt],
                n_results=2
            )
            context = "\n".join(results['documents'][0])
        except Exception as e:
            st.error(f"Error querying ChromaDB: {e}")
            context = "Unable to retrieve context from the database."

        system_message = """You are a helpful course assistant. Use the provided context to answer questions about the course. 
        If the information is not in the context, say you don't have that information. Keep your answers concise and relevant."""
        
        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": f"Context: {context}\n\nQuestion: {prompt}"}
        ]

        response = st.session_state.client.chat.completions.create(
            model=model_to_use,
            messages=messages
        )

        reply_content = response.choices[0].message.content

        st.session_state.messages.append({"role": "assistant", "content": reply_content})
        with st.chat_message("assistant"):
            st.markdown(reply_content)

        update_conversation_buffer(512)

if __name__ == "__main__":
    lab5()