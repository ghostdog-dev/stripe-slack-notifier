import stripe
from fastapi import Request

from config import STRIPE_API_KEY, STRIPE_WEBHOOK_SECRET
from utils.logger import get_logger

logger = get_logger(__name__)

if not STRIPE_WEBHOOK_SECRET:
    raise RuntimeError(
        "STRIPE_WEBHOOK_SECRET manquant : impossible de vérifier les webhooks Stripe."
    )

_client = stripe.StripeClient(STRIPE_API_KEY)
_endpoint_secret = STRIPE_WEBHOOK_SECRET


# Vérifie la signature Stripe et renvoie un dict {success, event|reason}
async def verify_signature(request: Request) -> dict:
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")

    if not sig_header:
        return {"success": False, "reason": "missing_signature_header"}

    try:
        event_obj = _client.construct_event(payload, sig_header, _endpoint_secret)
    except ValueError as e:
        return {"success": False, "reason": f"invalid_payload: {e}"}
    except stripe.SignatureVerificationError as e:
        return {"success": False, "reason": f"invalid_signature: {e}"}

    return {"success": True, "event": event_obj.to_dict()}
