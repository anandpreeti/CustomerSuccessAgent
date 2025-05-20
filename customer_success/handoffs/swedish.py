
from agents import Agent
from customer_success.context import CustomerContext

swedish_agent = Agent[CustomerContext](
    name="Swedish Agent",
    instructions="You provide assistance with English queries. Engage  the customer in English converstation.",
)

