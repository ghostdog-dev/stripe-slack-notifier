# Guide d'installation

## Prérequis

- **Python 3.11+** (utilise la syntaxe `type | None`)
- **Un compte Stripe** avec accès au dashboard
- **Un workspace Slack** avec les droits pour créer une app

## 1. Cloner et installer

```bash
git clone <repo-url>
cd webhook-stripe

# Créer l'environnement virtuel
python -m venv env
source env/bin/activate    # Linux/macOS
# ou: env\Scripts\activate  # Windows

# Installer les dépendances
pip install -r requirements.txt
```

### Dépendances

| Package | Rôle |
|---------|------|
| `fastapi` | Framework web async |
| `uvicorn` | Serveur ASGI |
| `stripe` | SDK Stripe (vérification de signature) |
| `httpx` | Client HTTP async (envoi Slack) |
| `pydantic` | Validation des données |
| `python-dotenv` | Chargement des variables d'environnement |

## 2. Configurer Stripe

### Récupérer la clé API

1. Va sur [dashboard.stripe.com/apikeys](https://dashboard.stripe.com/apikeys)
2. Copie la **clé secrète** (`sk_test_...` pour le mode test, `sk_live_...` pour la production)

### Créer le webhook

1. Va sur [dashboard.stripe.com/webhooks](https://dashboard.stripe.com/webhooks)
2. Clique **Ajouter un endpoint**
3. URL : `https://ton-domaine.com/webhook`
4. Sélectionne les événements à écouter (ou tous)
5. Copie le **signing secret** (`whsec_...`)

### Test local avec Stripe CLI

Pour tester sans déployer :

```bash
# Installer Stripe CLI : https://stripe.com/docs/stripe-cli
stripe login
stripe listen --forward-to localhost:8000/webhook
```

Le CLI affiche un `whsec_...` temporaire — utilise-le dans ton `.env` pour les tests locaux.

## 3. Configurer Slack

### Créer un Incoming Webhook

1. Va sur [api.slack.com/apps](https://api.slack.com/apps) → **Create New App** → **From scratch**
2. Donne un nom (ex: `Stripe Notifier`) et sélectionne ton workspace
3. Menu gauche → **Incoming Webhooks** → active le toggle
4. Clique **Add New Webhook to Workspace**
5. Choisis le canal cible (ex: `#stripe-notifications`)
6. Copie l'URL (`https://hooks.slack.com/services/T.../B.../xxxxx`)

## 4. Configurer l'application

```bash
cp .env.example .env
```

Remplis le fichier `.env` :

```ini
# Obligatoire
STRIPE_API_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/T.../B.../xxxxx

# Optionnel (valeurs par défaut)
SLACK_HTTP_TIMEOUT=5.0
SLACK_MAX_RETRIES=3
SLACK_RETRY_BACKOFF=1.0
LOG_LEVEL=INFO
```

### Paramètres réseau Slack

| Variable | Défaut | Description |
|----------|--------|-------------|
| `SLACK_HTTP_TIMEOUT` | `5.0` | Timeout par requête en secondes |
| `SLACK_MAX_RETRIES` | `3` | Nombre de tentatives en cas d'erreur |
| `SLACK_RETRY_BACKOFF` | `1.0` | Délai initial entre les retries (doublé à chaque fois) |

Avec les valeurs par défaut, les retries suivent cette séquence : 1s → 2s → 4s.

## 5. Lancer le serveur

### Développement

```bash
python main.py
```

Le serveur démarre sur `http://127.0.0.1:8000` avec le rechargement automatique activé.

### Production

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

Derrière un reverse proxy (Nginx, Caddy) avec HTTPS.

### Vérifier que tout tourne

```bash
curl http://localhost:8000/
# → {"status":"ok"}
```

## 6. Tester de bout en bout

```bash
# Terminal 1 : serveur
python main.py

# Terminal 2 : Stripe CLI
stripe listen --forward-to localhost:8000/webhook

# Terminal 3 : déclencher un événement
stripe trigger payment_intent.succeeded
```

Tu dois voir :
- Dans le terminal Stripe CLI : `[200] POST http://localhost:8000/webhook`
- Dans les logs serveur : `Notification Slack envoyée (payment | payment_intent.succeeded)`
- Dans Slack : un message formaté avec "✅ Paiement réussi"

## 7. Déploiement

### Variables d'environnement en production

En production, ne mets **jamais** les secrets dans un fichier. Utilise les variables d'environnement de ton hébergeur :

- **Railway / Render / Fly.io** : dashboard → variables d'environnement
- **Docker** : `docker run -e STRIPE_API_KEY=sk_live_... -e ...`
- **VPS** : `export STRIPE_API_KEY=sk_live_...` ou systemd `EnvironmentFile`

### Checklist production

- [ ] Clé API Stripe en mode **live** (`sk_live_...`)
- [ ] Webhook secret correspondant au endpoint **live**
- [ ] HTTPS obligatoire (Stripe refuse les webhooks en HTTP)
- [ ] `LOG_LEVEL=WARNING` pour réduire le bruit
- [ ] Monitoring sur le endpoint `/` (health check)
