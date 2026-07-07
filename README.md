# 🌐 AI Website Summarizer

An AI application that extracts the main content from any website and generates a concise summary using a Large Language Model via OpenRouter.

## 📌 Features

- Accepts any website URL.
- Downloads webpage content.
- Removes unnecessary HTML elements.
- Extracts and cleans webpage text.
- Generates an AI-powered summary.
- Secure API key management using `.env`.

## 🛠️ Tech Stack

- Python
- Requests
- BeautifulSoup
- lxml
- OpenRouter API
- OpenAI Python SDK
- python-dotenv

## 📂 Project Structure

```
Website_Summarizer/
│
├── main.py
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
Enter the website URL:
https://openai.com

Website Summary

OpenAI develops advanced AI models and products,
including ChatGPT and Codex...
```

## 🚀 Future Improvements

- Summarize multiple pages
- Export summaries to PDF
- Streamlit Web UI
- Support YouTube transcript summarization
- Multi-language summaries
