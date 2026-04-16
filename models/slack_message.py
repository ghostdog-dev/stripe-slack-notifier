from pydantic import BaseModel

# Slack field model
class SlackField(BaseModel):
    title: str
    value: str
    short: bool = True

# Slack attachment model
class SlackAttachment(BaseModel):
    color: str
    title: str
    text: str = ""
    fields: list[SlackField] | None = None
    mrkdwn_in: list[str] | None = None
    footer: str | None = None
    ts: int | None = None

# Slack message model
class SlackMessage(BaseModel):
    text: str
    attachments: list[SlackAttachment]
