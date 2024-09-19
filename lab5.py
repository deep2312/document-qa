import streamlit as st
from openai import OpenAI
import tiktoken  # Token counting
import pdfplumber  # For reading PDFs

__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import chromadb
from chromadb.utils import embedding_functions

def lab5():
    # Show title and description.
    st.title("Lab 5")

    # Create an OpenAI client.
    if 'openai_client' not in st.session_state:
        api_key = st.secrets["OPENAI_API_KEY"]
        st.session_state.openai_client = OpenAI(api_key=api_key)

    def add_to_collection(collection, text, filename):
        # Create an embedding
        openai_client = st.session_state.openai_client
        response = openai_client.embeddings.create(
            input=text,
            model="text-embedding-3-small"
        )
        
        # Get the embedding
        embedding = response.data[0].embedding
        
        # Add embedding and document to ChromaDB
        collection.add(
            documents=[text],
            ids=[filename],
            embeddings=[embedding]
        )
    
    topic = st.sidebar.selectbox("Topic", 
    ("Text Mining", "GenAI"))

    openai_client = st.session_state.openai_client
    response = openai_client.embeddings.create(
        input=topic,
        model="text-embedding-3-small"
    )

    # Get the embedding
    query_embedding = response.data[0].embedding

    # Get the text relating to this question (this prompt)
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=3  # Number of closest documents to return
    )

    # Print the results with IDs using an index
    for i in range(len(results['documents'][0])):
        doc = results['documents'][0][i]
        doc_id = results['ids'][0][i]
        st.write(f"The following file/syllabus might be helpful: {doc_id}")

