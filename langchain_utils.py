from langchain.chains import SimpleSequentialChain, LLMChain
from langchain.prompts import PromptTemplate
import re
from streamlit_utils import *


var = '''
        use this as a reference amd include the design content from here - 
                   ### Spice Route Columbus  

#### Tagline  
Authentic South Indian Flavors, American Comforts.  

#### Brand Identity  

**Colors:**  
- Primary: #a83249 (Based on Indian spices - chili pepper)  
- Secondary: #f2e8cf (Warm, creamy - representing coconut milk, a South Indian staple)  
- Accent: #457b9d (Cool, modern - appeals to American aesthetic)  
- Text Primary: #343a40 (Dark grey for readability)  
- Text Secondary: #6c757d (Lighter grey for supporting text)  

**Typography:**  
- Heading: Playfair Display, serif (Elegant, classic - adds a touch of formality)  
- Body: Open Sans, sans-serif (Clean, readable - good for body text)  

**Logo:**  
- A stylized image of a spice route caravan combined with a South Indian temple silhouette  
- Potentially includes the text "Spice Route Columbus"  
- Placement: Header, Footer, Favicon  

**Imagery Style:**  
- High-quality, authentic food photography  
- Lifestyle shots of diverse people enjoying the food in a warm and inviting atmosphere  

#### Storytelling  

**Overall Narrative:**  
Spice Route Columbus is a culinary bridge, connecting the vibrant flavors of South India with the familiar comforts of American cuisine. We offer a welcoming space for both communities to gather, celebrate, and enjoy delicious food made with fresh ingredients and heartfelt hospitality. We're not just a restaurant; we're a community gathering place.  

#### Content Structure  

##### Home  
- **Hero Section:**  
  - Headline: Experience the Spice Route  
  - Subheadline: Authentic South Indian Cuisine, American Favorites, and a Warm Welcome.  
  - Call to Action: View Our Menu  
  - Image: A stunning photo of a signature South Indian dish alongside a popular American appetizer  

- **About Us Snippet:**  
  - Headline: Our Story  
  - Content: Driven by a passion for sharing the rich culinary heritage of South India, our family opened Spice Route Columbus to bring authentic flavors and warm hospitality to the community. We carefully blend traditional recipes with modern twists, creating a unique dining experience that celebrates both cultures.  
  - Image: A family photo or a picture of the restaurant's founders in the kitchen  

- **Featured Dishes:**  
  - Headline: Taste the Difference  
  - Dishes:  
    - Masala Dosa - A crispy crepe made from fermented rice and lentil batter, filled with spiced potatoes and served with sambar and chutney  
    - Chicken Tikka Masala - Tender pieces of chicken marinated in yogurt and spices, cooked in a creamy tomato-based sauce  
    - Idli Sambar - Steamed rice cakes served with a lentil-based vegetable stew and coconut chutney  
  - Call to Action: See Full Menu  

- **Party Orders Section:**  
  - Headline: Celebrate with Spice Route  
  - Content: Planning a party or event? Let us cater with our delicious South Indian and American dishes. We offer customizable menus to suit your needs and budget. Contact us for a consultation.  
  - Image: Photo of a beautifully catered event with South Indian food  

- **Testimonials:**  
  - Headline: What Our Customers Say  
  - Reviews:  
    - John S.: "The best South Indian food in Columbus! The dosas are amazing and the service is always friendly."  
    - Priya K.: "A taste of home! The food is authentic and the atmosphere is so welcoming. Love bringing my family here."  

##### Menu  
- A comprehensive list of all dishes, categorized by type (appetizers, entrees, desserts, drinks)  
- Includes detailed descriptions and high-quality photos  
- Clear indication of vegetarian, vegan, and gluten-free options  
- Clean, easily navigable grid layout with filtering options for dietary restrictions  
- Color coding to differentiate between South Indian and American dishes  

##### Party Orders  
- Detailed information about catering services, including menu options, pricing, and contact information  
- Step-by-step guide to ordering catering  
- Gallery of catered events  
- Emphasis on customization and flexibility  

##### Contact  
- Restaurant address, phone number, email address, and operating hours  
- Interactive map integration  
- Easy-to-use contact form  

##### About Us  
- In-depth look at the restaurant's history, mission, and values  
- Profiles of the chefs and staff  
- Photos of the restaurant and team  
- Storytelling approach with a blend of text and visuals  
- Warm and inviting imagery that showcases the restaurant's personality  

#### UI/UX Elements  

**Navigation:**  
- Responsive navigation bar  
- Menu items: Home, Menu, Party Orders, About Us, Contact  
- Accessibility: ARIA attributes for screen readers, keyboard navigation support  

**Footer:**  
- Copyright © [Year] Spice Route Columbus. All Rights Reserved. | Privacy Policy | Terms of Service  
- Social Media Links: Facebook, Instagram  
- Restaurant address and phone number  

**Forms:**  
- **Contact Form:**  
  - Fields: Name, Email, Phone Number, Message  
  - Client-side and server-side validation to prevent errors  
  - Clear labels and instructions for each field  
- **Party Order Form:**  
  - Fields: Name, Email, Phone Number, Event Date, Number of Guests, Cuisine Preference (South Indian, American, Both), Budget, Additional Requirements  
  - Client-side and server-side validation  

**Animations:**  
- Subtle animations to enhance user experience without being distracting  
- Examples: Fade-in effects on page load, hover effects on menu items, smooth scrolling  

**Responsiveness:**  
- Website fully responsive and optimized for all devices (desktops, tablets, and smartphones)  
- Breakpoints: Small mobile, large mobile, tablet, desktop  

**Accessibility:**  
- Adherence to WCAG 2.1 Level AA guidelines  
- Features:  
  - Alternative text for images  
  - Keyboard navigation  
  - Sufficient color contrast  
  - Clear and concise content  
        '''


def create_design_prompt():
    return PromptTemplate(
        input_variables=["user_input"],
        template=
                """
                    you are a part of ragnova team, your role is to give detailed instructions to the web developer to create a static website for a users business needs. 
                    give detailed instructions to the web developer to create a simple minimalistic aesthetic professional looking website for {user_input}, 
                    the developer can use external frameworks for style; 
                    the background should contain a nice aesthetic image; 
                    dont give code snipets, only the plan for web developer; the user doesnt not give any input; dont keep any download links

                """
      
    )


def create_code_prompt():
    return PromptTemplate(
        input_variables=["design_instructions"],
        template="""
                    you are an elite web developer with years of experience, 
                    this is the requirement given by web desginer {design_instructions} , 
                    keep html css js in one file , 
                    the website should be deployment ready, 
                    use high quality images from the web, 
                    make sure all content is populated with information and website should look completed
                    give full code as it will the final code for deployment, 
                    keep the webpage as single page- 
                """
                +
                      
                var
    )

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
    return re.findall(r"```html(.*?)```", result.get('output'), re.DOTALL)[0]
