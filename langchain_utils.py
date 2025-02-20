from langchain.chains import SimpleSequentialChain, LLMChain
from langchain.prompts import PromptTemplate
import re
from streamlit_utils import *

# Designer
def create_design_prompt():
    return PromptTemplate(
        input_variables=["user_input"],
        template="""
            You are part of the Ragnova team. Your role is to give detailed instructions to the web developer to create a website for a user's business needs.
            Provide comprehensive guidance to design a simple, minimalistic, and professional-looking website for {user_input}.
            - Do NOT discuss the tech stack.
            - Do NOT provide code snippets or technical requirements—only a plan for the web developer.
            - Do NOT include any download links.
            - The website should feature multiple sections in a single-page layout.
            - Focus more on the UI part of the website.
            - Keep output minimal so that the developer can easily follow it
        """
    )

def create_design_chain(llm, prompt):
    return LLMChain(
        llm=llm,
        prompt=prompt,
        output_key="design_instructions"
    )

# Coder
def create_code_prompt():
    return PromptTemplate(
        input_variables=["design_instructions"],
        template="""
            You are an elite web developer with years of experience. You design beautiful web pages.
            
            **Project Setup:**  
            - This is the file structure for the Vite + Tailwind setup:  
              index.html  
              package.json  
              postcss.config.js  
              tailwind.config.js  
              src/  
                └── App.jsx  
                └── index.css  
                └── main.jsx  

            All code modifications should be made only in `App.jsx`.

            **Design Brief:**  
            - This is the requirement from the web designer: {design_instructions}. Make sure you follow the instructions as it is

            **Development Instructions:**  
            - Use high-quality images from unsplash.  
            - Integrate animations using `framer-motion`.  
            - Populate the website with content—ensure it looks complete and professional.  
            - Include the `import React` statement at the top.  
            - Ensure all links are functional.  
            - Provide the **full, final code** for deployment. The user will not complete any remaininf sections, everything should be ready
        """
    )

def create_code_chain(llm, prompt):
    return LLMChain(
        llm=llm,
        prompt=prompt,
        output_key="code"
    )

# Tester
def create_test_prompt():
    return PromptTemplate(
        input_variables=["code"],
        template="""
            You are a senior web tester and developer at Ragnova. Your role is to review the code provided by the developer, fix issues, and output the corrected full code.
             
            Here is the code to review:
            {code}

            add a chatbot to the website without any external dependencies

            **Tasks:**  
            1. **Review the Code:**  
               - Check for syntax errors and correct them.  
               - Ensure `import React` is at the top.  
               - Verify proper component structure and closures.  

            2. **Fix Functional Issues:**  
               - Ensure all links work.  
               - Implement smooth scroll transitions for navbar items.  
               - Correct or enhance animations using `framer-motion`.  

            3. **Ensure Completeness:**  
               - Confirm all navbar sections are implemented.  
               - Populate sections like footer with placeholder or real content as needed.
               - The website should not look incomplete  

            **Output:**  
            - Provide the full, corrected code as the final output, ready for deployment.
        """
    )

def create_test_chain(llm, prompt):
    return LLMChain(
        llm=llm,
        prompt=prompt,
        output_key="final_code"
    )

# Full Chain
def create_full_chain(design_chain, code_chain, test_chain):
    return SimpleSequentialChain(
        chains=[design_chain, code_chain, test_chain],
        verbose=True
    )

# HTML Extractor
def extract_html(result):
    matches = re.findall(r"```jsx(.*?)```", result.get('output', ''), re.DOTALL)
    return matches[0] if matches else ""
