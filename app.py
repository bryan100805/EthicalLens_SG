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
import plotly.express as px
from mcp_dashboard_agent import get_all_scores, get_ethics_finance, get_sector_region_breakdown
import pandas as pd
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
        "Report a bug": "https://github.com/bryan100805/EthicalLens_SG/issues"
    }
)

# Title and Header
hero, _ = st.columns([3,1])
with hero:
    st.markdown("# 🛒 EthicalLens SG")
    st.write(
    "Empower your shopping with full transparency on labor practices, sourcing, carbon footprint, "
    "animal welfare, and corporate governance.  \n"
    "EthicalLens SG helps you track, compare, and set alerts on your favorite brands'",
    "ethical scores - all in one place. \n\n"
    "Chat with our AI assistant to get instant insights, or explore our interactive dashboard for deeper analysis. \n"
)

# Sidebar
with st.sidebar.expander("ℹ️ Getting Started", expanded=False):
    st.markdown("""
        **1.** Start your MCP SQL server so EthicalLens SG can fetch up-to-date brand data.\n
        **2.** Visit **Home** for our Weekly Spotlight on trending brands.\n
        **3.** Browse **Brands** to search, filter, and add to your Watchlist.\n
        **4.** In **Watchlist**, click ✔️ or ⚠️ to view details and set alert thresholds.\n
        **5.** Use **Chatbot** for ad-hoc, natural-language queries against your data.\n
        **6.** Under **Dashboard**, hit **Generate** for interactive multi-chart metrics.\n\n

        👨‍💻 Contribute on [GitHub](https://github.com/bryan100805)
    """)

# METRIC DEFINITIONS 
with st.sidebar.expander("Metric Definitions", expanded=False):
    st.markdown(
        """
        **🌱 Labor Score** <span title="Measures company labor conditions: fair wages, working hours, and safety protocols.">ⓘ</span>  
        **🔍 Sourcing Score** <span title="Assesses transparency of raw-material sourcing and supplier audits.">ⓘ</span>  
        **⚡ Carbon Score** <span title="Tracks greenhouse-gas emissions and reduction initiatives.">ⓘ</span>  
        **🐾 Animal Score** <span title="Evaluates animal testing policies and cruelty-free product lines.">ⓘ</span>  
        **🏛️ Governance Score** <span title="Rates board oversight, ethics policies, and anti-corruption measures.">ⓘ</span>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
    """
    <style>
    /* Custom tooltip styling */
    .tooltip {
      position: relative;
      display: inline-block;
      cursor: help;
    }
    .tooltip .tooltiptext {
      visibility: hidden;
      width: 220px;
      background-color: #2f7a4f;
      color: #fff;
      text-align: left;
      border-radius: 6px;
      padding: 8px;
      position: absolute;
      z-index: 9999;
      bottom: 125%; /* position above */
      left: 50%;
      transform: translateX(-50%);
      opacity: 0;
      transition: opacity 0.2s;
      box-shadow: 0 2px 6px rgba(0,0,0,0.3);
      font-size: 0.9rem;
      line-height: 1.2;
    }
    .tooltip:hover .tooltiptext {
      visibility: visible;
      opacity: 1;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Function to display HTML dashboard
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
tab_home, tab_brand, tab_watch, tab_chatbot, tab_dash = st.tabs(["Home", "Brands", "Watchlist", "Chatbot", "Dashboard"])

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
    st.markdown(
        "*🔍 Insider scoop: Rumor has it their switch to 100% recycled polyester last quarter gave 'em that big carbon drop!* 🧐\n"
        "*🤝 And hey, holding steady on labor means those fair-wage programs are paying off - GO TEAM!*",
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
    st.markdown('<div class="tg-date">June 14</div>', unsafe_allow_html=True)
    st.image("image/brands_top_movers.png", width=400)
    st.subheader("Top Movers This Week")
    st.write(
        "- **Allbirds**: Animal Welfare +4 pts 📈\n"
        "- **Adidas**: Sourcing Transparency -3 pts 📉\n"
        "- **Nike**: Labor Policies -2 pts 📉"
    )
    st.markdown(
        """
        *🐦 Allbirds jumped after launching their new faux-leather alternative-cruelty-free fans are cheering!* 🎉\n
        *🌍 Adidas dipped when a third-party audit flagged gaps in their raw material traceability, watch for fixes soon!* 🔍\n
        *👷‍♂️ Nike's slight labor slip likely stems from a factory expansion rollout—hopefully they'll train those new workers up to standard!* 🚀,

        """, unsafe_allow_html=True
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
with tab_chatbot:
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
with tab_dash:
    st.subheader("📊 Dashboard")
    st.write("Click **Generate Dashboard** to load data and render interactive charts.")
    st.markdown("---")

    # 1) Load & cache data
    if st.button("Generate Dashboard"):
        with st.spinner("Loading and processing data..."):
            resp = asyncio.run(get_all_scores())
            raw = resp.content.strip().removeprefix("```json").removesuffix("```")
            df = pd.DataFrame(json.loads(raw))
            df["date"] = pd.to_datetime(df["date"])
            st.session_state.df = df

    # 2) If we have data, show filters + charts
    if "df" in st.session_state:
        df = st.session_state.df

        # Filtering controls
        st.markdown("> **Filter Controls:** Select up to 10 brands and choose a date range to narrow down your charts.")
        all_brands = sorted(df["brand"].unique())
        selected_brands = st.multiselect(
            "Select up to 10 brands",
            options=all_brands,
            default=all_brands[:10],
            max_selections=10
        )
        df["date_only"] = df["date"].dt.date
        min_d, max_d = df["date_only"].min(), df["date_only"].max()
        dr = st.date_input("Date range", value=(min_d, max_d))

        df_f = df[
            (df["brand"].isin(selected_brands)) &
            (df["date_only"] >= dr[0]) &
            (df["date_only"] <= dr[1])
        ]

        # 3) Five grouped‐bar charts
        metrics = [
            ("🌱 Labor Score",     "labor_score",
             "This chart shows each brand's labor policy score at every selected reporting date."),
            ("🔍 Sourcing Score",  "sourcing_score",
             "This chart shows how brands compare in sourcing transparency over time."),
            ("⚡ Carbon Score",    "carbon_score",
             "This chart tracks brands' carbon footprint scores across your chosen period."),
            ("🐾 Animal Score",    "animal_score",
             "This chart illustrates brands' animal-welfare performance over time."),
            ("🏛️ Governance Score","governance_score",
             "This chart highlights corporate-governance scores for each brand across dates.")
        ]

        for label, col, desc in metrics:
            st.markdown(f"### {label} by Brand Over Time")
            st.caption(desc)
            fig = px.bar(
                df_f,
                x="date_only",
                y=col,
                color="brand",
                barmode="group"
            )
            fig.update_layout(xaxis_title="Date", yaxis_title="Score")
            st.plotly_chart(fig, use_container_width=True)

        # 4) Correlation Matrix
        st.markdown("---")
        st.subheader("🔗 Correlation Between Ethical Metrics")
        st.caption(
            "Shows the pairwise Pearson correlation between labor, sourcing, carbon, "
            "animal and governance scores across your selected brands and dates."
        )
        cols = ["labor_score","sourcing_score","carbon_score","animal_score","governance_score"]
        corr = df_f[cols].corr()
        fig_corr = px.imshow(
            corr,
            text_auto=True,
            aspect="auto",
            color_continuous_scale="RdBu",
            origin="lower",
            title="Correlation Between Ethical Metrics"
        )
        fig_corr.update_layout(xaxis_title="Metric", yaxis_title="Metric")
        st.plotly_chart(fig_corr, use_container_width=True)

        # 4) Correlation Matrix
        st.markdown("---")
        st.subheader("🔗 Correlation Between Ethical Metrics")
        st.caption(
            "Shows the pairwise Pearson correlation between labor, sourcing, carbon, "
            "animal and governance scores across your selected brands and dates."
        )

        # Compute correlations on the filtered dataframe (df_f)
        metrics_cols = [
            "labor_score",
            "sourcing_score",
            "carbon_score",
            "animal_score",
            "governance_score",
        ]
        corr = df_f[metrics_cols].corr()

        # Render as a heatmap
        fig_corr = px.imshow(
            corr,
            text_auto=True,
            aspect="auto",
            color_continuous_scale="RdBu",
            origin="lower",
            title="Correlation Between Ethical Metrics"
        )
        fig_corr.update_layout(
            xaxis_title="Metric",
            yaxis_title="Metric",
            margin=dict(t=50, l=50, r=50, b=50)
        )
        st.plotly_chart(fig_corr, use_container_width=True)

    # 5) Ethics vs. Financial Performance Scatter
    st.markdown("---")
    st.subheader("📈 Ethics Index vs. Revenue (M USD)")
    st.caption(
        "Each point is a brand’s average ethical index (avg of five scores) vs its revenue "
        "for 2024, with a trendline to show overall correlation."
    )

    # Button to fetch scatter data
    if st.button("Generate Ethics x Finance Scatter"):
        with st.spinner("Loading data…"):
            resp = asyncio.run(get_ethics_finance())
            raw = resp.content.strip().removeprefix("```json").removesuffix("```")
            df_sc = pd.DataFrame(json.loads(raw))
            print(df_sc)
            # cache for this session
            st.session_state.df_scatter = df_sc

    # Render if available
    if "df_scatter" in st.session_state:
        df_sc = st.session_state.df_scatter
        fig_sc = px.scatter(
            df_sc,
            x="ethics_index",
            y="revenue_musd",
            color="brand",
            hover_name="brand",
            title="Ethics Index vs. Revenue (M USD)",
            labels={
                "ethics_index": "Ethics Index (avg score)",
                "revenue_musd": "Revenue (M USD)"
            },
            trendline="ols"
        )
        fig_sc.update_layout(margin=dict(t=40, b=20, l=20, r=20))
        st.plotly_chart(fig_sc, use_container_width=True)

    # 6) Sector & Region Breakdown
    st.markdown("---")
    st.subheader("⚖️ Average Metric by Sector & Region")
    st.caption(
        "Compare average scores by industry sector and headquarters region. "
        "Pick a metric below and then generate the breakdown."
    )
    metric_map = {
        "Labor":    "avg_labor",
        "Sourcing": "avg_sourcing",
        "Carbon":   "avg_carbon",
        "Animal":   "avg_animal",
        "Governance":"avg_governance",
    }
    choice = st.selectbox("Choose metric", list(metric_map.keys()))
    col = metric_map[choice]
    if st.button("Generate Sector & Region Breakdown"):
        with st.spinner("Fetching sector & region data…"):
            resp = asyncio.run(get_sector_region_breakdown())
            raw = resp.content.strip().removeprefix("```json").removesuffix("```")
            df_sr = pd.DataFrame(json.loads(raw))
            st.session_state.df_sr = df_sr

    if "df_sr" in st.session_state:
        df_sr = st.session_state.df_sr

        # Bar chart by sector
        st.markdown(f"### Average {choice} Score by Sector")
        fig_sec = px.bar(
            df_sr,
            x="sector",
            y=col,
            color="sector",
            title=f"{choice} by Sector",
        )
        fig_sec.update_layout(xaxis_title="Sector", yaxis_title=f"Avg {choice}")
        st.plotly_chart(fig_sec, use_container_width=True)

        # Bar chart by region
        st.markdown(f"### Average {choice} Score by Region")
        df_reg = (
            df_sr.groupby("region")[col]
                .mean()
                .reset_index()
                .sort_values(col, ascending=False)
        )
        fig_reg = px.bar(
            df_reg,
            x="region",
            y=col,
            color="region",
            title=f"{choice} by Region",
        )
        fig_reg.update_layout(xaxis_title="Region", yaxis_title=f"Avg {choice}")
        st.plotly_chart(fig_reg, use_container_width=True)

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
