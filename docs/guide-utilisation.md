# Guide d'utilisation

## Comment ça marche

Le serveur expose un seul endpoint `POST /webhook` qui :

1. **Vérifie la signature** — rejette les requêtes non authentifiées
2. **Répond immédiatement** `200 OK` à Stripe — pas de timeout
3. **Traite en arrière-plan** — parse, classe et notifie Slack

Tu n'as rien à faire côté code une fois le serveur lancé. Stripe envoie, le serveur traite, Slack affiche.

## Anatomie d'une notification Slack

```
┌─────────────────────────────────────────────────┐
│ ✅  Paiement réussi                 (barre verte)│
│                                                  │
│  Montant          Client                         │
│  15,00 €          cus_ULIudEfj…                  │
│                                                  │
│  Paiement · pi_3TMcIe… · 16/04/2026 01:05       │
└─────────────────────────────────────────────────┘
```

| Élément | Description |
|---------|-------------|
| Barre colorée | Sévérité : vert (succès), rouge (échec/critique), jaune (attention), gris (info) |
| Titre avec emoji | Description humaine de l'événement |
| Champs en colonnes | Données clés extraites du payload Stripe |
| Footer | Catégorie + ID Stripe (pour retrouver dans le dashboard) + horodatage |

## Les 231 événements couverts

Chaque événement Stripe est défini dans le catalogue (`utils/stripe_event_catalog.py`) avec :

- **`category`** — Domaine métier (payment, billing, customer, etc.)
- **`severity`** — Niveau d'alerte (info, low, medium, high, critical)
- **`key_fields`** — Champs extraits du payload et affichés dans Slack

### Événements les plus courants

#### Paiements

| Événement | Sévérité | Ce qui s'affiche |
|-----------|----------|-----------------|
| `payment_intent.succeeded` | high | Montant, devise, client |
| `payment_intent.payment_failed` | critical | Montant, code erreur, message, code refus |
| `charge.succeeded` | high | Montant, client, moyen de paiement, lien reçu |
| `charge.failed` | critical | Montant, code erreur, motif, niveau de risque |
| `charge.refunded` | high | Montant, montant remboursé, devise |
| `checkout.session.completed` | high | Total, client, email, mode |

#### Facturation

| Événement | Sévérité | Ce qui s'affiche |
|-----------|----------|-----------------|
| `invoice.paid` | high | N° facture, client, montant payé |
| `invoice.payment_failed` | critical | Client, montant dû, nb tentatives, prochaine tentative |
| `invoice.finalized` | medium | N° facture, client, montant dû, lien facture |
| `invoice.overdue` | high | Client, montant dû, échéance |

#### Abonnements

| Événement | Sévérité | Ce qui s'affiche |
|-----------|----------|-----------------|
| `customer.subscription.created` | high | Client, statut, fin période, fin essai |
| `customer.subscription.deleted` | high | Client, statut, date annulation, motif |
| `customer.subscription.trial_will_end` | medium | Client, fin essai |

#### Litiges et fraude

| Événement | Sévérité | Ce qui s'affiche |
|-----------|----------|-----------------|
| `charge.dispute.created` | critical | Montant, raison, statut, deadline preuve |
| `radar.early_fraud_warning.created` | critical | Paiement, type fraude |

## Personnalisation

### Ajouter un événement au catalogue

Dans `utils/stripe_event_catalog.py`, ajoute une entrée :

```python
"ma_resource.mon_event": {
    "category": "billing",
    "severity": "high",
    "object_type": "ma_resource",
    "key_fields": ("id", "amount", "currency", "status"),
},
```

Les `key_fields` sont les chemins vers les champs dans l'objet Stripe. Les chemins pointés sont supportés : `"payment_method_details.type"`, `"last_payment_error.message"`.

### Ajouter un titre humain

Dans `services/slack/formatter.py`, ajoute dans le dict `_TITLES` :

```python
"ma_resource.mon_event": ("🎯", "Mon titre personnalisé"),
```

Sans titre dédié, le fallback génère automatiquement un titre à partir du type d'événement avec l'emoji de la catégorie.

### Ajouter un label de champ

Dans `services/slack/formatter.py`, ajoute dans le dict `_FIELD_LABELS` :

```python
"mon_champ_technique": "Mon libellé FR",
```

Pour masquer un champ de l'affichage (sans le supprimer du catalogue), utilise `None` :

```python
"champ_interne": None,
```

### Modifier les couleurs de sévérité

Dans `services/slack/formatter.py`, modifie le dict `_COLORS` :

```python
_COLORS = {
    "info": "#cccccc",
    "low": "#cccccc",
    "medium": "#ffcc00",
    "high": "#2eb886",
    "critical": "#e01e5a",
}
```

### Modifier le formatage des montants

Le formatter convertit automatiquement les montants Stripe (en centimes) en format monétaire :

- `1500` + `usd` → `15,00 $`
- `1500` + `eur` → `15,00 €`
- `1500` + `jpy` → `1 500 ¥` (devise sans décimales)

Pour ajouter un symbole de devise, modifie `_CURRENCY_SYMBOLS` dans `formatter.py`.

## Logs

### Format

```
2026-04-16 01:05:34 | INFO     | services.slack.notifier | Notification Slack envoyée (payment | charge.succeeded)
2026-04-16 01:05:35 | WARNING  | controllers.webhook_controller | Webhook Stripe rejeté : invalid_signature
```

### Niveaux utiles

| Niveau | Ce que tu vois |
|--------|---------------|
| `DEBUG` | Tout, y compris les détails de traitement |
| `INFO` | Notifications envoyées, démarrage serveur |
| `WARNING` | Webhooks rejetés, événements inconnus |
| `ERROR` | Échecs d'envoi Slack, événements invalides |

Change le niveau dans `.env` : `LOG_LEVEL=WARNING`

## Monitoring

### Health check

```bash
curl http://localhost:8000/
# → {"status":"ok"}
```

Utilise cette URL pour tes checks de disponibilité (UptimeRobot, Pingdom, etc.).

### Ce qu'il faut surveiller

- **Logs `WARNING`** : webhooks rejetés → signature invalide ou type d'événement inconnu
- **Logs `ERROR`** : échecs Slack → problème réseau, URL webhook invalide, rate limit
- **Dashboard Stripe** → Webhooks → onglet "Attempts" : vérifie que les réponses sont `200`
