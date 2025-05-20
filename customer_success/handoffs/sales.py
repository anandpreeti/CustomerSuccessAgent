from agents import Agent
from customer_success.context import CustomerContext

sales_agent = Agent[CustomerContext](
    name="Sales Agent",
    instructions="You provide assistance with EventLogic Sales related queries. Explain  clearly.",
)

