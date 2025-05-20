# customer_success/agents/triage.py
from agents import Agent, handoff
from customer_success.context import CustomerContext
from customer_success.handoffs.finance import finance_agent
from customer_success.handoffs.marketing import marketing_agent
from customer_success.handoffs.sales import sales_agent
from customer_success.handoffs.development import development_agent
from customer_success.handoffs.external import external_services_agent
from customer_success.handoffs.apidoc import apidoc_agent
from customer_success.handoffs.feedback import feedback_agent
from customer_success.handoffs.customer_success import customer_success_agent

triage_agent = Agent[CustomerContext](
    name="Triage Agent",
    handoff_description="Routes to the correct support agent.",
    instructions="""
    Decide whether the issue is a Finace or sales or marketing related.
    If someone is trying to give feedback, handoff to feedback_agent. And, if 
    the issue is not related to any of these, hand off to the customer success agent.

    """,
    handoffs=[
        finance_agent,
        marketing_agent,
        sales_agent,
        development_agent,
    
        apidoc_agent,
        feedback_agent,
        customer_success_agent]
)

# faq_agent.handoffs.append(human_agent)
# subscription_agent.handoffs.append(human_agent)