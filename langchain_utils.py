from langchain.chains import SimpleSequentialChain, LLMChain
from langchain.prompts import PromptTemplate
import re
from streamlit_utils import *


# def create_design_prompt():
#     return PromptTemplate(
#         input_variables=["user_input"],
#         template=
#                 """
#                     you are a part of ragnova team, your role is to give detailed instructions to the web developer to create a static website for a users business needs. 
#                     give detailed instructions to the web developer to create a simple minimalistic aesthetic professional looking website for {user_input}, 
#                     the developer can use external frameworks for style; 
#                     the background should contain a nice aesthetic image; 
#                     dont give code snipets, only the plan for web developer; the user doesnt not give any input; dont keep any download links

#                 """
      
#     )

def create_design_prompt():
    return PromptTemplate(
        input_variables=["user_input"],
        template=
                """
                    you are a part of ragnova team, your role is to give detailed instructions to the web developer to create a  website for a users business needs. 
                    give detailed instructions to the web developer to create a simple minimalistic aesthetic professional looking website for {user_input}, 
                    the background should contain a nice aesthetic image; dont talk about tech stack
                    dont give code snipets or tech requirements; only the plan for web developer; 
                    the user doesnt not give any input; dont keep any download links;
                    the website should contain many sections in a single page layout;

                """
      
    )


def create_code_prompt():
    return PromptTemplate(
        input_variables=["design_instructions"],
        template="""
                    you are an elite web developer with years of experience;
                    This is the file structure of my vite+tailwind setup 
                    index.html
                    package.json
                    postcss.config.js
                    tailwind.config.js
                    src/
                      App.jsx
                      index.css
                      main.jsx
                      ;

                    all code is in app.jsx;

                    this is the requirement given by web desginer {design_instructions};
                    make changes only in the app.jsx file, i wont change any other file.
                    use high quality images from the web;  use framer motions
                    avoid using a logo, instead use the name of the business;
                    the webpage should contain multiple sections and look like its a large website; 
                    the website should be animated and functional; 
                    make sure all content is populated with information and website should look completed;
                    dont use complex dependencies, make sure the app will deploy in limited environment
                    include import react statement;
                    give full code as it will the final code for deployment;
                    make sure all links work and functional;

                """
                # +
                      
                # var
    )

# def create_code_prompt():
#     return PromptTemplate(
#         input_variables=["design_instructions"],
#         template="""
#                     you are an elite web developer with years of experience, 
#                     this is the requirement given by web desginer {design_instructions} , 
#                     keep html css js in one file , 
#                     the website should be deployment ready, 
#                     use high quality images from the web, 
#                     make sure all content is populated with information and website should look completed
#                     give full code as it will the final code for deployment, 
#                     keep the webpage as single page- 
#                 """
#                 # +
                      
#                 # var
#     )

def create_design_chain(llm, prompt):
    return LLMChain(
        llm=llm,
        prompt=prompt,
        output_key="design_instructions"
    )

def create_code_chain(llm, prompt):
    return LLMChain(
        llm=llm,
        prompt=prompt,
        output_key="final_code"
    )

def create_full_chain(design_chain, code_chain):
    return SimpleSequentialChain(
        chains=[design_chain, code_chain],
        verbose=True
    )

def extract_html(result):
    return re.findall(r"```jsx(.*?)```", result.get('output'), re.DOTALL)[0]
