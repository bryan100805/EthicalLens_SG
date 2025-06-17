# MCP SQL Chatbot & Dashboard

This project demonstrates how to build an interactive SQL chatbot and a dynamic dashboard using natural language processing (NLP) and the Modular Control Protocol (MCP). It allows users to query an SQL database using natural language and visualize the data in a web-based dashboard.

## Features

*   **Natural Language SQL Queries:** Interact with an SQL database using natural language. The chatbot understands your questions and translates them into SQL queries.
*   **Dynamic Dashboard Generation:** Generate interactive HTML dashboards based on the database schema and data.
*   **Database Schema Analysis:** The system analyzes the database schema to identify the domain, key metrics, and appropriate visualizations.
*   **MCP Integration:** Leverages the Modular Control Protocol (MCP) for secure and efficient database interaction.
*   **Interactive Charts:** Uses Chart.js to create interactive charts in the dashboard.
*   **Responsive Design:** The generated dashboards are responsive and mobile-friendly, thanks to Tailwind CSS.
*   **UV Package Manager:** Uses UV package manager for dependency management.

## Project Structure

*   **`app.py`:** The main Streamlit application that provides the user interface for the chatbot and dashboard.
*   **`agent.py`:** Contains the code for the natural language SQL query/graph agent.
*   **`dashboard_agent.py`:** Contains the code for the dashboard generation agent.

## Prerequisites

*   **UV:** This project uses the UV package manager. Install it by following the instructions on the UV website: https://astral.sh/uv. i.e.pip install uv
*   **Python 3.9+:** Ensure you have Python 3.9 or a later version installed.
*   **MCP SQL Server:** You need an MCP SQL server running. You can set it up using the `uvx` command. 
*   **Database:** An SQL database (e.g., MySQL) with some data.
*   **Environment Variables:** Set the following environment variables in a `.env` file in the project root:
    *   `GROQ_API_KEY`: Your Groq API key.
    *   `DB_HOST`: The hostname or IP address of your database server.
    *   `DB_USER`: The username for your database.
    *   `DB_PASSWORD`: The password for your database.
    *   `DB_NAME`: The name of your database.
    * `MODEL_ID`: The model id to use. (optional)

## Setup and Installation (using UV)

1.  **Change directory:**

    ```bash
    cd mcp-agent-experiment
    ```

2.  **Install Dependencies with UV:**

    ```bash
    uv sync
    ```
    This command will:
    * Create a virtual environment if one does not exist.
    * Install all the dependencies listed in the `pyproject.toml` file.

3.  **Create `.env` File:**

    Create a `.env` file in the project root and add your environment variables:

    ```
    
    DB_HOST=your_db_host
    DB_USER=your_db_user
    DB_PASSWORD=your_db_password
    DB_NAME=your_db_name
    MODEL_API_KEY = API for OpenAI or GROQ
    MODEL_ID = The ID of the language model to use like gemini-2.0-flash, llama-3.3-70b-versatile, gpt-4o
    ```
    *Note :- Gives better results with OpenAI models


## Running the Application

1.  **Activate the Virtual Environment:**
    UV will create a `.venv` folder in your project.
    ```bash
    source .venv/Scripts/activate  # On Linux/macOS
    .venv\Scripts\activate  # On Windows
    ```

2. **Run the MCP server**
   Run this command to connect to the MCP server
   ```bash
   uvx mcp-sql-server --db-host localhost --db-database ethical_scores --db-user root --db-password your_password
   ```

   Run this command to run the proxy server to inspect the tools and other connection details
   ```bash
   npx @modelcontextprotocol/inspector uvx mcp-sql-server --db-host localhost --db-database ethical_scores --db-user root --db-password your_password
   ```

3. **Add in LLM API token in the corresponding files**
   This application is using gemini-flash-2.0.

4.  **Run the Streamlit App:**

    ```bash
    streamlit run app.py
    ```

5.  **Access the App:**

    Open your web browser and go to the URL provided in the terminal (usually `http://localhost:8501`).

## Usage

### Chatbot Tab

1.  **Ask Questions:** In the "Chatbot" tab, type your questions about the database in natural language (e.g., "Compare the brand with the highest carbon score and the lowest carbon score.").
2.  **View Results:** The chatbot will respond with a natural language summary of the data or a chart when it is suitable.

### Dashboard Tab

- Work in progress

## Key Components

*   **`agent.py`:**
    *   Defines the `db_connection_agent` which is responsible for understanding user queries and generating SQL.
    *   Uses the `get_schema` and `read_query` tools from the MCP toolkit.
    *   Returns a natural language summary of the query results.
*   **`dashboard_agent.py`:**
    - Work in progress
*   **`app.py`:**
    *   The main Streamlit application.
    *   Provides the user interface for the chatbot and dashboard.
    *   Uses `st.session_state` to persist chat messages.
    *   Uses `st.container` and JavaScript to keep the chat at the top of the screen.
    *   Uses `st.tabs` to create the "Chatbot" and "other tabs.

## Contributing

- [bryan100805](https://github.com/bryan100805)
- [Kennetan2](https://github.com/Kennetan2)

## License

MIT
