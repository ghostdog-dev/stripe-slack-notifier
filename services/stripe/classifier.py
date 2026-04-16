from models.stripe_event import StripeEvent
from utils.logger import get_logger
from utils.stripe_event_catalog import EVENT_CATALOG

logger = get_logger(__name__)

_MISSING = object()


# Récupère une valeur imbriquée via un chemin pointé (ex: "a.b.c")
def _get_nested(data: dict, path: str, default=None):
    current = data
    for key in path.split("."):
        if not isinstance(current, dict):
            return default
        current = current.get(key, _MISSING)
        if current is _MISSING:
            return default
    return current


# Réduit le payload Stripe aux seuls champs définis dans le catalogue
def _extract_key_fields(obj: dict, key_fields: tuple[str, ...]) -> dict:
    return {field: _get_nested(obj, field) for field in key_fields}


# Classifie un événement Stripe selon le catalogue et renvoie {category, severity, payload}
def classify_event(event: StripeEvent) -> dict | None:
    spec = EVENT_CATALOG.get(event.type)
    if spec is None:
        logger.warning("Type d'événement inconnu : %s", event.type)
        return None

    key_fields = spec.get("key_fields", ())
    if not isinstance(key_fields, tuple):
        key_fields = tuple(key_fields)

    payload = _extract_key_fields(event.data.object, key_fields)
    return {
        "category": spec.get("category", "unknown"),
        "severity": str(spec.get("severity", "info")),
        "payload": payload,
    }
