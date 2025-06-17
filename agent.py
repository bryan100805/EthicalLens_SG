import asyncio
import sys
if 'win32' in sys.platform:
    # Windows specific event-loop policy & cmd
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    cmds = [['C:/Windows/system32/HOSTNAME.EXE']]

import asyncio
import os
from dotenv import load_dotenv
from textwrap import dedent
from agno.agent import Agent, RunResponse
from agno.models.google import Gemini
from agno.tools.mcp import MCPTools
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from agno.utils.log import logger
from typing import Optional
from llm_model import get_model
import traceback

INSTRUCTIONS = dedent(
    """\
    You are EthicalLens SG's intelligent SQL assistant/graphical designer with access to a database through the MCP tool. You have access to these tables:
    - brand_financials: (brand, year, revenue_musd, profit_musd, employee_count)
    - brand_info: (brand, industry_sector, hq_country)
    - brand_sentiment: (brand, date, sentiment_score)
    - brand_store_presence: (brand, postal_district, store_count)
    - csr_report_index: (brand, year, report_count)
    - ethical_scores: (brand, date, labor_score, sourcing_score, carbon_score, animal_score, governance_score)
    - user_preferences: (user_id, brand, criterion, threshold)
    - user_votes: (brand, criterion, up_votes, down_votes)

    Your job is to:
    1. Understand the user's question or request related to data.
    2. Use the `get_schema` tool to retrieve the structure of the database, if needed.
    3. Generate a valid SQL `SELECT` query using the correct table and column names.
    4. Use the `read_query` tool to run your query and retrieve the results.
    5. Analyze the results and respond with a **clear, natural language summary** of the data.
       - This response should be simple, accurate, and easy to understand.
       - Focus on key insights, trends, counts, comparisons, or highlights.
       - Include numbers or observations, not just restatements.
       - Answer questions about ethics trends, comparisons, correlations, sentiment, or finance.
       - Avoid technical jargon or raw data unless specifically requested.

    Constraints:
    - Only use SELECT queries.
    - Do not perform INSERT, UPDATE, DELETE, or any modification operations.
    - Do not return raw SQL or result tables unless explicitly asked by the user.
    - Always return a human-friendly explanation, even if the result is empty or zero.

    Tools you can use:
    - `get_schema`: Retrieves the full schema of the database.
    - `read_query`: Executes a SELECT query and returns the result as a list of dictionaries.

    Examples of user queries:
    - "What is Nike's carbon_score trend for 2024?"
    - "Compare Patagonia vs Allbirds on animal_score and governance_score."
    - "Which brand has the highest sourcing_score as of 2025-06-01?"

    You MUST respond with:
    - A well-written, friendly summary of the result using only the data queried.
    - You may include a suitable short chart description if applicable.
    - If it involves **comparing trends or scores across multiple brands or criteria**, use grouped bar charts instead of line charts.
    - **If** you write "This could be shown as a <chart_type>.", provide insights of the graph, then **immediately** append a second paragraph containing a fully self-contained <div class="card bg-zinc-500 p-4 rounded-lg shadow-lg w-full h-64"> that:
       - Loads **Tailwind CSS** (via CDN).
       - Loads **Chart.js** (inline script tag from CDN).
       - Use intuitive colors and layout.
       - Add title and description to the chart.
       - Ensure that the x axis and y axis limits are set to the data range.
       - Make the layout mobile-friendly, elegant, and readable.
       - Wrap the chart's <canvas> in a <div> with Tailwind classes `w-65 h-50`.
       - Do not include extra explanations or comments — just the HTML.
       - Renders the chart using exactly the data you just described.
       - Uses Chart.js config:
         ```js
         options: {
           responsive: true,
           maintainAspectRatio: false
         }
         ```
    - **Nothing else — no explanations of how you got the result.**

    Before answering, review the last three user-assistant exchanges for context and carry the conversational thread.
    """
)

# Load environment variables from .env file
load_dotenv()
# DB_HOST = os.getenv("DB_HOST", "localhost")
# DB_USER = os.getenv("DB_USER", "root")
# DB_PASSWORD = os.getenv("DB_PASSWORD", "P@ssword1234")
# DB_NAME = os.getenv("DB_NAME", "ethical_scores")
MODEL_API_KEY = os.getenv("MODEL_API_KEY", "")
# Fallback default model ID
default_id = os.getenv("MODEL_ID", "gemini-2.0-flash")


async def db_connection_agent(session: ClientSession, model_id: Optional[str] = None) -> Agent:
    """
    Creates and configures an agent that interacts with an SQL database via MCP.

    Args:
        session (ClientSession): The MCP client session.
        model_id (Optional[str]): The ID of the language model to use. Defaults to DEFAULT_MODEL_ID.

    Returns:
        Agent: The configured agent.

    """
    # Use default if model_id is None
    model_id = model_id or default_id
    
    # Initialize the MCP toolkit
    mcp_tools = MCPTools(session=session)
    await mcp_tools.initialize()
    
    # Create and return the configured agent
    return Agent(
        model=get_model(model_id,MODEL_API_KEY),
        tools=[mcp_tools],
        instructions=INSTRUCTIONS,
        markdown=True,
        show_tool_calls=True,
    )


async def run_agent(message: str, conversation_history: Optional[list]=None, model_id: Optional[str] = None) -> RunResponse:
    """
    Runs the agent with the given message and returns the response.

    Args:
        message (str): The message to send to the agent.
        model_id (Optional[str]): The ID of the language model to use. Defaults to DEFAULT_MODEL_ID.

    Returns:
        RunResponse: The agent's response.

    Raises:
        ValueError: If any of the required database environment variables are not set.
        RuntimeError: If there is an error connecting to the MCP server.
    """
    if conversation_history:
        # history is list of dicts: {"role":...,"content":...}
        history_text = "".join([
            f"{turn['role']}: {turn['content']}\n"
            for turn in conversation_history[-6:]
        ])
        message = f"\n{history_text}\nUser: {message}"
    print(f"Running agent with message: {message}")
    # Use default if model_id is None
    model_id = model_id or default_id
    # Check for required database environment variables
    # required_vars = ["DB_HOST", "DB_USER", "DB_PASSWORD", "DB_NAME"]
    # missing_vars = [var for var in required_vars if not os.getenv(var)]
    # if missing_vars:
    #     raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")

    # Configure MCP server parameters
    server_params = StdioServerParameters(
        command="uvx",
        args=[
            "mcp-sql-server",
            "--db-host",
            "localhost",
            "--db-user",
            "root",
            "--db-password",
            "P@ssword1234",
            "--db-database",
            "ethical_scores",
        ],
    )

    # Connect to the MCP server and run the agent
    try:
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                agent = await db_connection_agent(session, model_id)
                response = await agent.arun(message)
                return response
    except Exception as e:
        print("Original exception:", e)
        raise RuntimeError(f"Error connecting to MCP server or running agent: {e}") from e


async def main():
    """
    Example usage of the agent.
    """
    try:
        # Run the agent with a sample query
        history = [
            {"role":"user","content":"Show me the labor scores."},
            {"role":"assistant","content":"Here are the labor scores for June 2025."},
            {"role":"user","content":"Now compare sourcing scores."},
        ]
        response = await run_agent("Plot sourcing trends over the last year.", conversation_history=history)
        logger.info(f"Agent Response: {response.content}")
    except ValueError as ve:
        logger.error(f"Configuration error: {ve}")
    except RuntimeError as re:
        logger.error(f"Runtime error: {re}")
    # in agent.py -> run_agent
    except Exception as e:
        print("Original exception:", e)
        raise RuntimeError(f"Error connecting to MCP server or running agent: {e}") from e


if __name__ == "__main__":
    asyncio.run(main())