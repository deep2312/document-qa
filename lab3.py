import streamlit as st
from openai import OpenAI
import numpy as np

def lab3():
    # Show title and description.
    st.title("📄 Deep's Simple Chatbot")

    # Sidebar: Add a menu for the type of summary
    st.sidebar.title("Summary Options")
    summary_type = st.sidebar.selectbox(
        "Choose the type of summary:",
        ["Summarize the content in 100 words",
            "Summarize the content in 2 connecting paragraphs",
            "Summarize the content in 5 bullet points"
            ]
    )

    OpenAI_model = st.sidebar.selectbox('Which Model?',
                                           ('mini', 'regular'))
    
    if OpenAI_model == 'mini':
        model_to_use = 'gpt-4o-mini'
    else:
        model_to_use = 'gpt-4o'

    if 'client' not in st.session_state:
        api_key = st.secrets["my_api_key"]
        st.session_state.client = OpenAI(api_key=api_key)
    
    if 'messages' not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]
    
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("What is up?"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})       
        
        with st.chat_message("user"):
            st.markdown(prompt)
        
        client = st.session_state.client
        stream = client.chat.completions.create(
            model = model_to_use,
            messages = st.session_state.messages,
            stream=True
        )

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            response = st.write_stream(stream)

        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})
