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
def get_career_advice(user_question):
    system_prompt = f"you are my assistant. you are responsible for replying to questions about my career. you have my cv text here:\n{text}"
    
    response = client.chat.completions.create(
        model="poolside/laguna-m.1:free",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_question}
        ]
    )
    return response.choices[0].message.content

# Gradio interface with English labels
demo = gr.Interface(
    fn=get_career_advice,
    inputs=gr.Textbox(label="Ask about your career", placeholder="What is my university?"),
    outputs=gr.Markdown(label="Assistant Response"),
    title="Career Assistant",
    description="Ask any question regarding your career based on your CV."
)

if __name__ == "__main__":
    demo.launch(share=True)
