# from agents import Agent, function_tool
# from customer_success.context import CustomerContext

# @function_tool
# def fetch_eventlogic_docs(query: str) -> str:
#     """
#     Fetches documentation content from EventLogic's public API docs.
#     """
#     import requests

#     url = "https://admin-qat.eventlogic.se/api/v1/event/feedback/"
#     try:
#         response = requests.post(url)
#         if response.status_code == 200:
#             return response.text
#         else:
#             return f"Failed to fetch documentation. Status: {response.status_code}"
#     except Exception as e:
#         return f"Error fetching docs: {str(e)}"

# feedback_agent = Agent[CustomerContext](
#     name="Feedback Agent",
#     instructions=
#     '''If someone wants to give feedback about our platform, you ask necessary info like feedback message and then you ask for the email address of the person giving feedback and call feedback tool. Decide on your own
#     if feedback is good or bad. Don't ask the user if it's good or bad feedback. After that,
#     If the feedback is good, you ask for the name of the person giving feedback and then you say thank you to the person for giving feedback.
#     If the feedback is bad, you ask for the name of the person giving feedback and then you say sorry to the person for giving bad feedback.
#     If the feedback is neutral, you ask for the name of the person giving feedback and then you say thank you to the person for giving feedback.
#     If the feedback is not related to our platform, you say sorry to the person for giving feedback.
#     If the feedback is not related to our platform, you say sorry to the person for giving feedback.
#     . Use the websearch tool to find real-time information when internal knowledge is not enough''',
#     tools=[
#         WebSearchTool()]
# )

from agents import Agent, function_tool
from customer_success.context import CustomerContext
import requests

@function_tool
def send_feedback(feedbacktype: str, feedback: str, email: str) -> str:
    """
    Sends user feedback to EventLogic's feedback endpoint.
    """
    url = "https://admin-qat.eventlogic.se/api/v1/event/feedback/"
    payload = {
        "type": feedbacktype,
        "comment": feedback,
        "email": email,
        "contactMe": True
    }
    print('payload', payload);
    try:
        response = requests.post(url, json=payload)
        print(f"Response: {response}")
        if response.status_code == 200:
            return "Feedback successfully submitted!"
        else:
            return f"Failed to submit feedback. Status: {response.status_code}, Response: {response.text}"
    except Exception as e:
        return f"Error submitting feedback: {str(e)}"

feedback_agent = Agent[CustomerContext](
    name="Feedback Agent",
    instructions="""
If a user wants to give feedback about our platform:
1. Decide on your own whether the feedback is good, bad, or neutral. 
2.If feedback is good map 'good' to 'common.onboarding.like.something'.
3.If feedback is bad map 'bad' to 'common.onboarding.dont.like.something'.
4. If feedback is suggestion map 'suggestion' to 'common.onboarding.have.a.suggestion'.
5. Ask for the feedback content.
5. Ask for the email address of the person giving the feedback. If user already provided email in conversation, confirm with user if that's the email they want to use. Make sure 
user has provided the email address before confirming.
6. Call the `send_feedback` tool with these details.


After that:
- If the feedback is good, ask for the person's name and say thank you.
- If the feedback is bad, ask for the person's name and say sorry.
- If the feedback is neutral, ask for the person's name and say thank you.
- If the feedback is not related to our platform, politely say sorry and inform them that the feedback can't be processed.

Use the websearch tool to find real-time information when internal knowledge is not enough.
""",
    tools=[send_feedback]
)
