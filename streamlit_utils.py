import requests
import base64
import streamlit as st


def initialize_app():
    st.set_page_config(
        page_title='WebsiteGPT',
        page_icon='🤖',
        initial_sidebar_state='collapsed'
    )


    st.title("Let’s bring your business to life!")
    st.markdown("""
                WebsiteGPT is your AI-powered assistant to create and deploy stunning websites effortlessly. 🚀
                
                """)
    with st.sidebar:
        st.markdown('<center><h1>WebsiteGPT</h1></center>', unsafe_allow_html=True)
        st.info("""
                Welcome to WebsiteGPT! This tool helps you create a website by interacting with an AI assistant. 
                Simply type your ideas or requirements in the chat, and let the assistant generate the website for you.
                Ready to create your website? Let's get started! 
                """)

def initialize_session_variables():
    
    if "html" not in st.session_state:
        st.session_state["html"] = False

    if "messages" not in st.session_state:
        st.session_state["messages"] = [

            {"role": "assistant", "content": "Hello! let's create a website together, Can you please let me know more about your business or the type of website you want to create?"}
        ]




def display_previous_messages():
    for msg in st.session_state.messages: 
        if msg["role"] =='assistant':
            st.chat_message(msg["role"],avatar="🤖").write(msg["content"])
        else:
            st.chat_message(msg["role"],avatar="👤").write(msg["content"])



def github_push(GITHUB_KEY,html):
    repo_name = "vitetailwind"
    file_name = "src/App.jsx"
    commit_message = "Replaced index.html with new content"

    # Read the new file content and encode it to base64
    content = base64.b64encode(html.encode('utf-8')).decode('utf-8')

    # Correct URL format for the GitHub API
    url = f"https://api.github.com/repos/mprajay999/{repo_name}/contents/{file_name}"

    headers = {
        "Authorization": "Bearer "+ GITHUB_KEY
    }

    # Fetch the current file's details to get the sha for replacement
    response_get = requests.get(url, headers=headers)

    if response_get.status_code == 200:
        # File exists, get the sha value for replacement
        file_info = response_get.json()
        sha = file_info['sha']

        # Prepare the data for the file replacement
        data = {
            "message": commit_message,
            "content": content,
            "sha": sha  # Include the sha to replace the file
        }
    elif response_get.status_code == 404:
        # If file doesn't exist, create a new one without sha
        data = {
            "message": commit_message,
            "content": content
        }
    else:
        #print(f"Failed to fetch file details: {response_get.status_code}, {response_get.text}")
        exit()

    # Send the PUT request to replace the file
    response = requests.put(url, headers=headers, json=data)
