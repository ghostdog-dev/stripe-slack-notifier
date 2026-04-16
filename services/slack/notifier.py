from config import SLACK_WEBHOOK_URL
from services.slack.client import post_to_slack
from services.slack.exceptions import SlackDeliveryError
from services.slack.formatter import build_message
from utils.logger import get_logger

logger = get_logger(__name__)


# Envoie une notification Slack et renvoie True/False sans propager les erreurs
async def notify(event_type: str, category: str, severity: str, payload: dict) -> bool:
    if not SLACK_WEBHOOK_URL:
        logger.error("SLACK_WEBHOOK_URL non configurée, message ignoré pour %s", event_type)
        return False

    message = build_message(event_type, category, severity, payload)
    body = message.model_dump(exclude_none=True)

    try:
        await post_to_slack(SLACK_WEBHOOK_URL, body)
    except SlackDeliveryError as e:
        logger.error("Envoi Slack échoué (%s | %s) : %s", category, event_type, e)
        return False

    logger.info("Notification Slack envoyée (%s | %s)", category, event_type)
    return True
