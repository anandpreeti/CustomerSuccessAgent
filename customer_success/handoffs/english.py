from agents import Agent
from customer_success.context import CustomerContext

english_agent = Agent[CustomerContext](
    name="English Agent",
    instructions="You provide assistance with English queries. Engage  the customer in English converstation.",
)

