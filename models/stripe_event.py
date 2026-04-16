from pydantic import BaseModel, ConfigDict

# Stripe event data model
class StripeEventData(BaseModel):
    object: dict
    model_config = ConfigDict(extra="allow")

# Stripe event model
class StripeEvent(BaseModel):
    id: str
    type: str
    data: StripeEventData
    model_config = ConfigDict(extra="allow")
