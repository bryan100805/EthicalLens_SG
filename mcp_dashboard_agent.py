# mcp_dashboard_agent.py
import json
from agno.agent import RunResponse
from dashboard_agent import run_mcp_agent

# Instruction: fetch the full ethical_scores table as JSON
INSTRUCTIONS_FETCH_ALL_SCORES = """
You are an MCP SQL assistant. You will receive a SQL query in the message.
Use the read_query tool to execute that query against the database.
Return ONLY the result as a JSON array of objects, with no additional text or formatting.
"""

async def get_all_scores(max_retries: int = 3) -> RunResponse:
    sql = (
        "SELECT brand, date, labor_score, sourcing_score, carbon_score, "
        "animal_score, governance_score "
        "FROM ethical_scores;"
    )
    return await run_mcp_agent(
        message=sql,
        instructions=INSTRUCTIONS_FETCH_ALL_SCORES,
        max_retries=max_retries
    )

# INSTRUCTIONS_FETCH_SCATTER_JSON = """
# You are an MCP SQL assistant. Execute the given SQL query via read_query.
# Return ONLY the query result as a JSON array of objects, with keys:
#  - brand
#  - ethics_index
#  - revenue_musd
# Do not include any extra text or formatting.
# """

async def get_ethics_finance(max_retries: int = 3) -> RunResponse:
    sql = """
    WITH ethics_2024 AS (
      SELECT
        brand,
        ROUND(
          AVG(
            (labor_score
             + sourcing_score
             + carbon_score
             + animal_score
             + governance_score
            )/5.0
          ), 1
        ) AS ethics_index
      FROM ethical_scores
      WHERE date = '2024-09-01'
      GROUP BY brand
    )
    SELECT
      e.brand,
      e.ethics_index,
      f.revenue_musd
    FROM ethics_2024 e
    JOIN brand_financials f
      ON e.brand = f.brand
     AND f.year  = 2024;
    """
    return await run_mcp_agent(
        message=sql,
        instructions=INSTRUCTIONS_FETCH_ALL_SCORES,
        max_retries=max_retries
    )

# INSTRUCTIONS_FETCH_SECTOR_REGION_JSON = """
# You are an MCP SQL assistant. You will receive a SQL query in the message.
# Use the read_query tool to execute that query against the database.
# Return ONLY the result as a JSON array of objects with keys:
#   - sector
#   - region
#   - avg_labor
#   - avg_sourcing
#   - avg_carbon
#   - avg_animal
#   - avg_governance
# Do not include any extra text or formatting.
# """

async def get_sector_region_breakdown(max_retries: int = 3) -> RunResponse:
    sql = '''
    SELECT
      i.industry_sector   AS sector,
      i.hq_country        AS region,
      ROUND(AVG(e.labor_score),1)      AS avg_labor,
      ROUND(AVG(e.sourcing_score),1)   AS avg_sourcing,
      ROUND(AVG(e.carbon_score),1)     AS avg_carbon,
      ROUND(AVG(e.animal_score),1)     AS avg_animal,
      ROUND(AVG(e.governance_score),1) AS avg_governance
    FROM ethical_scores e
    JOIN brand_info    i
      ON e.brand = i.brand
    GROUP BY
      i.industry_sector,
      i.hq_country;
    '''
    return await run_mcp_agent(
        message=sql,
        instructions=INSTRUCTIONS_FETCH_ALL_SCORES,
        max_retries=max_retries,
    )