import asyncio
import sys
if 'win32' in sys.platform:
    # Windows specific event-loop policy & cmd
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    cmds = [['C:/Windows/system32/HOSTNAME.EXE']]

import streamlit as st
import asyncio
import json
from agent import run_agent
from dashboard_agent import run_agent as run_dashboard_agent
from typing import Dict, Any
import traceback
import re


st.set_page_config(
    page_title="EthicalLens SG",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Report a bug": "https://github.com/bryan100805"
    }
)

# Title and Header
st.title("🛒 EthicalLens SG")
st.write(
    "Interact with an SQL database using natural language and visualize database trends. "
    "This app connects to an MCP SQL server to execute your queries, provide results, and generate dashboards."
)

# Sidebar
with st.sidebar:
    st.header("ℹ️ About")
    st.markdown(
        "This application allows you to interact with an SQL database using natural language and visualize data. "
        "It leverages the MCP (Modular Control Protocol) to connect to an SQL server, "
        "execute your queries, present the results, and generate interactive dashboards."
    )
    st.markdown(
        "**How to use:**\n"
        "1. Ensure the MCP SQL server is running.\n"
        "2. Ask your questions in the chat box below.\n"
        "3. The app will generate and execute the appropriate SQL query.\n"
        "4. The results will be displayed in the chat.\n"
        "5. Navigate to the 'Dashboard' tab to view database insights."
    )
    st.markdown("👨‍💻 Developed as an AI experiment. Contribute on [GitHub](https://github.com/bryan100805)")


def display_html_dashboard(html_content: str):
    """Displays the HTML dashboard in Streamlit."""
    st.components.v1.html(html_content, height=800, scrolling=True)


# --- Main App Logic ---

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "conversation_state" not in st.session_state:
    st.session_state.conversation_state = {}
if "dashboard_html" not in st.session_state:
    st.session_state.dashboard_html = ""

# Tabs
tab1, tab2 = st.tabs(["Chatbot", "Dashboard"])

# Chatbot Tab
with tab1:
    # Create a container for the chat messages
    chat_container = st.container()

    # Add an id to the chat container
    chat_container.markdown('<div id="chat-container"></div>', unsafe_allow_html=True)

    # Display chat history within the container
    with chat_container:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # User input
    user_query = st.chat_input("Ask a question about the database (e.g., What is Nike's carbon_score trend for 2024?)", key="chat_input")

    if user_query:
        st.session_state.messages.append({"role": "user", "content": user_query})

        # Display the user message immediately
        with chat_container:
            with st.chat_message("user"):
                st.markdown(user_query)

        with st.spinner("Fetching response from the database..."):
            try:
                resp = asyncio.run(
                    run_agent(
                        user_query,
                        conversation_history=st.session_state.messages
                    )
                )
            # in app.py
            except Exception as e:
                tb = traceback.format_exc()
                st.error(f"An error occurred:\n{e}\n{tb}")
                raise
            except Exception as e:
                st.error(f"An error occurred: {e}")
                resp = None

        if resp:
            # # Add assistant's response to session state
            # st.session_state.messages.append({"role": "assistant", "content": resp.content})

            # Display the assistant message immediately
            with chat_container:
                with st.chat_message("assistant"):
                    content = resp.content.strip()

                    # strip ```html fences if present
                    if content.startswith("```html"):
                        content = content[7:]
                    if content.endswith("```"):
                        content = content[:-3]
                    marker = '<div class="card bg-zinc-500 p-4 rounded-lg shadow-lg w-full h-64">'
                    if marker in content and "<script" in content:
                        text_part, html_part = content.split(marker, 1)
                        html_snippet = marker + html_part
                        # Add assistant's response to session state
                        st.session_state.messages.append({"role": "assistant", "content": text_part}) 
                        st.markdown(text_part)  
                              
                        st.components.v1.html(html_snippet, height=400, scrolling=False)
                    else:
                        st.markdown(content)
                        st.session_state.messages.append({"role": "assistant", "content": content})                               



# Dashboard Tab
# with tab2:
#     st.header("Database Dashboard")

#     # # 1) Fetch raw data: all five scores per brand & date
#     # sql = """
#     #   SELECT
#     #     date,
#     #     brand,
#     #     labor_score,
#     #     sourcing_score,
#     #     carbon_score,
#     #     animal_score,
#     #     governance_score
#     #   FROM ethical_scores
#     #   ORDER BY date, brand;
#     # """
#     # chart_resp = asyncio.run(run_dashboard_agent(
#     #     "Analyse my database and suggest a dashboard"+sql    ))
#     # # try:
#     # #     rows = json.loads(resp.content)
#     # # except Exception:
#     # #     rows = []

#     # # if not rows:
#     # #     st.info("No data available.")
#     # # else:
#     # #     # 2) Build a JSON metrics prompt for the agent
#     # #     metrics_payload = {
#     # #         "domain": "ethical consumerism",
#     # #         "key_metrics": [{
#     # #             "metric": "all_ethics",
#     # #             "description": "All five ethical scores by brand and date",
#     # #             "visualization_type": "bar_chart",
#     # #             "visualization_rationale": "Grouped bars showing each score category for every brand-date pair",
#     # #             "data": rows
#     # #         }],
#     # #         "dashboard_components": ["bar_chart"]
#     # #     }

#     # #     # 3) Ask Gemini to render the grouped bar chart snippet
#     # #     chart_prompt = json.dumps(metrics_payload)
#     # #     chart_resp  = asyncio.run(run_dashboard_agent(chart_prompt))
#     # chart_html  = chart_resp.content.strip()

#     # # 4) Strip any ```html fences
#     # if chart_html.startswith("```html"):
#     #     chart_html = chart_html[len("```html"):]
#     # if chart_html.endswith("```"):
#     #     chart_html = chart_html[:-3]

#     # display_html_dashboard(chart_html)
#     # # 5) Embed the AI‐generated snippet
#     # st.components.v1.html(chart_html, height=500, scrolling=False)

#     if st.button("Generate Dashboard"):
#         with st.spinner("Analyzing database and generating dashboard..."):
#             try:
#                 dashboard_response = asyncio.run(run_dashboard_agent("Analyse my database and suggest a dashboard"))
#                 #remove  ```html if present
#                 __html = dashboard_response.content
#                 if __html.startswith("```html"):
#                     __html =  __html.replace("```html", "")
#                     if __html.endswith("```"):
#                         __html = __html.replace("```", "")
#                 st.session_state.dashboard_html = __html
#                 display_html_dashboard(__html)

#             except Exception as e:
#                 st.error(f"An error occurred: {e}")
                
#     if st.session_state.dashboard_html:
#         st.download_button(
#             label="Download Dashboard HTML",
#             data=st.session_state.dashboard_html,
#             file_name="dashboard.html",
#             mime="text/html",
#         )
