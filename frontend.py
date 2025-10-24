import streamlit as st
from app import app  
from langchain_core.messages import HumanMessage, AIMessage
import uuid

# *********************************** Utility Functions ******************************************
def generate_thread_id():
    return str(uuid.uuid4())

def reset_chat():
    thread_id = generate_thread_id()
    st.session_state['thread_id'] = thread_id
    add_thread(thread_id)
    st.session_state['message_history'] = []

def add_thread(thread_id):
    if thread_id not in st.session_state['chat_threads']:
        st.session_state['chat_threads'].append(thread_id)

def load_conversation(thread_id):
    return st.session_state.get('message_history_map', {}).get(thread_id, [])

# *********************************** Session Setup *********************************************
if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

if 'thread_id' not in st.session_state:
    st.session_state['thread_id'] = generate_thread_id()

if 'chat_threads' not in st.session_state:
    st.session_state['chat_threads'] = []

if 'message_history_map' not in st.session_state:
    st.session_state['message_history_map'] = {}

add_thread(st.session_state['thread_id'])

# **************************************** Sidebar UI *******************************************
st.sidebar.title("Property Chatbot")

if st.sidebar.button("New Chat"):
    reset_chat()

st.sidebar.header("My Conversations")
for thread_id in st.session_state['chat_threads'][::-1]:
    if st.sidebar.button(str(thread_id)):
        st.session_state['thread_id'] = thread_id
        st.session_state['message_history'] = load_conversation(thread_id)

# **************************************** Main Chat UI *****************************************
# Load conversation history
for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])

# User input
user_input = st.chat_input("Type here")

if user_input:
    # Add user message
    st.session_state['message_history'].append({'role':'user','content':user_input})
    with st.chat_message('user'):
        st.text(user_input)

    # Config for thread
    CONFIG = {
        'configurable': {'thread_id': st.session_state['thread_id']}
    }

    # Stream bot response
    with st.chat_message('assistant'):
        def ai_only_stream():
            
            result = app.invoke({"question": user_input}, CONFIG)
            answer = result.get("answer", "No answer returned")
            for char in answer:  
                yield char

        ai_message = st.write_stream(ai_only_stream())
        st.session_state['message_history'].append({'role':'assistant','content':ai_message})

    # Save the conversation per thread
    st.session_state['message_history_map'][st.session_state['thread_id']] = st.session_state['message_history']
