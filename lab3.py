import streamlit as st
from openai import OpenAI
import tiktoken  # Token counting

def lab3():
    # Show title and description.
    st.title("🧠 Simple Chatbot for Kids")

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

    # Initialize the OpenAI client if it doesn't exist
    if 'client' not in st.session_state:
        api_key = st.secrets["my_api_key"]
        st.session_state.client = OpenAI(api_key=api_key)

    # Initialize chat history if it doesn't exist
    if 'messages' not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "content": "Hi! How can I help you today?"}]
        st.session_state["awaiting_info_reply"] = False  # Tracks whether bot is awaiting a yes/no reply

    # Define a function to calculate the token count using the tiktoken library
    def count_tokens(messages):
        encoding = tiktoken.encoding_for_model(model_to_use)  # Get encoding for the selected model
        tokens_per_message = sum([len(encoding.encode(message["content"])) for message in messages])
        return tokens_per_message

    # Function to update chat history to fit within max_tokens
    def update_conversation_buffer(max_tokens):
        # Start with the full message history
        full_history = st.session_state.messages
        current_tokens = count_tokens(full_history)

        # Trim the history until it fits within the token limit
        while current_tokens > max_tokens and len(full_history) > 1:
            # Remove the oldest message (pop the first element)
            full_history.pop(0)
            current_tokens = count_tokens(full_history)

        st.session_state.messages = full_history  # Update the messages with the trimmed version

    # Display all the messages in the chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Handle user input
    if prompt := st.chat_input("What would you like to ask?"):
        if st.session_state["awaiting_info_reply"]:
            # Handle the yes/no response for more info
            if prompt.lower() == 'yes':
                # Provide more information
                last_assistant_message = [msg["content"] for msg in st.session_state.messages if msg["role"] == "assistant"][-1]

                # Ask for more information from OpenAI API
                st.session_state.messages.append({"role": "user", "content": "Can you give me more details?"})
                
                client = st.session_state.client
                response = client.chat.completions.create(
                    model=model_to_use,
                    messages=[
                        {"role": "system", "content": "Expand on this in a way a 10-year-old would understand."},
                        {"role": "assistant", "content": last_assistant_message}
                    ]
                )

                # Extract and display the more detailed information
                detailed_reply = response.choices[0].message.content
                st.session_state.messages.append({"role": "assistant", "content": detailed_reply})

                with st.chat_message("assistant"):
                    st.markdown(detailed_reply)

                # Ask if they want more info again
                follow_up = "DO YOU WANT MORE INFO?"
                st.session_state.messages.append({"role": "assistant", "content": follow_up})
                st.session_state["awaiting_info_reply"] = True

                with st.chat_message("assistant"):
                    st.markdown(follow_up)

            elif prompt.lower() == 'no':
                # Reset and ask for a new question
                new_question_prompt = "What question can I help you with next?"
                st.session_state.messages.append({"role": "assistant", "content": new_question_prompt})
                st.session_state["awaiting_info_reply"] = False

                with st.chat_message("assistant"):
                    st.markdown(new_question_prompt)
            else:
                # If the response isn't clear, ask again
                clarification = "Please answer with 'yes' or 'no'. DO YOU WANT MORE INFO?"
                st.session_state.messages.append({"role": "assistant", "content": clarification})

                with st.chat_message("assistant"):
                    st.markdown(clarification)
        
        else:
            # Normal question flow
            st.session_state.messages.append({"role": "user", "content": prompt})

            with st.chat_message("user"):
                st.markdown(prompt)

            # Define your max tokens limit
            max_tokens = 1024  # For example, set it to 1024 tokens

            # Update conversation buffer to fit within max_tokens
            update_conversation_buffer(max_tokens)

            # Send to OpenAI API and get the response
            client = st.session_state.client
            response = client.chat.completions.create(
                model=model_to_use,
                messages=st.session_state.messages
            )

            # Extract the response content properly
            reply_content = response.choices[0].message.content

            # Display assistant response in chat message container
            st.session_state.messages.append({"role": "assistant", "content": reply_content})

            with st.chat_message("assistant"):
                st.markdown(reply_content)

            # Ask if they want more info
            follow_up = "DO YOU WANT MORE INFO?"
            st.session_state.messages.append({"role": "assistant", "content": follow_up})
            st.session_state["awaiting_info_reply"] = True

            with st.chat_message("assistant"):
                st.markdown(follow_up)
