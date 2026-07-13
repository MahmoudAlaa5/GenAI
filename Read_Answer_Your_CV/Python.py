import os
from dotenv import load_dotenv
from pypdf import PdfReader
from openai import OpenAI
import gradio as gr

# Load environment variables
load_dotenv(override=True)
client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
)

# Extract text from the PDF
reader = PdfReader("Data Entry.pdf")
text = ""
for page in reader.pages:
    text += page.extract_text() + "\n"

# Function to handle the chat logic
def get_career_advice(message, history):
    # 1. Start with the system prompt
    messages = [{"role": "system", "content": f"you are my assistant. you are responsible for replying to questions about my career. you have my cv text here:\n{text}"}]
    
    # 2. Append the history (which is already in the correct format)
    messages.extend(history)
    
    # 3. Append the new user message
    messages.append({"role": "user", "content": message})
    
    # 4. Call the API
    response = client.chat.completions.create(
        model="poolside/laguna-m.1:free",
        messages=messages
    )
    
    return response.choices[0].message.content

# Launch with type="messages"
demo = gr.ChatInterface(fn=get_career_advice)


if __name__ == "__main__":
    demo.launch(share=True)
