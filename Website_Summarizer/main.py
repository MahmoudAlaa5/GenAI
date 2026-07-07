import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from openai import OpenAI

# ==========================
# Load Environment Variables
# ==========================

load_dotenv()

API_KEY = os.getenv("OPENROUTER_APIKEY")

if not API_KEY:
    raise ValueError("OPENROUTER_APIKEY was not found in the .env file.")

MODEL = "nvidia/nemotron-3-super-120b-a12b:free"
BASE_URL = "https://openrouter.ai/api/v1"

# ==========================
# Get URL
# ==========================

user_url = input("Enter the Page URL: ").strip()

# ==========================
# Validate URL
# ==========================

def validate_url(url):
    if not url.startswith(("http://", "https://")):
        print("Invalid URL.")
        return False
    return True

if not validate_url(user_url):
    exit()

# ==========================
# Download Website
# ==========================

try:
    response = requests.get(user_url, timeout=10)
except requests.exceptions.RequestException as e:
    print(f"Error downloading website:\n{e}")
    exit()

# ==========================
# Check Status Code
# ==========================

if response.status_code != 200:
    print(f"Couldn't access the website. Status Code: {response.status_code}")
    exit()

# ==========================
# Parse HTML
# ==========================

html = response.text
soup = BeautifulSoup(html, "lxml")

# ==========================
# Remove Unwanted Elements
# ==========================

for tag in soup(["script", "style", "nav", "footer", "header"]):
    tag.decompose()

# ==========================
# Extract & Clean Text
# ==========================

text = soup.get_text(separator=" ")
text = " ".join(text.split())

# ==========================
# System Prompt
# ==========================

system_prompt = f"""
You are an expert summarizer.

Summarize the following webpage in a clear and concise way.

Webpage Content:

{text}
"""

# ==========================
# Create Client
# ==========================

client = OpenAI(
    api_key=API_KEY,
    base_url=BASE_URL,
)

# ==========================
# Generate Summary
# ==========================

try:
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            }
        ],
    )

    summary = response.choices[0].message.content

    print("\nWebsite Summary\n")
    print(summary)

except Exception as e:
    print(f"OpenRouter Error:\n{e}")
