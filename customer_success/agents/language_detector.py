# customer_success/agents/triage.py
from agents import Agent, handoff
from customer_success.context import CustomerContext
from customer_success.handoffs.english import english_agent
from customer_success.handoffs.swedish import swedish_agent


language_detector_agent = Agent[CustomerContext](
    name="Language Detector Agent",
    handoff_description="Routes to the correct language supporter agent. ",
    instructions="""
    Be a helpful assistant. If the user speaks Swedish, handoff to the Swedish agent.
    If not, handoff to the english agent.
    """,
    handoffs=[
        english_agent,
        swedish_agent,
    ],
)

# faq_agent.handoffs.append(human_agent)
# subscription_agent.handoffs.append(human_agent)