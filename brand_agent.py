# brand_agent.py
import json
from typing import Optional
from agno.agent import RunResponse
from dashboard_agent import run_mcp_agent

# Instruction set for fetching just the list of brand names
INSTRUCTIONS_BRAND_LIST_JSON = """
You are an MCP SQL assistant. You will receive a SQL query in the message.
Use the read_query tool to execute that query against the database.
Return ONLY the result as a JSON array of strings (the brand names), with no extra explanation.
"""

# Instruction set for fetching a single row’s details as JSON
INSTRUCTIONS_BRAND_DETAIL_JSON = """
You are an MCP SQL assistant. You will receive a SQL query in the message.
Use the read_query tool to execute that query against the database.
Return ONLY the result as a JSON array containing one object with column names as keys.
"""

async def get_brand_list(max_retries: int = 3) -> RunResponse:
    sql = "SELECT DISTINCT brand FROM ethical_scores;"
    return await run_mcp_agent(
        message=sql,
        instructions=INSTRUCTIONS_BRAND_LIST_JSON,
        max_retries=max_retries,
    )

async def get_brand_details(sql_query: str, max_retries: int = 3) -> RunResponse:
    return await run_mcp_agent(
        message=sql_query,
        instructions=INSTRUCTIONS_BRAND_DETAIL_JSON,
        max_retries=max_retries,
    )
