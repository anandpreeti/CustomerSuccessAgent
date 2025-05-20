from agents import Tool
import requests

class EventLogicDocsTool(Tool):
    name = "eventlogic_docs"
    description = "Fetches documentation content from EventLogic's public API docs"

    def call(self, query: str) -> str:
        url = "https://admin-qat.eventlogic.se/assets/docs/index.html"
        response = requests.get(url)
        if response.status_code == 200:
            return response.text  # or parse & extract based on query
        else:
            return "Failed to fetch documentation."
