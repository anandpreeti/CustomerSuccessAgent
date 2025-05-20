
# customer_success/main.py
import asyncio
import uuid
from agents import Runner, ItemHelpers, MessageOutputItem, HandoffOutputItem, ToolCallItem, ToolCallOutputItem, TResponseInputItem, trace
from customer_success.agents.language_detector import language_detector_agent
from customer_success.agents.traige import triage_agent
from customer_success.context import CustomerContext

async def main():
    current_agent = triage_agent
    context = CustomerContext()
    input_items: list[TResponseInputItem] = []
    conversation_id = uuid.uuid4().hex[:16]

    while True:
        user_input = input("You: ")
        with trace("Customer Support Session", group_id=conversation_id):
            input_items.append({"content": user_input, "role": "user"})
            result = await Runner.run(current_agent, input_items, context=context)

            for new_item in result.new_items:
                name = new_item.agent.name
                if isinstance(new_item, MessageOutputItem):
                    print(f"{name}: {ItemHelpers.text_message_output(new_item)}")
                elif isinstance(new_item, HandoffOutputItem):
                    print(f"Handoff: {new_item.source_agent.name} ➔ {new_item.target_agent.name}")
                elif isinstance(new_item, ToolCallItem):
                    print(f"{name}: Calling tool...")
                elif isinstance(new_item, ToolCallOutputItem):
                    print(f"{name}: Tool result: {new_item.output}")
                else:
                    print(f"{name}: Skipping item: {new_item.__class__.__name__}")

            input_items = result.to_input_list()
            current_agent = result.last_agent

if __name__ == "__main__":
    asyncio.run(main())

