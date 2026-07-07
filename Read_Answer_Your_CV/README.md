# 🤖 AI CV Assistant

An AI-powered assistant that answers questions about my professional background by reading my CV (PDF) and using a Large Language Model through OpenRouter.

## 📌 Features

- Extracts text from a PDF resume.
- Uses an LLM to answer questions based only on the CV content.
- Interactive command-line interface.
- Secure API key management using `.env`.
- Built with the OpenAI SDK and OpenRouter.

## 🛠️ Tech Stack

- Python
- OpenRouter API
- OpenAI Python SDK
- PyPDF
- python-dotenv

## 📂 Project Structure

```
AI_CV_Assistant/
│
├── main.py
├── Data Entry.pdf
├── .env
├── pyproject.toml
├── uv.lock
└── README.md
```

## ⚙️ Installation

Clone the repository

```bash
git clone <repository-url>
```

Create a virtual environment

```bash
uv venv
```

Install dependencies

```bash
uv sync
```

## 🔑 Environment Variables

Create a `.env` file.

```env
OPENROUTER_API_KEY=your_api_key_here
```

## ▶️ Run

```bash
uv run main.py
```

## 💬 Example

```
Question:
What programming languages do you know?

Answer:
I have experience with Python, JavaScript...
```

## 🚀 Future Improvements

- Chat history
- Memory support
- RAG with Vector Database
- Streamlit Web UI
- Multi-document support
