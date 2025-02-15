import requests
from bs4 import BeautifulSoup
import re
import streamlit as st
from openai import OpenAI

html ='''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Raaga Indian Grand - Authentic Indian Cuisine</title>
    <style>
        /* Reset and Base Styles */
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Arial', sans-serif;
        }

        /* Color Variables */
        :root {
            --primary-color: #C43E00;
            --secondary-color: #FFD700;
            --text-color: #333;
            --light-bg: #FFF5EB;
        }

        /* Header Styles */
        header {
            background-color: white;
            padding: 1rem;
            position: fixed;
            width: 100%;
            top: 0;
            z-index: 1000;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }

        .nav-container {
            display: flex;
            justify-content: space-between;
            align-items: center;
            max-width: 1200px;
            margin: 0 auto;
        }

        .logo {
            font-size: 1.5rem;
            color: var(--primary-color);
            font-weight: bold;
        }

        .nav-menu {
            display: flex;
            gap: 2rem;
        }

        .nav-menu a {
            text-decoration: none;
            color: var(--text-color);
            transition: color 0.3s;
        }

        .nav-menu a:hover {
            color: var(--primary-color);
        }

        /* Hero Section */
        .hero {
            height: 100vh;
            background-color: var(--light-bg);
            display: flex;
            align-items: center;
            justify-content: center;
            text-align: center;
            padding-top: 80px;
        }

        .hero-content h1 {
            font-size: 3rem;
            color: var(--primary-color);
            margin-bottom: 1rem;
        }

        .cta-button {
            background-color: var(--primary-color);
            color: white;
            padding: 1rem 2rem;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            transition: background-color 0.3s;
        }

        .cta-button:hover {
            background-color: #A33300;
        }

        /* Sections Common Styles */
        section {
            padding: 4rem 2rem;
            max-width: 1200px;
            margin: 0 auto;
        }

        .section-title {
            text-align: center;
            margin-bottom: 2rem;
            color: var(--primary-color);
        }

        /* Menu Section */
        .menu-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 2rem;
        }

        .menu-item {
            text-align: center;
            padding: 1rem;
            border-radius: 10px;
            background-color: white;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }

        /* Testimonials Section */
        .testimonials {
            background-color: var(--light-bg);
        }

        /* Contact Section */
        .contact-form {
            max-width: 600px;
            margin: 0 auto;
        }

        .form-group {
            margin-bottom: 1rem;
        }

        input, textarea {
            width: 100%;
            padding: 0.5rem;
            margin-top: 0.5rem;
            border: 1px solid #ddd;
            border-radius: 5px;
        }

        /* Footer */
        footer {
            background-color: var(--text-color);
            color: white;
            padding: 2rem;
            text-align: center;
        }

        /* Responsive Design */
        @media (max-width: 768px) {
            .nav-menu {
                display: none;
            }

            .hero-content h1 {
                font-size: 2rem;
            }
        }
    </style>
</head>
<body>
    <!-- Header -->
    <header>
        <nav class="nav-container">
            <div class="logo">Raaga Indian Grand</div>
            <div class="nav-menu">
                <a href="#home">Home</a>
                <a href="#menu">Menu</a>
                <a href="#about">About</a>
                <a href="#contact">Contact</a>
            </div>
        </nav>
    </header>

    <!-- Hero Section -->
    <section class="hero" id="home">
        <div class="hero-content">
            <h1>Experience Authentic Indian Cuisine</h1>
            <p>Discover the rich flavors and traditional recipes of India</p>
            <button class="cta-button">Book a Table</button>
        </div>
    </section>

    <!-- Menu Section -->
    <section id="menu">
        <h2 class="section-title">Our Special Menu</h2>
        <div class="menu-grid">
            <div class="menu-item">
                <img src="butter-chicken.jpg" alt="Creamy butter chicken in a rich tomato sauce garnished with cream and coriander" style="width: 100%; height: 200px; object-fit: cover;">
                <h3>Butter Chicken</h3>
                <p>₹450</p>
            </div>
            <!-- Add more menu items similarly -->
        </div>
    </section>

    <!-- About Section -->
    <section id="about">
        <h2 class="section-title">About Us</h2>
        <p>Raaga Indian Grand brings you authentic Indian cuisine with a modern twist...</p>
    </section>

    <!-- Contact Section -->
    <section id="contact">
        <h2 class="section-title">Contact Us</h2>
        <form class="contact-form">
            <div class="form-group">
                <label for="name">Name:</label>
                <input type="text" id="name" required>
            </div>
            <div class="form-group">
                <label for="email">Email:</label>
                <input type="email" id="email" required>
            </div>
            <div class="form-group">
                <label for="message">Message:</label>
                <textarea id="message" rows="5" required></textarea>
            </div>
            <button type="submit" class="cta-button">Send Message</button>
        </form>
    </section>

    <!-- Footer -->
    <footer>
        <p>&copy; 2024 Raaga Indian Grand. All rights reserved.</p>
    </footer>

    <script>
        // Smooth scrolling for navigation links
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                document.querySelector(this.getAttribute('href')).scrollIntoView({
                    behavior: 'smooth'
                });
            });
        });

        // Form submission handling
        document.querySelector('.contact-form').addEventListener('submit', function(e) {
            e.preventDefault();
            alert('Thank you for your message! We will get back to you soon.');
            this.reset();
        });

        // Scroll-based animation for sections
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.style.opacity = 1;
                    entry.target.style.transform = 'translateY(0)';
                }
            });
        });

        document.querySelectorAll('section').forEach((section) => {
            section.style.opacity = 0;
            section.style.transform = 'translateY(20px)';
            section.style.transition = 'all 0.5s ease-out';
            observer.observe(section);
        });
    </script>
</body>
</html>
'''

def fetch_unsplash_image(query, unsplash_api_key):
    """Fetch the most appropriate Unsplash image based on a search query."""
    url = f"https://api.unsplash.com/search/photos?query={query}&client_id={unsplash_api_key}&per_page=5"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if data["total"] > 0:
            return data["results"][0]["urls"]["regular"]  # First result (most relevant)
        else:
            print(f"No images found for '{query}'")
            return None
    except Exception as e:
        print(f"Error fetching image for '{query}': {e}")
        return None
    
def fetch_dalle_image(query, openai_api_key):
    """Generate an image using DALL·E based on a text prompt."""
    client = OpenAI(api_key=openai_api_key)
    try:
        response = client.images.generate(
        model="dall-e-3",
        prompt=query,
        size="1792x1024",
        quality="hd",
        n=1,
    )
        return response.data[0].url
    except Exception as e:
        print(f"Error generating DALL·E image for '{query}': {e}")
        return None
    

def replace_images(html_content, unsplash_api_key,openai_api_key):
    """
    Replaces all <img> src attributes in the given HTML using Unsplash API, based on the alt text.

    Parameters:
    - html_content (str): The HTML content as a string.
    - unsplash_api_key (str): Your Unsplash API Access Key.

    Returns:
    - str: Updated HTML with replaced image URLs.
    """

    # Parse the HTML content
    soup = BeautifulSoup(html_content, "html.parser")

    # Find and replace all image sources
    for img in soup.find_all("img"):
        alt_text = img.get("alt")  # Get alt text for Unsplash search
        if alt_text:
            new_image_url = fetch_dalle_image(alt_text,openai_api_key)
            if new_image_url:
                img["src"] = new_image_url  # Update image src

    # Replace background images in <div> style attributes
    for div in soup.find_all("div", style=True):
        style = div["style"]
        match = re.search(r'url\([\'"]?(.*?)[\'"]?\)', style)  # Extract URL
        if match:
            alt_text = div.get("aria-label")  # Use aria-label for search
            if alt_text:
                new_image_url = fetch_dalle_image(alt_text, openai_api_key)
                if new_image_url:
                    div["style"] = re.sub(r'url\([\'"]?(.*?)[\'"]?\)', f'url({new_image_url})', style)

        # Replace URLs inside <style> blocks
    for style_tag in soup.find_all("style"):
        css = style_tag.string
        if css:
            urls = re.findall(r'url\([\'"]?(.*?)[\'"]?\)', css)  # Find all background images
            for url in urls:
                query = url.split("/")[-1].split(".")[0].replace("-", " ")  # Extract keyword from filename
                new_image_url = fetch_dalle_image(query, openai_api_key)
                if new_image_url:
                    css = css.replace(url, new_image_url)
            style_tag.string.replace_with(css)

    
    return str(soup)  # Return modified HTML as a string


#print(replace_images(html,st.secrets["UNSPLASH_API_KEY"]))