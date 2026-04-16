# Levée quand l'envoi à Slack échoue définitivement après retries
class SlackDeliveryError(Exception):
    pass
