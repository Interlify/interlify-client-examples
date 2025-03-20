import asyncio
import os
from dotenv import load_dotenv

from openai import AsyncOpenAI

from agents import (
    Agent,
    OpenAIChatCompletionsModel,
    Runner,
    set_tracing_disabled,
    FunctionTool
)

from interlify import Interlify

load_dotenv()

BASE_URL = os.getenv("BASE_URL") or ""
API_KEY = os.getenv("API_KEY") or ""
MODEL_NAME = os.getenv("MODEL_NAME") or ""
INTERLIFY_API_KEY = os.getenv("INTERLIFY_API_KEY") or ""
PROJECT_ID = os.getenv("PROJECT_ID") or ""
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN") or ""


if not BASE_URL or not API_KEY or not MODEL_NAME or not INTERLIFY_API_KEY or not PROJECT_ID or not ACCESS_TOKEN:
    raise ValueError(
        "Please set BASE_URL, API_KEY, MODEL_NAME, INTERLIFY_API_KEY, PROJECT_ID, ACCESS_TOKEN via env var or code."
    )


client = AsyncOpenAI(base_url=BASE_URL, api_key=API_KEY)
set_tracing_disabled(disabled=True)

# Initialize the client
interlify = Interlify(
    api_key=INTERLIFY_API_KEY,
    project_id=PROJECT_ID,
    auth_headers=[{"Authorization": f"Bearer {ACCESS_TOKEN}"}],
)


# Prepare the tools
# tools = interlify.get_tools()

# Prepare tools for agent: convert tools to agent tools
agent_tools = interlify.openai_agent_tools()

async def main():

    agent = Agent(
        name="Assistant",
        instructions="You are a shoe shop assistant.",
        model=OpenAIChatCompletionsModel(model=MODEL_NAME, openai_client=client),
        tools=agent_tools,
    )

    result = await Runner.run(agent, "what shoes do you have?")
    print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())

