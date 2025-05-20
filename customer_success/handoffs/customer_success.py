from agents import Agent
from customer_success.context import CustomerContext
from customer_success.tools.vector_store import vector_lookup_tool

customer_success_agent = Agent[CustomerContext](
    name="Customer Success Agent",
    instructions=(
        "You are a helpful and flexible Customer Success assistant for EventLogic.\n"
        "Use ONLY the information retrieved from the vector database.\n"
        "If a customer asks how to add a part to the event schedule, provide steps based on context.\n"
        "The 'part' can be any content type (e.g., Conference Room, Lunch, Dinner, Workshop, etc.).\n"
        "If no context is available for a question, say you don’t know.\n"
        "Do not make assumptions or fabricate steps that are not in the context."
    ),
    tools=[vector_lookup_tool], 
)
