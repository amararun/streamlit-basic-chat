import os
from openai import OpenAI
import openai
import streamlit as st
import pandas as pd
import time

# Create a sidebar for API key configuration and additional features
st.sidebar.header("Configuration")
api_key = st.sidebar.text_input("Enter your OpenAI API key", type="password")
if api_key:
    # openai.api_key = api_key
    os.environ["OPENAI_API_KEY"] = api_key


def main():

    if 'client' not in st.session_state:
        # Initialize the client
        st.session_state.client = openai.OpenAI()

    # Assign existign Assistant ID
    if 'assistant_id' not in st.session_state:
      st.session_state.assistant_id= 'asst_9oIYXXLAnCrlVeekXEcajRwo'

    # Create thread, input box and user message
    st.session_state.thread = st.session_state.client.beta.threads.create()

    user_query = st.text_input("Enter your query:", "Tell me about streamlit")

    if st.button('Submit'):
        # Step 3: Add a Message to a Thread
        message = st.session_state.client.beta.threads.messages.create(
            thread_id=st.session_state.thread.id,
            role="user",
            content=user_query
        )

    # Step 4: Run the Assistant
    run = st.session_state.client.beta.threads.runs.create(
    thread_id=st.session_state.thread.id,
    assistant_id=st.session_state.assistant_id,
    instructions="Please address the user as Amar"
)


    while True:
            # Wait for 5 seconds
            time.sleep(10)

            # Retrieve the run status
            run_status = st.session_state.client.beta.threads.runs.retrieve(
                thread_id=st.session_state.thread.id,
                run_id=run.id
            )

            # If run is completed, get messages
            if run_status.status == 'completed':
                messages = st.session_state.client.beta.threads.messages.list(
                    thread_id=st.session_state.thread.id
                )

                # Loop through messages and print content based on role
                for msg in messages.data:
                    role = msg.role
                    content = msg.content[0].text.value
                    st.write(f"{role.capitalize()}: {content}")
                break
            else:
                st.write("Waiting for the Assistant to process...")
                time.sleep(10)

if __name__ == "__main__":
    main()
