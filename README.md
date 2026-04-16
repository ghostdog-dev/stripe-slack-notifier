# Stripe Webhook to Slack Notifier

Serveur FastAPI qui reçoit les webhooks Stripe, vérifie leur signature, et envoie des notifications formatées en temps réel dans Slack.

## Pourquoi ce projet ?

L'app officielle Stripe pour Slack est limitée : notifications basiques, pas de personnalisation, pas de contrôle sur le format ni le filtrage. Ce projet offre un **contrôle total** sur les événements Stripe que tu reçois et la manière dont ils sont présentés.

### Ce que ça fait

- Reçoit et vérifie les webhooks Stripe (signature HMAC-SHA256)
- Classe **231 types d'événements** par catégorie et sévérité
- Formate des messages Slack lisibles : emojis, montants en devise, libellés FR, couleurs par sévérité
- Envoie vers Slack avec retry automatique et backoff exponentiel
- Traitement non-bloquant en arrière-plan (Stripe reçoit un `200 OK` immédiat)

### Exemple de notification

```
✅  Paiement réussi                    (barre verte)

Montant          Client
15,00 €          cus_ULIudEfj…

─────────────────────────────
Paiement · pi_3TMcIe… · 16/04/2026 01:05
```

## Démarrage rapide

### Prérequis

- Python 3.11+
- Un compte Stripe avec un webhook configuré
- Un workspace Slack avec un Incoming Webhook

### Installation

```bash
git clone <repo-url> && cd webhook-stripe
python -m venv env && source env/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

### Configuration

Remplis le fichier `.env` :

```ini
STRIPE_API_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/T.../B.../xxxxx
```

### Lancement

```bash
python main.py
```

Le serveur démarre sur `http://127.0.0.1:8000`.

### Test local avec Stripe CLI

```bash
# Terminal 1
python main.py

# Terminal 2
stripe listen --forward-to localhost:8000/webhook

# Terminal 3
stripe trigger payment_intent.succeeded
```

## Architecture

```
webhook stripe/
├── main.py                    # Point d'entrée FastAPI
├── config.py                  # Variables d'environnement
├── controllers/
│   └── webhook_controller.py  # Orchestre le flux webhook
├── services/
│   ├── stripe/                # Signature, parsing, classification
│   │   ├── signature.py
│   │   ├── parser.py
│   │   └── classifier.py
│   └── slack/                 # Formatage, envoi HTTP, retry
│       ├── formatter.py
│       ├── client.py
│       ├── notifier.py
│       └── exceptions.py
├── models/
│   ├── stripe_event.py        # Modèle Pydantic événement Stripe
│   └── slack_message.py       # Modèle Pydantic message Slack
└── utils/
    ├── logger.py              # Configuration des logs
    └── stripe_event_catalog.py # Catalogue des 231 événements
```

### Flux de traitement

```
Stripe POST /webhook
    │
    ▼
Vérification signature (immédiat)
    │
    ├── Invalide → 400 + log warning
    │
    └── Valide → 200 OK (réponse immédiate à Stripe)
         │
         ▼
    Tâche de fond :
         │
         ├── Parsing Pydantic
         ├── Classification (catégorie + sévérité)
         ├── Formatage message Slack
         └── Envoi HTTP avec retry
```

## Configuration complète

| Variable | Requis | Défaut | Description |
|----------|--------|--------|-------------|
| `STRIPE_API_KEY` | Oui | — | Clé API Stripe |
| `STRIPE_WEBHOOK_SECRET` | Oui | — | Secret du webhook Stripe (`whsec_...`) |
| `SLACK_WEBHOOK_URL` | Oui | — | URL Incoming Webhook Slack |
| `SLACK_HTTP_TIMEOUT` | Non | `5.0` | Timeout HTTP en secondes |
| `SLACK_MAX_RETRIES` | Non | `3` | Nombre de tentatives max |
| `SLACK_RETRY_BACKOFF` | Non | `1.0` | Backoff initial (doublé à chaque retry) |
| `LOG_LEVEL` | Non | `INFO` | Niveau de log (`DEBUG`, `INFO`, `WARNING`, `ERROR`) |

## Catégories d'événements

| Catégorie | Événements | Exemples |
|-----------|-----------|----------|
| Paiement | 25 | `payment_intent.*`, `charge.*`, `refund.*`, `checkout.session.*` |
| Facturation | 72 | `invoice.*`, `subscription.*`, `quote.*`, `price.*`, `product.*` |
| Client | 15 | `customer.*`, `cash_balance.*` |
| Risque / Fraude | 9 | `charge.dispute.*`, `radar.*`, `review.*` |
| Moyen de paiement | 17 | `payment_method.*`, `setup_intent.*`, `mandate.*` |
| Trésorerie | 23 | `payout.*`, `transfer.*`, `topup.*`, `balance.*` |
| Connect | 13 | `account.*`, `person.*`, `capability.*` |
| Issuing | 22 | `issuing_authorization.*`, `issuing_card.*`, `issuing_transaction.*` |
| Autres | 35 | `identity.*`, `financial_connections.*`, `terminal.*`, `climate.*` |

## Sévérités et couleurs

| Sévérité | Couleur | Usage |
|----------|---------|-------|
| `critical` | Rouge | Échecs de paiement, litiges, fraude |
| `high` | Vert | Paiements réussis, factures payées, abonnements |
| `medium` | Jaune | Mises à jour, actions en cours |
| `low` | Gris | Créations mineures, changements informatifs |
| `info` | Gris | Opérations catalogue (prix, produit, plan) |

## Documentation

Voir le dossier [`docs/`](docs/) pour :

- [Installation détaillée](docs/guide-installation.md)
- [Guide d'utilisation](docs/guide-utilisation.md)
- [Intégration dans un projet existant](docs/guide-integration.md)
- [Comparaison avec l'app Stripe officielle pour Slack](docs/comparaison-stripe-slack-app.md)

## Stack technique

- **FastAPI** — Framework web async
- **Pydantic** — Validation des données
- **httpx** — Client HTTP async (envoi Slack)
- **stripe** — SDK officiel (vérification de signature)
- **uvicorn** — Serveur ASGI
