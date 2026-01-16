from arcadepy import AsyncArcade
from dotenv import load_dotenv
from google.adk import Agent, Runner
from google.adk.artifacts import InMemoryArtifactService
from google.adk.models.lite_llm import LiteLlm
from google.adk.sessions import InMemorySessionService, Session
from google_adk_arcade.tools import get_arcade_tools
from google.genai import types
from human_in_the_loop import auth_tool, confirm_tool_usage

import os

load_dotenv(override=True)


async def main():
    app_name = "my_agent"
    user_id = os.getenv("ARCADE_USER_ID")

    session_service = InMemorySessionService()
    artifact_service = InMemoryArtifactService()
    client = AsyncArcade()

    agent_tools = await get_arcade_tools(
        client, toolkits=["Walmart"]
    )

    for tool in agent_tools:
        await auth_tool(client, tool_name=tool.name, user_id=user_id)

    agent = Agent(
        model=LiteLlm(model=f"openai/{os.environ["OPENAI_MODEL"]}"),
        name="google_agent",
        instruction="# Introduction
Welcome to the Walmart Product Search AI Agent! This agent is designed to help users find detailed information about products available at Walmart. By using advanced search capabilities, the agent can quickly retrieve product listings based on specified keywords and provide further details on selected items.

# Instructions
1. Begin by accepting user input for product keywords and any additional filters (price range, next-day delivery preference).
2. Use the **Walmart_SearchProducts** tool to find relevant products based on the provided keywords and filters.
3. Once the search results are obtained, present the user with a list of products, including their names and prices.
4. If the user requests more details about a specific product, retrieve the item's ID and use the **Walmart_GetProductDetails** tool to fetch and display comprehensive information.

# Workflows

## Workflow 1: Product Search
1. **Input**: Accept keywords from the user (and optional filters for price and delivery).
2. **Tool**: Use **Walmart_SearchProducts** with the provided keywords and filters.
3. **Output**: Display a list of product names and prices to the user.

## Workflow 2: Product Details Retrieval
1. **Input**: Accept a specific product selection from the user.
2. **Tool**: Retrieve the item's ID from the selected product.
3. **Tool**: Use **Walmart_GetProductDetails** with the retrieved item ID.
4. **Output**: Present detailed product information, including specifications, images, and availability.",
        description="An agent that uses Walmart tools provided to perform any task",
        tools=agent_tools,
        before_tool_callback=[confirm_tool_usage],
    )

    session = await session_service.create_session(
        app_name=app_name, user_id=user_id, state={
            "user_id": user_id,
        }
    )
    runner = Runner(
        app_name=app_name,
        agent=agent,
        artifact_service=artifact_service,
        session_service=session_service,
    )

    async def run_prompt(session: Session, new_message: str):
        content = types.Content(
            role='user', parts=[types.Part.from_text(text=new_message)]
        )
        async for event in runner.run_async(
            user_id=user_id,
            session_id=session.id,
            new_message=content,
        ):
            if event.content.parts and event.content.parts[0].text:
                print(f'** {event.author}: {event.content.parts[0].text}')

    while True:
        user_input = input("User: ")
        if user_input.lower() == "exit":
            print("Goodbye!")
            break
        await run_prompt(session, user_input)


if __name__ == '__main__':
    import asyncio
    asyncio.run(main())