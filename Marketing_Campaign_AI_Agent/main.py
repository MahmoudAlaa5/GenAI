import os
from dotenv import load_dotenv
from openai import AsyncOpenAI
import gradio as gr
import json
import asyncio

load_dotenv(override=True)


def main():

    model = "openai/gpt-oss-20b:free"

    system_prompt = """
    You are a message router.

    Your task is to classify the user message.

    Example routes:

    1. greeting:
    - Hello
    - Hi
    - Thanks
    - How are you

    2. marketing:
    - Creating campaigns
    - Product promotion
    - Audience analysis
    - Marketing strategy

    Return ONLY a valid JSON object.

Do not explain.
Do not use markdown.
Do not wrap it inside ```json.
Do not output anything except JSON.

Examples:

{"route":"greeting"}

{"route":"marketing"}
    """

    client = AsyncOpenAI(
        api_key=os.getenv("OPENROUTER_API_KEY"),
        base_url="https://openrouter.ai/api/v1"
    )

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

    async def make_subtasks(task):

        response = await client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": "Split Marketing task into 3 subtasks"
                },
                {
                    "role": "user",
                    "content": task
                }
            ],
        )

        steps = [
            s.strip(" .")
            for s in response.choices[0].message.content.split("\n")
            if s.strip()
        ]

        return steps[:3]

    async def decision_making(user_message):

        route = await router(user_message)

        if route == "greeting":
            return "Hello! How can I help you today?"

        elif route == "marketing":
            return await make_subtasks(user_message)

        return None

    async def Agent_Experts(role, task):

        role_prompts = {
            "Researcher": "You are a Market researcher. Analyze audience needs.",
            "Copywriter": "You are a copywriter. Write catchy ad copy.",
            "Planner": "You are a campaign planner. Suggest a weekly schedule."
        }

        response = await client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": role_prompts[role]
                },
                {
                    "role": "user",
                    "content": task
                }
            ],
            temperature=0.6
        )

        return f"--- {role} ---\n{response.choices[0].message.content}"

    async def paralize(task):

        roles = ["Researcher", "Copywriter", "Planner"]

        tasks = [Agent_Experts(r, task) for r in roles]

        results = await asyncio.gather(*tasks)

        return "\n\n".join(results)

    async def review_and_optimize(text):

        review = await client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": "Review if this marketing content is clear, persuasive and actionable. Reply 'yes' or 'no' and give feedback."
                },
                {
                    "role": "user",
                    "content": text
                }
            ],
            temperature=0
        )

        feedback = review.choices[0].message.content.strip().lower()

        if "yes" in feedback:

            return text + "\n\n✅ Approved by Marketing Reviewer"

        else:

            improved = await client.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role": "system",
                        "content": f"Improve the marketing content based on this feedback: {feedback}"
                    },
                    {
                        "role": "user",
                        "content": text
                    }
                ],
                temperature=0.5
            )

            return (
                improved.choices[0].message.content
                + "\n\n✅ Improved after review"
            )

    async def Agent_Workflow(user_input):

        decision = await decision_making(user_input)

        if decision is None:
            return "If you have any question, tell me!"

        if isinstance(decision, str):
            return decision

        subtasks = decision

        parallel_results = await paralize(
            " | ".join(subtasks)
        )

        final = await review_and_optimize(
            parallel_results
        )

        return final

    async def chat(message, history):

        response = await Agent_Workflow(message)

        return response

    demo = gr.ChatInterface(
        fn=chat,
        title="Marketing Campaign AI Agent",
        description="An AI Agent that creates marketing campaigns."
    )

    demo.launch(share=True)


if __name__ == "__main__":
    main()