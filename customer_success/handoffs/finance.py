from agents import Agent
from customer_success.context import CustomerContext

finance_agent = Agent[CustomerContext](
    name="Finance Agent",
    instructions="You provide assistance with EventLogic Finance related queries. Explain  clearly.",
)

