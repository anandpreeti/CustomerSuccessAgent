# import streamlit as st
# import asyncio
# import uuid
# from agents import Runner, ItemHelpers, MessageOutputItem, HandoffOutputItem, ToolCallItem, ToolCallOutputItem, TResponseInputItem
# from customer_success.agents.language_detector import language_detector_agent
# from customer_success.agents.traige import triage_agent
# from customer_success.context import CustomerContext

# st.set_page_config(page_title="Customer Success Chat", page_icon="💬")

# # Initialize session state
# if "chat_history" not in st.session_state:
#     st.session_state.chat_history = []
# if "input_items" not in st.session_state:
#     st.session_state.input_items = []
# if "current_agent" not in st.session_state:
#     st.session_state.current_agent = triage_agent
# if "conversation_id" not in st.session_state:
#     st.session_state.conversation_id = uuid.uuid4().hex[:16]
# if "context" not in st.session_state:
#     st.session_state.context = CustomerContext()

# st.title("💬 Customer Success Chatbot")

# # Display past chat
# for entry in st.session_state.chat_history:
#     with st.chat_message(entry["role"]):
#         st.markdown(entry["message"])

# # Get user input
# user_input = st.chat_input("Type your message...")
# if user_input:
#     # Display user message
#     st.chat_message("user").markdown(user_input)
#     st.session_state.chat_history.append({"role": "user", "message": user_input})

#     # Append input item
#     st.session_state.input_items.append({"content": user_input, "role": "user"})

#     # Run agent logic
#     async def run_agent():
#         result = await Runner.run(
#             st.session_state.current_agent,
#             st.session_state.input_items,
#             context=st.session_state.context
#         )

#         for new_item in result.new_items:
#             name = new_item.agent.name
#             if isinstance(new_item, MessageOutputItem):
#                 output = ItemHelpers.text_message_output(new_item)
#                 st.chat_message("assistant").markdown(output)
#                 st.session_state.chat_history.append({"role": "assistant", "message": output})
#             elif isinstance(new_item, HandoffOutputItem):
#                 handoff_text = f"Handoff: {new_item.source_agent.name} ➔ {new_item.target_agent.name}"
#                 st.chat_message("assistant").markdown(handoff_text)
#                 st.session_state.chat_history.append({"role": "assistant", "message": handoff_text})
#             elif isinstance(new_item, ToolCallItem):
#                 tool_call_text = f"{name}: Calling tool..."
#                 st.chat_message("assistant").markdown(tool_call_text)
#                 st.session_state.chat_history.append({"role": "assistant", "message": tool_call_text})
#             elif isinstance(new_item, ToolCallOutputItem):
#                 tool_output = f"{name}: Tool result: {new_item.output}"
#                 st.chat_message("assistant").markdown(tool_output)
#                 st.session_state.chat_history.append({"role": "assistant", "message": tool_output})
#             else:
#                 skip_text = f"{name}: Skipping item: {new_item.__class__.__name__}"
#                 st.chat_message("assistant").markdown(skip_text)
#                 st.session_state.chat_history.append({"role": "assistant", "message": skip_text})

#         # Update session state
#         st.session_state.input_items = result.to_input_list()
#         st.session_state.current_agent = result.last_agent

#     asyncio.run(run_agent())

import streamlit as st
import asyncio
import uuid
from agents import Runner, ItemHelpers, MessageOutputItem, HandoffOutputItem, ToolCallItem, ToolCallOutputItem, TResponseInputItem
from customer_success.agents.language_detector import language_detector_agent
from customer_success.agents.traige import triage_agent
from customer_success.context import CustomerContext
from customer_success.tools.vector_store import load_vector_store, init_vector_store, vector_store_exists
from customer_success.tools.data_loader import get_zendesk_article_text 

# Example article list
article_ids = ["4410160179345"]

if "vector_store" not in st.session_state:
    if vector_store_exists():
        st.session_state.vector_store = load_vector_store()
    else:
        article_texts = []
        for article_id in article_ids:
            try:
                article_texts.append(get_zendesk_article_text(article_id))
            except Exception as e:
                st.warning(f"Failed to fetch article {article_id}: {e}")
        st.session_state.vector_store = init_vector_store(article_texts)

st.set_page_config(page_title="Customer Success Chat", page_icon="💬")

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "input_items" not in st.session_state:
    st.session_state.input_items = []
if "current_agent" not in st.session_state:
    st.session_state.current_agent = triage_agent
if "conversation_id" not in st.session_state:
    st.session_state.conversation_id = uuid.uuid4().hex[:16]
if "context" not in st.session_state:
    st.session_state.context = CustomerContext()

st.title("💬 Customer Success Chatbot")

# Display past chat
for entry in st.session_state.chat_history:
    with st.chat_message(entry["role"]):
        st.markdown(entry["message"])

# Get user input
user_input = st.chat_input("Type your message...")
if user_input:
    # Display user message
    st.chat_message("user").markdown(user_input)
    st.session_state.chat_history.append({"role": "user", "message": user_input})

    # Append input item
    st.session_state.input_items.append({"content": user_input, "role": "user"})

    # Run agent logic
    async def run_agent():
        result = await Runner.run(
            st.session_state.current_agent,
            st.session_state.input_items,
            context=st.session_state.context
        )

        for new_item in result.new_items:
            name = new_item.agent.name
            if isinstance(new_item, MessageOutputItem):
                output = ItemHelpers.text_message_output(new_item)
                st.chat_message("assistant").markdown(output)
                st.session_state.chat_history.append({"role": "assistant", "message": output})
            elif isinstance(new_item, HandoffOutputItem):
                handoff_text = f"Handoff: {new_item.source_agent.name} ➔ {new_item.target_agent.name}"
                st.chat_message("assistant").markdown(handoff_text)
                st.session_state.chat_history.append({"role": "assistant", "message": handoff_text})
            elif isinstance(new_item, ToolCallItem):
                tool_call_text = f"{name}: Calling tool..."
                st.chat_message("assistant").markdown(tool_call_text)
                st.session_state.chat_history.append({"role": "assistant", "message": tool_call_text})
            elif isinstance(new_item, ToolCallOutputItem):
                tool_output = f"{name}: Tool result: {new_item.output}"
                st.chat_message("assistant").markdown(tool_output)
                st.session_state.chat_history.append({"role": "assistant", "message": tool_output})
            else:
                skip_text = f"{name}: Skipping item: {new_item.__class__.__name__}"
                st.chat_message("assistant").markdown(skip_text)
                st.session_state.chat_history.append({"role": "assistant", "message": skip_text})

        # Update session state
        st.session_state.input_items = result.to_input_list()
        st.session_state.current_agent = result.last_agent

    asyncio.run(run_agent())
