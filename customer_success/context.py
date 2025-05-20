from pydantic import BaseModel

EVENT_CREATION_STEPS = """
1. User is redirected to the onboarding landing page.
2. User is prompted to choose event category. This is mandatory.
3. User is prompted to choose event sub category. This is mandatory.
4. User is prompted to choose event date. This is mandatory.
5. User is prompted to choose event participants number. This is mandatory.
6. User is prompted to choose event location. This is mandatory.
7. User is prompted to choose event name. This is mandatory.
8. If there is error on any step, user is redirected to the onboarding landing page. User must start the process all over again. The event will be lost.
9. If there is no error, user is redirected to the event summary page.
"""

class CustomerContext(BaseModel):
    customer_id: str | None = None
    subscription_plan: str | None = None
    issue_type: str | None = None

    # New field: embeds the constant event description/steps
    event_creation_steps: str = EVENT_CREATION_STEPS
