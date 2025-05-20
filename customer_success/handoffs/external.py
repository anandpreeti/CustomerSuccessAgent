from agents import Agent, WebSearchTool
from customer_success.context import CustomerContext

external_services_agent = Agent[CustomerContext](
    name="External Services Agent",
    instructions="You are a helpful customer success agent. Use the websearch tool to find real-time information when internal knowledge is not enough",
    tools=[
        WebSearchTool()]
)

