import asyncio

import httpx

from config import SLACK_HTTP_TIMEOUT, SLACK_MAX_RETRIES, SLACK_RETRY_BACKOFF
from services.slack.exceptions import SlackDeliveryError
from utils.logger import get_logger

logger = get_logger(__name__)


# Détermine si le code HTTP justifie un retry (429 ou 5xx)
def _should_retry(status_code: int) -> bool:
    return status_code == 429 or 500 <= status_code < 600


# Extrait le délai Retry-After du header Slack, ou utilise le fallback
def _parse_retry_after(response: httpx.Response, fallback: float) -> float:
    raw = response.headers.get("Retry-After")
    if raw is None:
        return fallback
    try:
        return max(float(raw), fallback)
    except ValueError:
        return fallback


# Envoie le payload à l'URL Slack, avec retry exponentiel en cas d'échec transitoire
async def post_to_slack(url: str, payload: dict) -> None:
    last_error: str = "unknown"

    async with httpx.AsyncClient(timeout=SLACK_HTTP_TIMEOUT) as client:
        for attempt in range(1, SLACK_MAX_RETRIES + 1):
            # Backoff exponentiel : 1s, 2s, 4s, ...
            backoff = SLACK_RETRY_BACKOFF * (2 ** (attempt - 1))
            try:
                response = await client.post(url, json=payload)
            except httpx.TimeoutException as e:
                last_error = f"timeout: {e}"
                logger.warning("Slack timeout (tentative %d/%d)", attempt, SLACK_MAX_RETRIES)
            except httpx.RequestError as e:
                last_error = f"request_error: {e}"
                logger.warning("Slack request error (tentative %d/%d): %s", attempt, SLACK_MAX_RETRIES, e)
            else:
                if response.status_code == 200:
                    return
                if not _should_retry(response.status_code):
                    # Erreur définitive (4xx hors 429) : inutile d'insister
                    raise SlackDeliveryError(
                        f"slack_http_{response.status_code}: {response.text}"
                    )
                # Statut retryable (429 ou 5xx)
                last_error = f"http_{response.status_code}: {response.text}"
                logger.warning(
                    "Slack status %d (tentative %d/%d)",
                    response.status_code, attempt, SLACK_MAX_RETRIES,
                )
                if response.status_code == 429:
                    backoff = _parse_retry_after(response, backoff)

            # On ne dort pas après la dernière tentative
            if attempt < SLACK_MAX_RETRIES:
                await asyncio.sleep(backoff)

    raise SlackDeliveryError(f"slack_delivery_failed: {last_error}")
