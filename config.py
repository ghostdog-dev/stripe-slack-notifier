from dotenv import load_dotenv
import os

load_dotenv()

# Stripe
STRIPE_API_KEY = os.getenv("STRIPE_API_KEY")
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET")

# Slack — URL unique d'Incoming Webhook (tout est trié côté back)
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")

# Paramètres réseau pour l'envoi vers Slack
SLACK_HTTP_TIMEOUT = float(os.getenv("SLACK_HTTP_TIMEOUT", "5.0"))
SLACK_MAX_RETRIES = int(os.getenv("SLACK_MAX_RETRIES", "3"))
SLACK_RETRY_BACKOFF = float(os.getenv("SLACK_RETRY_BACKOFF", "1.0"))

# Niveau de log (DEBUG, INFO, WARNING, ERROR)
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
