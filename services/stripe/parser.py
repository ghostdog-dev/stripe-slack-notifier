from pydantic import ValidationError

from models.stripe_event import StripeEvent
from utils.logger import get_logger

logger = get_logger(__name__)


# Valide la structure d'un événement Stripe et renvoie None si invalide
def parse_event(raw_event: dict) -> StripeEvent | None:
    try:
        return StripeEvent.model_validate(raw_event)
    except ValidationError as e:
        event_id = raw_event.get("id") if isinstance(raw_event, dict) else None
        event_type = raw_event.get("type") if isinstance(raw_event, dict) else None
        logger.error(
            "Événement Stripe invalide (id=%s, type=%s) : %s",
            event_id, event_type, e,
        )
        return None
