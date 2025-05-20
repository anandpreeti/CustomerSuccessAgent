from agents import Agent
from customer_success.context import CustomerContext

marketing_agent = Agent[CustomerContext](
    name="Marketing Agent",
    instructions="You provide assistance with EventLogic Marketing related queries. Explain  clearly.",
)

