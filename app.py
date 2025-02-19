import streamlit as st
from streamlit_utils import *
from langchain_utils import *
from langchain_google_genai import GoogleGenerativeAI
from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI
import time
from images import *

llm_models = {
        "gemini": GoogleGenerativeAI(model="gemini-1.5-pro", google_api_key=st.secrets["GOOGLE_API_KEY"]),
        "claude": ChatAnthropic(model="claude-3-5-sonnet-20241022", anthropic_api_key=st.secrets["ANTHROPIC_API_KEY"],max_tokens=8192),
        "deepseek": ChatOpenAI(model="deepseek-reasoner", api_key=st.secrets["DEEPSEEK_API_KEY"], base_url="https://api.deepseek.com/v1"),
        "qwen": ChatOpenAI(model="qwen-max", api_key=st.secrets["QWEN_API_KEY"], base_url="https://dashscope-intl.aliyuncs.com/compatible-mode/v1"),
        "openai": ChatOpenAI(model="chatgpt-4o-latest", api_key=st.secrets["OPENAI_API_KEY"])
}


def websitegpt_app():

    initialize_app()

    initialize_session_variables()
    
    display_previous_messages()

    if not st.session_state["html"]:
        user_input = st.chat_input(max_chars=500, placeholder="Describe your website")

    else:
        user_input = st.chat_input(max_chars=500)


    if user_input:   

        st.chat_message("user",avatar="👤").write(user_input)
        st.session_state.messages.append({"role": "user", "content": user_input}) 

        if not st.session_state["html"]:
            print(st.session_state.messages)

            with st.spinner('thinking...'):
                    
                    design_prompt = create_design_prompt()
                    code_prompt = create_code_prompt()
                    
                    # Create chains
                    design_chain = create_design_chain(llm_models["openai"], design_prompt)
                    code_chain = create_code_chain(llm_models["claude"], code_prompt)
                    full_chain = create_full_chain(design_chain, code_chain)
                    result = full_chain.invoke(user_input)
    
                    # Process and push
                    html_content = extract_html(result)
                    #html_content = replace_images(html_content,st.secrets["UNSPLASH_API_KEY"],st.secrets["OPENAI_API_KEY"])
                    github_push(st.secrets["GITHUB_KEY"], html_content)

                    st.session_state["html"] = html_content
                    time.sleep(20)
                    st.session_state.messages.append(
                    {"role": "assistant", "content": "Your website is ready! Check it out [here](https://vitetailwind.vercel.app/). Let me know if you need any changes or ask me to deploy it"}
                )




        st.rerun()
        
websitegpt_app()