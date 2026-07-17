# 🤖 AI Multi-Agent Code Reviewer

An AI-powered **Multi-Agent Code Review System** built with **Python**, **OpenRouter**, **AsyncOpenAI**, and **Gradio**.

The application analyzes source code using multiple specialized AI agents working in parallel, then combines their findings into a single professional report before deciding whether the code is production-ready or should be optimized.

---

# ✨ Features

- 📂 Upload a source code file
- 📝 Paste source code directly
- 🤖 AI Router Agent
- ⚡ Parallel execution using AsyncIO
- 🧠 Multiple specialized AI agents
- 📊 Professional synthesized review report
- ✅ Automatic code evaluation
- 🔧 AI-powered code optimization (when needed)
- 🌐 Interactive Gradio interface

---

# 🏗️ Workflow

```
                 User Input
          (File or Source Code)
                     │
                     ▼
             Input Validation
                     │
                     ▼
              Code Extraction
                     │
                     ▼
               Router Agent
                     │
                     ▼
              Orchestrator
                     │
      ┌──────────────┼──────────────┐
      ▼              ▼              ▼
 Syntax        Style Reviewer    Bug Analyst
 Checker
      ▼              ▼              ▼
 Performance   Security Auditor  Code Refactor
 Optimizer
      └──────────────┼──────────────┘
                     ▼
              Synthesizer Agent
                     │
                     ▼
              Evaluator Agent
              ┌─────────────┐
              │             │
         Approved        Not Approved
              │             │
              ▼             ▼
      Return Report     Optimizer Agent
                            │
                            ▼
                 Return Improved Code
```

---

# 🧠 AI Agents

## Router Agent

Determines whether the user's request is:

- Greeting
- Code Review
- Unknown

---

## Syntax Checker

Checks for:

- Syntax errors
- Missing imports
- Invalid indentation
- Missing brackets
- Language-specific syntax issues

---

## Style Reviewer

Reviews code quality including:

- Naming
- Readability
- Formatting
- Maintainability
- Clean Code principles

---

## Bug Analyst

Finds:

- Logical bugs
- Runtime issues
- Infinite loops
- Edge cases
- Incorrect conditions

---

## Performance Optimizer

Analyzes:

- Time Complexity
- Space Complexity
- Duplicate work
- Expensive operations
- Algorithm efficiency

---

## Security Auditor

Detects vulnerabilities such as:

- SQL Injection
- Command Injection
- Hardcoded Secrets
- Path Traversal
- Authentication flaws
- Authorization issues

---

## Code Refactor

Suggests a cleaner implementation while preserving functionality.

---

## Synthesizer

Collects all agent reports and generates one structured technical report.

---

## Evaluator

Decides whether:

- The code is production-ready

or

- The code requires optimization.

---

## Optimizer

Improves the original source code according to the evaluator's feedback.

---

# ⚙️ Technologies

- Python
- AsyncIO
- OpenRouter API
- AsyncOpenAI
- Gradio
- dotenv

---

# 📦 Installation

Clone the repository

```bash
git clone https://github.com/yourusername/AI-Multi-Agent-Code-Reviewer.git
```

Install dependencies

```bash
pip install -r requirements.txt
```

Create a `.env` file

```env
OPENROUTER_API_KEY=your_api_key
```

Run the application

```bash
python main.py
```

---

# 📁 Supported Languages

- Python
- C
- C++
- Java
- JavaScript
- TypeScript
- C#
- Go
- Rust
- PHP
- Ruby
- Kotlin
- Swift
- Scala
- SQL
- HTML
- CSS

---

# 📈 Future Improvements

- Support entire projects instead of a single file
- Generate downloadable PDF reports
- GitHub repository integration
- Pull Request review
- CI/CD integration
- Severity scoring
- Token usage analytics
- Multiple AI model selection
- Conversation history
- Export improved code

---

# 📸 Demo

Add screenshots or a GIF demonstrating the application here.

---

# 👨‍💻 Author

**Mahmoud Alaa**

Computer Science & Artificial Intelligence Student

AI Automation Engineer | AI Agent Developer | Python Developer

---

# ⭐ If you found this project useful, don't forget to give it a star!
