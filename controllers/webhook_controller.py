from fastapi import BackgroundTasks, Request

from services.slack import notify
from services.stripe import classify_event, parse_event, verify_stripe_signature_webhook
from utils.logger import get_logger

logger = get_logger(__name__)

# Process event and notify Slack
async def process_event(raw_event: dict) -> None:
    event = parse_event(raw_event)
    if event is None:
        return

    classified = classify_event(event)
    if classified is None:
        return

    await notify(
        event_type=event.type,
        category=classified["category"],
        severity=classified["severity"],
        payload=classified["payload"],
    )

# Handle stripe webhook and process event in background
async def handle_stripe_webhook(request: Request, background_tasks: BackgroundTasks) -> dict:
    result = await verify_stripe_signature_webhook(request)
    if not result["success"]:
        logger.warning("Webhook Stripe rejeté : %s", result.get("reason"))
        return {"status": "error", "message": "Invalid signature"}

    background_tasks.add_task(process_event, result["event"])
    return {"status": "ok"}
