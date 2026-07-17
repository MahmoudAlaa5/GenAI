# %%
import os
from dotenv import load_dotenv
import gradio as gr
import json
import asyncio
from openai import AsyncOpenAI
from pathlib import Path

# %%
load_dotenv(override=True)
client = AsyncOpenAI(
        api_key=os.getenv("OPENROUTER_API_KEY"),
        base_url="https://openrouter.ai/api/v1"
    )

model = "google/gemma-4-26b-a4b-it:free"

system_prompt = """
You are the Router Agent for a multi-agent Code Review System.

Your only responsibility is to classify the user's request.

You DO NOT review code.
You DO NOT explain anything.
You DO NOT answer programming questions.
You ONLY decide where the request should go.

=========================
Available Routes
=========================

1. greeting
Use this route if the user is:
- greeting
- thanking
- saying goodbye
- asking how you are
- casual conversation

Examples:
- Hi
- Hello
- Good morning
- Thanks
- Thank you
- Bye
- How are you?

Output:
{
  "route": "greeting"
}

-------------------------

2. code_review
Use this route if the user:

- provides source code
- uploads a source code file
- asks to review code
- asks to find bugs
- asks to improve code
- asks about performance
- asks about security
- asks for refactoring
- asks about best practices
- asks why code doesn't work
- asks for optimization
- asks to explain code

Examples:

Review this Python code.

Find bugs.

Optimize this function.

Explain this C++ code.

Here is my JavaScript project.

Check my SQL query.

Improve readability.

Output:

{
  "route": "code_review"
}


3. Unknown
Use this route if the user:
- ask about any thing except code and greeting
- ask about general information

Examples:
Do you know who is frank kolman?
what is the capital of Egypt?
who is messi?

Output:

{
  "route": "Unknown"
}

=========================
Important Rules
=========================

Return ONLY valid JSON.

Never wrap JSON inside markdown.

Never write explanations.

Never add extra fields.

Never answer the user's request.

Never generate code.

Never generate markdown.

Only return one of these two outputs.

Example 1

User:
Hello

Assistant:
{
  "route":"greeting"
}

Example 2

User:
Can you review this Python code?

Assistant:
{
  "route":"code_review"
}

Example 3

User:
def add(a,b):
    return a+b

Assistant:
{
  "route":"code_review"
}

Example 4
User:
Tell me about your self

Assistant:
{
  "route":"Unknown"
}

"""

# %%
# Read Code from user (file/text)

SUPPORTED_EXTENSIONS = {
    ".py",
    ".cpp",
    ".c",
    ".cc",
    ".h",
    ".hpp",
    ".java",
    ".js",
    ".ts",
    ".cs",
    ".go",
    ".rs",
    ".php",
    ".rb",
    ".swift",
    ".kt",
    ".scala",
    ".sql",
    ".html",
    ".css"
}

MAX_CODE_LENGTH = 30000

# %%
async def extract_code(file=None, text=None):
    """
    Extract code from either:
        1. Uploaded file (Gradio)
        2. File path (Terminal/Jupyter)
        3. Textbox

    Returns:
        code (str)
    """

    if file is not None:

        # If file is a string path
        if isinstance(file, str):
            path = file

        # If file comes from Gradio
        else:
            path = file.name

        with open(path, "r", encoding="utf-8") as f:
            return f.read()

    if text is not None:
        return text.strip()

    return None

# %%
async def validate_input(file=None, text=None):
    """
    Validate the user's input.
    """

    # -----------------------------
    # No Input
    # -----------------------------
    if file is None and (text is None or not text.strip()):
        return False, "❌ Please upload a code file or paste your code."

    # -----------------------------
    # File Validation
    # -----------------------------
    if file is not None:

        # Terminal / Jupyter
        if isinstance(file, str):
            extension = Path(file).suffix.lower()

        # Gradio
        else:
            extension = Path(file.name).suffix.lower()

        if extension not in SUPPORTED_EXTENSIONS:
            return (
                False,
                f"❌ Unsupported file type: {extension}"
            )

    # -----------------------------
    # Extract Code
    # -----------------------------
    code = await extract_code(file, text)

    # -----------------------------
    # Empty Code
    # -----------------------------
    if code is None or not code.strip():
        return False, "❌ The code is empty."

    # -----------------------------
    # Code Too Large
    # -----------------------------
    if len(code) > MAX_CODE_LENGTH:
        return (
            False,
            "❌ The code is too large."
        )

    # -----------------------------
    # Success
    # -----------------------------
    return True, code

# %%
async def router(user_message):

        response = await client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ],
            response_format={"type": "json_object"}
        )

        content = response.choices[0].message.content

        if content is None:
            return None

        result = json.loads(content)

        return result["route"]

# %%


# %%


# %%
# syntax checker
async def syntax_checker(user_code):
    system_prompt = """
    You are a Syntax Checker.

    Your job is ONLY to inspect the syntax of the code.

    Check for:
    - Syntax errors
    - Missing brackets
    - Missing imports
    - Invalid indentation
    - Wrong function definitions
    - Invalid variable declarations
    - Language-specific syntax issues

    Return a clear report.

    If no syntax problems exist, say:
    "No syntax errors found".
    """
    response = await client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            
            {
                "role": "user",
                "content": user_code
            }
        ],
        temperature=0

    )

    return response.choices[0].message.content

# %%
# style review
async def style_reviewer(user_code):
    system_prompt = """
    You are a Code Style Reviewer.

    Review the code according to clean code principles.

        Focus on:
        - Variable names
        - Function names
        - Readability
        - Comments
        - Formatting
        - Consistency
        - Maintainability

        Do NOT fix the code.
        Only explain what should be improved.
    """
    response = await client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_code
            }
        ],
        temperature=0.3
    )

    return response.choices[0].message.content

# %%
# Bug Analyst
async def bug_analyst(user_code):
    system_prompt = """
        You are a Bug Analyst.

    Analyze the code for logical bugs.

    Look for:
    - Wrong conditions
    - Infinite loops
    - Null errors
    - Incorrect calculations
    - Runtime exceptions
    - Edge cases
    - Logic mistakes

    Explain every bug and why it may happen.
    """
    response = await client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": system_prompt

            },
            {
                "role": "user",
                "content": user_code
            }
        ],
        temperature=0.2
    )

    return response.choices[0].message.content

# %%
# Performance Optimizer

async def performance_optimizer(user_code):
    system_prompt = """
        You are a Performance Optimization Expert.

    Analyze the efficiency of the code.

    Focus on:
    - Time Complexity
    - Space Complexity
    - Unnecessary loops
    - Duplicate work
    - Memory usage
    - Expensive operations
    - Better algorithms

    Suggest improvements without changing functionality.
    """

    response = await client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_code
            }
        ],
        temperature=0.2
    )

    return response.choices[0].message.content

# %%
# security auditor
async def security_auditor(user_code):
    system_prompt = """
        You are a Security Auditor.

    Inspect the code for security vulnerabilities.

    Look for:
    - SQL Injection
    - Command Injection
    - Path Traversal
    - Hardcoded secrets
    - API Keys
    - Authentication flaws
    - Authorization issues
    - Unsafe file operations
    - Insecure deserialization

    Explain every vulnerability and its severity.
        """
    response = await client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_code
            }
        ],
        temperature=0
    )

    return response.choices[0].message.content

# %%
# code refactor
async def code_refactor(code):
    system_prompt = """
        You are a Senior Software Engineer.

    Refactor the code while preserving its functionality.

    Goals:
    - Cleaner architecture
    - Better readability
    - Better maintainability
    - Remove duplication
    - Better function decomposition
    - Better naming
    - Follow best practices

    Return the improved code followed by a short explanation.
    """
    response = await client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": code
            }
        ],
        temperature=0.4
    )

    return response.choices[0].message.content

# %%
# Orchestrator


async def orchestrator(code):
    """
    Run all review agents in parallel and collect their outputs.
    """

    tasks = {
        "syntax_checker": syntax_checker(code),
        "style_reviewer": style_reviewer(code),
        "bug_analyst": bug_analyst(code),
        "performance_optimizer": performance_optimizer(code),
        "security_auditor": security_auditor(code),
        "code_refactor": code_refactor(code),
    }

    results = await asyncio.gather(*tasks.values())

    return {
        name: result
        for name, result in zip(tasks.keys(), results)
    }

# %%
# Collect Reports
SYSTEM_PROMPT_SYNTHESIZER = """
You are the Synthesizer Agent in a Multi-Agent Code Review System.

Your responsibility is to combine the outputs produced by multiple expert agents into ONE clear, professional report.

The experts are:

- Syntax Checker
- Style Reviewer
- Bug Analyst
- Performance Optimizer
- Security Auditor
- Code Refactor

Your job is NOT to perform another code review.

Instead:

1. Merge duplicate observations.
2. Remove repeated information.
3. Organize the report professionally.
4. Keep every important finding.
5. Prioritize critical issues first.
6. Keep the report concise but complete.

Return the report using exactly this structure.

# Code Review Report

## Executive Summary

Provide a short overview of the code quality.

---

## Syntax Issues

List syntax problems.

If none exist write:

No syntax issues found.

---

## Bugs

List logical or runtime bugs.

---

## Performance

List performance improvements.

---

## Security

List security vulnerabilities ordered by severity.

---

## Code Style

List readability and maintainability suggestions.

---

## Refactoring Suggestions

Summarize the proposed refactoring.

---

## Overall Assessment

Give an overall evaluation of the code.

Use one of:

Excellent

Good

Needs Improvement

Poor

Do not invent issues.

Do not remove important findings.

Write in professional technical English.
"""

async def synthesizer(results):

    report = f"""
Syntax Checker:
{results["syntax_checker"]}

Style Reviewer:
{results["style_reviewer"]}

Bug Analyst:
{results["bug_analyst"]}

Performance Optimizer:
{results["performance_optimizer"]}

Security Auditor:
{results["security_auditor"]}

Code Refactor:
{results["code_refactor"]}
"""

    response = await client.chat.completions.create(
        model=model,
        messages=[
            {
                "role":"system",
                "content":SYSTEM_PROMPT_SYNTHESIZER
            },
            {
                "role":"user",
                "content":report
            }
        ],
        temperature=0.2
    )

    return response.choices[0].message.content

# %%


async def evaluator(code, report):

    system_prompt = """
You are the Final Evaluation Agent in a Multi-Agent Code Review System.

You receive:

1. The original source code.
2. The final synthesized review report.

Your job is NOT to rewrite the code.

Your job is ONLY to decide whether the code is good enough or still requires improvements.

Evaluation Criteria:

- No critical syntax errors.
- No critical logical bugs.
- No high-risk security vulnerabilities.
- Acceptable performance.
- Acceptable code style.
- Maintainable structure.
- The synthesized report correctly summarizes the findings.

Return ONLY valid JSON.

Example:

{
    "approved": true,
    "feedback": "The code is production-ready."
}

or

{
    "approved": false,
    "feedback": "Remove duplicated code and fix the SQL Injection vulnerability."
}
"""

    response = await client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": f"""
Original Code:

{code}


Synthesized Report:

{report}
"""
            }
        ],
        response_format={
            "type": "json_object"
        },
        temperature=0
    )

    return json.loads(
        response.choices[0].message.content
    )

# %%
async def optimizer(code, feedback):

    system_prompt = f"""
You are an expert Senior Software Engineer.

Your responsibility is to improve the source code.

You MUST follow the evaluator feedback below.

Evaluator Feedback:

{feedback}

Rules:

1. Fix every issue mentioned.
2. Preserve the original functionality.
3. Improve readability.
4. Improve maintainability.
5. Improve performance whenever possible.
6. Apply security best practices.
7. Do NOT explain anything.
8. Return ONLY the improved source code.
"""

    response = await client.chat.completions.create(
        model=model,
        messages=[
            {
                "role":"system",
                "content":system_prompt
            },
            {
                "role":"user",
                "content":code
            }
        ],
        temperature=0.2
    )

    return response.choices[0].message.content

# %%
async def workflow(file=None, text=None):

    # -----------------------------
    # Step 1 : Validate Input
    # -----------------------------
    valid, code = await validate_input(
        file=file,
        text=text
    )

    if not valid:
        return code


    # -----------------------------
    # Step 2 : Router
    # -----------------------------
    route = await router(code)

    if route != "code_review":
        return "❌ Unsupported request."


    # -----------------------------
    # Step 3 : Run All Review Agents
    # -----------------------------
    results = await orchestrator(code)


    # -----------------------------
    # Step 4 : Generate Final Report
    # -----------------------------
    report = await synthesizer(results)


    # -----------------------------
    # Step 5 : Evaluate Report & Code
    # -----------------------------
    evaluation = await evaluator(
        code,
        report
    )


    # -----------------------------
    # Step 6 : Approved
    # -----------------------------
    if evaluation["approved"]:

        return {
            "status": "Approved",
            "report": report,
            "code": code
        }


    # -----------------------------
    # Step 7 : Optimize Code
    # -----------------------------
    improved_code = await optimizer(
        code,
        evaluation["feedback"]
    )


    # -----------------------------
    # Step 8 : Return Final Result
    # -----------------------------
    return {
        "status": "Optimized",
        "report": report,
        "code": improved_code,
        "feedback": evaluation["feedback"]
    }

# %%
async def review(code_text, code_file):

    result = await workflow(
        file=code_file,
        text=code_text
    )

    return result

# %%
with gr.Blocks(title="AI Multi-Agent Code Reviewer") as demo:

    gr.Markdown("# AI Multi-Agent Code Reviewer")

    gr.Markdown(
        "Upload a source code file or paste your code."
    )

    code_file = gr.File(
        label="Upload Code File"
    )

    code_text = gr.Textbox(
        lines=20,
        label="Paste Code"
    )

    output = gr.JSON(
        label="Analysis Result"
    )

    analyze_btn = gr.Button(
        "Analyze Code"
    )

    analyze_btn.click(
        fn=review,
        inputs=[
            code_text,
            code_file
        ],
        outputs=output
    )

demo.launch()


