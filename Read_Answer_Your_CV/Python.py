import os
from dotenv import load_dotenv
from pypdf import PdfReader
from openai import OpenAI

# =========================
# Configuration
# =========================

PDF_PATH = "Data Entry.pdf"
MODEL = "poolside/laguna-m.1:free"
BASE_URL = "https://openrouter.ai/api/v1"

# =========================
# Load Environment Variables
# =========================

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")

if not API_KEY:
    raise ValueError(
        "OPENROUTER_API_KEY was not found.\n"
        "Please add it to your .env file."
    )

# =========================
# Create OpenAI Client
# =========================

client = OpenAI(
    api_key=API_KEY,
    base_url=BASE_URL,
)

# =========================
# Read PDF
# =========================

def extract_pdf_text(pdf_path: str) -> str:
    """Extract all text from a PDF file."""

    reader = PdfReader(pdf_path)
    text = ""

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"

    return text


cv_text = extract_pdf_text(PDF_PATH)

# =========================
# System Prompt
# =========================

system_prompt = f"""
You are my professional AI career assistant.

Your job is to answer questions ONLY using the information
contained in my CV.

Rules:
- Answer only career-related questions.
- Never invent information.
- If the answer is not found in the CV, say:
  "I couldn't find that information in your CV."
- Keep your answers clear and professional.

Here is my CV:

{cv_text}
"""

# =========================
# Chat Loop
# =========================

print("=" * 50)
print("CV Assistant is Ready!")
print("Type 'exit' to quit.")
print("=" * 50)

while True:

    user_prompt = input("\nAsk a question: ").strip()

    if user_prompt.lower() == "exit":
        print("Goodbye!")
        break

    try:

        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": user_prompt,
                },
            ],
        )

        reply = response.choices[0].message.content

        print("\nAssistant:")
        print(reply)

    except Exception as e:
        print(f"\nAn error occurred:\n{e}")