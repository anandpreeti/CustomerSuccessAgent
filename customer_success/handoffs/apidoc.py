from agents import Agent, WebSearchTool, function_tool
from customer_success.context import CustomerContext


import requests


@function_tool
def fetch_eventlogic_docs(query: str) -> str:
    """
    Fetches documentation content from EventLogic's public API docs.
    """
    import requests

    url = "https://admin-qat.eventlogic.se/assets/docs/index.html"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            return f"Failed to fetch documentation. Status: {response.status_code}"
    except Exception as e:
        return f"Error fetching docs: {str(e)}"


# eventlogic_docs_tool = ToolSpec(
#     name="eventlogic_docs",
#     description="Fetches documentation content from EventLogic's public API docs.",
#     func=fetch_eventlogic_docs
# )

apidoc_agent = Agent[CustomerContext](
    name="APIDOC Agent",
    instructions="Use the fetch_eventlogic_docs tool to look up API documentation details.",
    tools=[fetch_eventlogic_docs],  # function directly used
)