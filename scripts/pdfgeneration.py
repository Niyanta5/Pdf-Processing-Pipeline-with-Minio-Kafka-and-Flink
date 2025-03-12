import random
import os
import time
from datetime import datetime
from weasyprint import HTML
from dotenv import load_dotenv
from transformers import pipeline
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load the environment variables from the .env file (if needed for other purposes)
load_dotenv()

# Initialize the Hugging Face text generation pipeline
generator = pipeline("text-generation", model="distilgpt2")

# Function to generate the story
def generate_story(prompt):
    """
    Generates a story based on a given prompt using a local Hugging Face model.
    """
    try:
        # Generate text with the local model
        response = generator(prompt, max_length=150, num_return_sequences=1, temperature=0.7)
        return response[0]["generated_text"].strip()
    except Exception as e:
        print(f"Error generating story: {e}")
        return None

# Function to convert the story into a PDF
def generate_pdf(story, filename):
    """
    Converts a story into a PDF and saves it.
    """
    try:
        html_content = f"<html><body><h1>Generated Story</h1><p>{story}</p></body></html>"
        HTML(string=html_content).write_pdf(filename)
    except Exception as e:
        print(f"Error generating PDF: {e}")
        return False
    return True

# Function to generate a random prompt
def generate_random_prompt():
    characters = [
        "A lonely knight",
        "A brave pirate",
        "An astronaut",
        "A wizard",
        "A time traveler"
    ]
    actions = [
        "wanders through a dense forest",
        "embarks on a quest for treasure",
        "discovers a new planet",
        "casts a powerful spell",
        "travels to a mysterious time"
    ]
    settings = [
        "in a faraway land",
        "on an uncharted island",
        "in a galaxy far, far away",
        "in a magical kingdom",
        "in a post-apocalyptic world"
    ]
    
    character = random.choice(characters)
    action = random.choice(actions)
    setting = random.choice(settings)
    
    return f"{character} {action} {setting}."

# Function to generate a unique filename
def generate_unique_filename():
    """
    Generates a unique filename using timestamp and random characters.
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    random_chars = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=5))
    return f"story_{timestamp}_{random_chars}.pdf"

if __name__ == "__main__":
    # Generate a random prompt
    prompt = generate_random_prompt()
    print(f"Generated prompt: {prompt}")
    
    # Generate the story based on the random prompt
    story = generate_story(prompt)
    
    if story:
        # Generate a unique PDF filename
        unique_filename = generate_unique_filename()
        pdf_filename = f"/app/data/{unique_filename}"
        
        # Generate the PDF with the story
        if generate_pdf(story, pdf_filename):
            print(f"Random story PDF '{pdf_filename}' generated successfully!")
        else:
            print("Failed to generate PDF file.")
    else:
        print("Failed to generate the story.")