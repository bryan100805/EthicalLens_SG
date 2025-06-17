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
from brand_agent import get_brand_list, get_brand_details
from typing import Dict, Any
import traceback
import re
import json


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
hero, _ = st.columns([3,1])
with hero:
    st.markdown("# 🛒 EthicalLens SG")
    st.markdown(
        "With Model Context Protocol (MCP), interact with a real-time MySQL database using **natural language** and get instant charts & alerts."
    )

# Sidebar
with st.sidebar.expander("ℹ️ About / How to use", expanded=False):
    st.markdown(
        """
        **This app** lets you chat with an SQL DB and spin up instant dashboards.  
        **How to use:**  
        1. Start your MCP SQL server  
        2. Ask natural-language questions under **Chatbot**  
        3. View your insights under **Dashboard**  
        4. Check the **Home** tab for our Weekly Spotlight  

        👨‍💻 Contribute on [GitHub](https://github.com/bryan100805)
        """
    )

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
if "brand_list" not in st.session_state:
    st.session_state.brand_list = []
if "watchlist" not in st.session_state:
    st.session_state.watchlist = []
if "alerts" not in st.session_state:
    st.session_state.alerts = []  # list of (brand,metric,value)
if "selected_brand" not in st.session_state:
    st.session_state.selected_brand = None
if "selected_watch_brand" not in st.session_state:
    st.session_state.selected_watch_brand = None

# Tabs
tab_home, tab_brand, tab_watch, tab1, tab2 = st.tabs(["Home", "Brands", "Watchlist", "Chatbot", "Dashboard"])

# --- HOME TAB: Weekly Spotlight Newsletter ---
with tab_home:
    st.markdown(
    """
    <style>
    .tg-date {
        text-align: right;
        color: #888;
        font-size: 12px;
        margin: 10px 20px 4px 0;
    }
    """
    , unsafe_allow_html=True)
    st.subheader("📬 Weekly Spotlight")
    st.markdown(
        "Welcome to the Weekly Spotlight! Here, we highlight key trends and updates in ethical consumerism. "
        "Stay informed about the latest developments in sustainable brands and their impact on our planet."
    )
    st.markdown("---")
    st.markdown('<div class="tg-date">June 21</div>', unsafe_allow_html=True)
    st.image("image/patogonia_carbon_footprint.png", width=400)
    st.subheader("Weekly Spotlight: Patagonia")
    st.write(
        "- 🌱 **Carbon Footprint**: Improved by +6 pts (76 → 82)\n"
        "- 🤝 **Labor Policies**: Steady at 88\n"
        "- 🔍 **Sourcing Transparency**: +4 pts (70 → 74)"
    )
    st.markdown(
        "*💚 Wow, Patagonia just knocked 6pts off their carbon score, total eco-heroes move!* 😎\n"
        "*Can't wait to see if they keep that green glow-up going in their factories too!*",
        unsafe_allow_html=True,
    )

    # -- Init heart count & toggle --
    count_key  = "post1_heart"
    toggle_key = "post1_heart_toggled"
    if count_key not in st.session_state:
        st.session_state[count_key] = 7
    if toggle_key not in st.session_state:
        st.session_state[toggle_key] = False

    # -- Single heart button --
    cnt = st.session_state[count_key]
    if st.button(f"❤️ {cnt}", key="post1_heart_btn"):
        # flip the toggle and adjust count
        st.session_state[toggle_key] = not st.session_state[toggle_key]
        st.session_state[count_key] += 1 if st.session_state[toggle_key] else -1

    st.markdown("---")

    # ---- Post 2: Top Movers ----
    st.markdown('<div class="tg-date">June 21</div>', unsafe_allow_html=True)
    st.image("image/brands_top_movers.png", width=400)
    st.subheader("Top Movers This Week")
    st.write(
        "- **Allbirds**: Animal Welfare +4 pts 📈\n"
        "- **Adidas**: Sourcing Transparency -3 pts 📉\n"
        "- **Nike**: Labor Policies -2 pts 📉"
    )
    st.markdown(
        "*🐦 Allbirds is straight-up slaying the animal welfare game-major props!* 🎉\n"
        "*Adidas, we need that behind-the-scenes tea ☕️ on where your materials come from, and Nike… let's pick up the pace on worker care!*",
        unsafe_allow_html=True,
    )
    # -- Init heart count & toggle --
    count_key2  = "post2_heart"
    toggle_key2 = "post2_heart_toggled"
    if count_key2 not in st.session_state:
        st.session_state[count_key2] = 11
    if toggle_key2 not in st.session_state:
        st.session_state[toggle_key2] = False

    # -- Single heart button --
    cnt2 = st.session_state[count_key2]
    if st.button(f"❤️ {cnt2}", key="post2_heart_btn"):
        # flip the toggle and adjust count
        st.session_state[toggle_key2] = not st.session_state[toggle_key2]
        st.session_state[count_key2] += 1 if st.session_state[toggle_key2] else -1
    st.markdown("---")

# --- BRANDS TAB ---
with tab_brand:
    st.subheader("🏷️ All Brands")
    st.write("Search & filter all brands, add to your watchlist, or view details.")
    st.markdown("---")

    # Load brand list once
    if not st.session_state.brand_list:
        with st.spinner("Loading brands..."):
            resp = asyncio.run(get_brand_list())
            raw = resp.content.strip()
            if raw.startswith("```json"): raw = raw[7:]
            if raw.endswith("```"):      raw = raw[:-3]
            try:
                st.session_state.brand_list = json.loads(raw)
            except:
                st.error("Could not parse brand list.")

    # Filter input
    search = st.text_input("Filter brands by name…")
    filtered = [
        b for b in st.session_state.brand_list
        if not search or search.lower() in b.lower()
    ]

    # List each brand with its own Watch/Details buttons
    for brand in filtered:
        col_name, col_view, col_watch = st.columns([4,1,1], gap="small")
        with col_name:
            st.write(brand)
        with col_view:
            if st.button("🔍 Details", key=f"details_{brand}"):
                st.session_state.selected_brand = brand
        with col_watch:
            if brand in st.session_state.watchlist:
                if st.button("✔️ Watching", key=f"watch_{brand}"):
                    st.session_state.watchlist.remove(brand)
                    st.toast(f"Removed {brand} from watchlist")
            else:
                if st.button("☆ Watch", key=f"watch_{brand}"):
                    st.session_state.watchlist.append(brand)
                    st.toast(f"Added {brand} to watchlist")

    # Brand Detail View
    if st.session_state.selected_brand:
        b = st.session_state.selected_brand
        if st.button("← Back to Brands"):
            st.session_state.selected_brand = None
        st.subheader(f"🔍 {b} — Details")


        # Ethical scores
        q1 = f"""
            SELECT brand, date AS latest_date,
                   labor_score, sourcing_score, carbon_score,
                   animal_score, governance_score
              FROM ethical_scores
             WHERE brand='{b}'
          ORDER BY date DESC LIMIT 1;
        """
        r1 = asyncio.run(get_brand_details(q1))
        raw1 = r1.content.strip().removeprefix("```json").removesuffix("```")
        scores = json.loads(raw1)[0]

        # Financials
        q2 = f"""
            SELECT brand, year AS latest_year,
                   revenue_musd, profit_musd, employee_count
              FROM brand_financials
             WHERE brand='{b}'
          ORDER BY year DESC LIMIT 1;
        """
        r2 = asyncio.run(get_brand_details(q2))
        raw2 = r2.content.strip().removeprefix("```json").removesuffix("```")
        fin = json.loads(raw2)[0]

        # Display Ethical Scores
        st.caption(f"Last updated: {scores['latest_date']} • Source: CSR Q4 2024 §3.2")
        r1c = st.columns(3)
        r1c[0].metric("🌱 Labor",    scores["labor_score"])
        r1c[1].metric("🔍 Sourcing",  scores["sourcing_score"])
        r1c[2].metric("⚡ Carbon",    scores["carbon_score"])
        r2c = st.columns(2)
        r2c[0].metric("🐾 Animal",     scores["animal_score"])
        r2c[1].metric("🏛️ Governance", scores["governance_score"])

        st.markdown("---")
        # Display Financials
        st.subheader(f"💰 Financials ({fin['latest_year']})")
        st.caption("Source: Company Annual Report")
        fc = st.columns(3)
        fc[0].metric("Revenue (M USD)", f"{fin['revenue_musd']:,}")
        fc[1].metric("Profit (M USD)",  f"{fin['profit_musd']:,}")
        fc[2].metric("Employees",       f"{fin['employee_count']:,}")


# --- WATCHLIST TAB (with live‐updating Pending Alerts) ---
with tab_watch:
    st.subheader("📑 My Watchlist")
    st.write("Manage watched brands and set custom alerts on their ethical metrics.")
    st.markdown("---")

    # 1) Create a placeholder for the alerts metric
    alerts_placeholder = st.empty()
    # Initial render
    alerts_placeholder.metric("🔔 Pending Alerts", len(st.session_state.alerts))

    if not st.session_state.watchlist:
        st.info("Your watchlist is empty. Add brands from the Brands tab.")
    else:
        # 2) Collect metrics for Set Alerts button
        metrics_by_brand = {}

        for brand in st.session_state.watchlist:
            with st.expander(f"⭐ {brand}", expanded=False):
                # (stub) fetch current metrics
                metrics = {
                    "Labor":      88,
                    "Sourcing":   74,
                    "Carbon":     82,
                    "Animal":     90,
                    "Governance": 85,
                }
                metrics_by_brand[brand] = metrics

                # show metrics cards
                cols = st.columns(len(metrics))
                for col, (n, v) in zip(cols, metrics.items()):
                    col.metric(n, v)
                st.caption("Data sources: CSR 2024, NEA registry")

                # threshold inputs
                st.markdown("**Alert Thresholds**")
                thresh_cols = st.columns(len(metrics))
                for col, (n, v) in zip(thresh_cols, metrics.items()):
                    key = f"watch_th_{brand}_{n}"
                    if key not in st.session_state:
                        st.session_state[key] = v
                    col.number_input(
                        f"{n} ≥", min_value=0, max_value=100,
                        value=st.session_state[key],
                        key=key
                    )

        # 3) Single “Set Alerts” button
        if st.button("Set Alerts"):
            new = 0
            for brand, metrics in metrics_by_brand.items():
                for name, val in metrics.items():
                    threshold = st.session_state[f"watch_th_{brand}_{name}"]
                    alert = (brand, name, val)
                    if val >= threshold and alert not in st.session_state.alerts:
                        st.session_state.alerts.append(alert)
                        new += 1
            if new:
                st.toast(f"🔔 {new} new alert(s) set.")
            else:
                st.success("No new alerts to add.")

            # 4) Immediately re-render the metric
            alerts_placeholder.metric("🔔 Pending Alerts", len(st.session_state.alerts))

        st.markdown("---")

        # 5) Unwatch and ensure alerts for removed brands are cleared
        for brand in st.session_state.watchlist.copy():
            col1, col2 = st.columns([4, 1], gap="small")
            with col1:
                st.write(brand)
            with col2:
                if st.button("✖ Unwatch", key=f"watch_un_{brand}"):
                    st.session_state.watchlist.remove(brand)
                    # remove any alerts for that brand
                    st.session_state.alerts = [
                        a for a in st.session_state.alerts if a[0] != brand
                    ]
                    st.toast(f"Removed {brand} and its alerts")
                    alerts_placeholder.metric("🔔 Pending Alerts", len(st.session_state.alerts))

# Chatbot Tab
with tab1:
    st.subheader("💬 Chatbot")
    st.markdown("Pick a starter or type your own question below:")

    # Conversation-starter buttons
    starters = [
        "What is Nike's carbon_score trend for all the unique years?",
        "Compare Patagonia vs Allbirds on animal score.",
        "Which brand has the highest governance score on 1st Jun 2025?",
        "Show me the sourcing trends across every brand for all the unique years."
    ]
    cols = st.columns(len(starters))
    clicked = None
    for col, text in zip(cols, starters):
        if col.button(text, key=f"starter_{text}"):
            clicked = text
    # Create a container for the chat messages
    chat_container = st.container()

    # Add an id to the chat container
    chat_container.markdown('<div id="chat-container"></div>', unsafe_allow_html=True)

    # Display chat history within the container
    with chat_container:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    typed_query = st.chat_input(
        "Ask a question about the database (e.g., What is Nike's carbon_score trend for 2024?)"
    )

    user_query = clicked or typed_query


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
with tab2:
    st.header("Brand Overview")

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
