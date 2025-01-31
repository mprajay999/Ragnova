from langchain.chains import SimpleSequentialChain, LLMChain
from langchain.prompts import PromptTemplate
import re
from streamlit_utils import *

def create_design_prompt():
    """Create prompt template for design instructions"""
    return PromptTemplate(
        input_variables=["user_input"],
        template="""Create detailed web design instructions for: {user_input}
        Include these elements:
        1. Color scheme
        2. Layout structure
        3. Key sections/components
        4. Responsive design requirements
        5. Special features
        
        Make instructions clear and specific for a developer to implement."""
    )

def create_code_prompt():
    """Create prompt template for code generation"""
    return PromptTemplate(
        input_variables=["design_instructions"],
        template="""Convert these design instructions into complete HTML/CSS code:
        {design_instructions}
        
        Requirements:
        - Include HTML, CSS, JS in one file
        - Include Images from the web
        - Use modern semantic HTML5
        - Include responsive CSS with Flexbox/Grid
        - Add comments for key sections
        - Ensure mobile-first approach
        - Include sample placeholder content
        - Output full code only, dont output snippets"""
    )

def create_design_chain(llm, prompt):
    """Create LLMChain for design generation"""
    return LLMChain(
        llm=llm,
        prompt=prompt,
        output_key="design_instructions"
    )

def create_code_chain(llm, prompt):
    """Create LLMChain for code generation"""
    return LLMChain(
        llm=llm,
        prompt=prompt,
        output_key="final_code"
    )

def create_full_chain(design_chain, code_chain):
    """Create sequential processing chain"""
    return SimpleSequentialChain(
        chains=[design_chain, code_chain],
        verbose=True
    )

def extract_html(result):
    """Extract HTML content from result"""
    return re.findall(r"```html(.*?)```", result.get('output'), re.DOTALL)[0]
