# Guide d'intégration

Comment intégrer ce notifier dans un projet existant ou un flux de production.

## Cas 1 : Ajouter à un projet existant qui a déjà un webhook Stripe

Si tu as déjà un endpoint webhook Stripe dans ton app (ex: pour mettre à jour ta base de données), tu as deux options.

### Option A : Endpoint dédié (recommandé)

Ajoute un **deuxième endpoint webhook** dans Stripe qui pointe vers ce notifier.

```
Stripe webhook 1 → ton-app.com/webhook       → logique métier (BDD, etc.)
Stripe webhook 2 → ton-notifier.com/webhook   → notifications Slack
```

**Avantages :**
- Zéro modification de ton app existante
- Si le notifier tombe, ton app n'est pas impactée
- Déploiement indépendant

**Comment faire :**
1. Déploie ce notifier sur un serveur/service séparé
2. Dans le dashboard Stripe → Webhooks → Ajoute un nouvel endpoint
3. URL : `https://ton-notifier.com/webhook`
4. Sélectionne les mêmes événements (ou un sous-ensemble)

### Option B : Intégrer dans ton app (FastAPI)

Si ton app utilise **FastAPI**, c'est plug-and-play. La fonction `handle_stripe_webhook` fait tout le flux en un appel :

```python
# 1. Copie le dossier du notifier dans ton projet (ou ajoute-le au PYTHONPATH)
# 2. Dans ton fichier de routes :

from fastapi import BackgroundTasks, Request
from controllers.webhook_controller import handle_stripe_webhook

@app.post("/webhook")
async def mon_webhook_stripe(request: Request, background_tasks: BackgroundTasks):
    # Ta logique métier existante si besoin...
    # update_database(...)

    # Une seule ligne : vérif signature + parsing + classification + envoi Slack
    return await handle_stripe_webhook(request, background_tasks)
```

C'est tout. La fonction :
1. Vérifie la signature Stripe
2. Renvoie `{"status": "ok"}` immédiatement (Stripe reçoit un 200 rapide)
3. Lance le traitement en tâche de fond (parse → classifie → formate → envoie Slack)

### Option C : Intégrer dans ton app (Flask, Django, autre framework)

Si ton app n'utilise pas FastAPI, la logique reste la même — seule la récupération de la requête change. Utilise directement les fonctions internes :

```python
from services.stripe import verify_stripe_signature_webhook, parse_event, classify_event
from services.slack import notify
```

#### Exemple Flask

```python
import asyncio
from flask import Flask, request, jsonify

from services.stripe.signature import verify_raw_signature
from services.stripe import parse_event, classify_event
from services.slack import notify

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook_stripe():
    payload = request.data
    sig_header = request.headers.get("Stripe-Signature")

    # Étape 1 : vérifier la signature
    result = verify_raw_signature(payload, sig_header)
    if not result["success"]:
        return jsonify({"error": result["reason"]}), 400

    # Étape 2 : traiter et notifier (en synchrone ici, ou via Celery/thread)
    event = parse_event(result["event"])
    if event:
        classified = classify_event(event)
        if classified:
            asyncio.run(notify(
                event_type=event.type,
                category=classified["category"],
                severity=classified["severity"],
                payload=classified["payload"],
            ))

    return jsonify({"status": "ok"}), 200
```

#### Exemple Django

```python
import asyncio
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from services.stripe.signature import verify_raw_signature
from services.stripe import parse_event, classify_event
from services.slack import notify

@csrf_exempt
def webhook_stripe(request):
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")

    result = verify_raw_signature(payload, sig_header)
    if not result["success"]:
        return JsonResponse({"error": result["reason"]}, status=400)

    event = parse_event(result["event"])
    if event:
        classified = classify_event(event)
        if classified:
            asyncio.run(notify(
                event_type=event.type,
                category=classified["category"],
                severity=classified["severity"],
                payload=classified["payload"],
            ))

    return JsonResponse({"status": "ok"})
```

> **Note** : les exemples Flask et Django utilisent `asyncio.run()` car `notify()` est async. Pour de la production, utilise un task queue (Celery, RQ) pour ne pas bloquer la réponse HTTP.

#### La fonction clé : `verify_raw_signature`

C'est la seule fonction qui diffère du mode FastAPI. Elle prend le payload brut (`bytes`) et le header de signature (`str`) directement, sans dépendre de `fastapi.Request` :

```python
from services.stripe.signature import verify_raw_signature

result = verify_raw_signature(payload_bytes, sig_header_string)
# → {"success": True, "event": {...}}   si signature valide
# → {"success": False, "reason": "..."}  si invalide
```

Le reste du flux (`parse_event` → `classify_event` → `notify`) est identique quel que soit le framework.

**Dépendances à ajouter** dans ton `requirements.txt` :
```
httpx
pydantic
stripe
python-dotenv
```

## Cas 2 : Déploiement standalone

Le cas le plus simple : déploie ce projet tel quel comme un micro-service indépendant.

### Docker

```dockerfile
FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```bash
docker build -t stripe-notifier .
docker run -d \
  -e STRIPE_API_KEY=sk_live_... \
  -e STRIPE_WEBHOOK_SECRET=whsec_... \
  -e SLACK_WEBHOOK_URL=https://hooks.slack.com/services/... \
  -p 8000:8000 \
  stripe-notifier
```

### Railway / Render / Fly.io

1. Push le repo sur GitHub
2. Connecte le repo à ton hébergeur
3. Configure les variables d'environnement dans le dashboard
4. Le déploiement est automatique

### VPS avec systemd

```ini
# /etc/systemd/system/stripe-notifier.service
[Unit]
Description=Stripe Webhook to Slack Notifier
After=network.target

[Service]
User=www-data
WorkingDirectory=/opt/stripe-notifier
EnvironmentFile=/opt/stripe-notifier/.env
ExecStart=/opt/stripe-notifier/env/bin/uvicorn main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable stripe-notifier
sudo systemctl start stripe-notifier
```

## Cas 3 : Multi-canaux Slack

Tu veux envoyer les paiements dans `#payments` et les litiges dans `#alerts` ?

Modifie `services/slack/notifier.py` pour router par catégorie :

```python
CHANNEL_URLS = {
    "payment": "https://hooks.slack.com/services/.../payments",
    "risk_fraud": "https://hooks.slack.com/services/.../alerts",
}
DEFAULT_URL = os.getenv("SLACK_WEBHOOK_URL")

async def notify(event_type, category, severity, payload):
    url = CHANNEL_URLS.get(category, DEFAULT_URL)
    if not url:
        return False
    # ... reste identique
```

## Cas 4 : Filtrer les événements

Tu ne veux pas recevoir tous les 231 événements ? Deux approches :

### Côté Stripe (recommandé)

Dans le dashboard Stripe → Webhooks → ton endpoint → sélectionne uniquement les événements qui t'intéressent.

### Côté application

Ajoute un filtre dans `webhook_controller.py` :

```python
EVENTS_TO_NOTIFY = {
    "payment_intent.succeeded",
    "payment_intent.payment_failed",
    "invoice.paid",
    "invoice.payment_failed",
    "charge.dispute.created",
    "customer.subscription.created",
    "customer.subscription.deleted",
}

async def process_event(raw_event: dict) -> None:
    event = parse_event(raw_event)
    if event is None or event.type not in EVENTS_TO_NOTIFY:
        return
    # ... suite identique
```

### Filtrer par sévérité

Pour ne recevoir que les événements importants :

```python
async def process_event(raw_event: dict) -> None:
    event = parse_event(raw_event)
    if event is None:
        return
    classified = classify_event(event)
    if classified is None:
        return
    if classified["severity"] not in ("high", "critical"):
        return
    await notify(...)
```

## Reverse proxy

### Nginx

```nginx
server {
    listen 443 ssl;
    server_name stripe-notifier.ton-domaine.com;

    ssl_certificate /etc/letsencrypt/live/.../fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/.../privkey.pem;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### Caddy

```
stripe-notifier.ton-domaine.com {
    reverse_proxy localhost:8000
}
```

Caddy gère le HTTPS automatiquement.
