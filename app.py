import streamlit as st
from streamlit_utils import *
from langchain_utils import *
from langchain_google_genai import GoogleGenerativeAI
from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI


llm_models = {
     
    
        "gemini": GoogleGenerativeAI(model="gemini-2.0-flash-exp", google_api_key=st.secrets["GOOGLE_API_KEY"]),
        "claude": ChatAnthropic(model="claude-3-5-sonnet-20241022", anthropic_api_key=st.secrets["ANTHROPIC_API_KEY"]),
        "deepseek": ChatOpenAI(model="deepseek-reasoner", api_key=st.secrets["DEEPSEEK_API_KEY"], base_url="https://api.deepseek.com/v1"),
        "openai": ChatOpenAI(model="gpt-4o", api_key=st.secrets["OPENAI_API_KEY"])

}



def websitegpt_app():

    initialize_app()

    initialize_session_variables()
    
    display_previous_messages()

    if not st.session_state["html"]["generated"]:
        user_input = st.chat_input(max_chars=500, placeholder="Describe your website")

    else:
        user_input = st.chat_input(max_chars=500)


    if user_input:   

        st.chat_message("user",avatar="👤").write(user_input)
        st.session_state.messages.append({"role": "user", "content": user_input}) 
        st.session_state.display_messages.append({"role": "user", "content": user_input})

        if not st.session_state["html"]["generated"]:
            print(st.session_state.messages)

            with st.spinner('thinking...'):
                    
                    design_prompt = create_design_prompt()
                    code_prompt = create_code_prompt()
                    
                    # Create chains
                    design_chain = create_design_chain(llm_models["claude"], design_prompt)
                    code_chain = create_code_chain(llm_models["openai"], code_prompt)
                    full_chain = create_full_chain(design_chain, code_chain)
                    result = full_chain.invoke(user_input)
    
                    # Process and push
                    html_content = extract_html(result)
                    github_push(st.secrets["GITHUB_KEY"], html_content)

                    st.session_state["html"]["generated"] = html_content
                    time.sleep(40)
                    st.session_state.display_messages.append(
                    {"role": "assistant", "content": "Your website is ready! Check it out [here](https://mprajay999.github.io/). Let me know if you need any changes or ask me to deploy it"}
                )
                    #st.session_state["html"]["generated"] = html_content

                    #st.session_state.messages.append({"role": "assistant", "content": assistant_response})



        st.rerun()
        
websitegpt_app()