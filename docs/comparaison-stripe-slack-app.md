# Stripe Notifier vs App Stripe officielle pour Slack

## Le problème de l'app officielle

L'app [Stripe pour Slack](https://stripe.com/integrations/slack) existe et fonctionne. Mais elle a des limites structurelles qui deviennent vite bloquantes pour un usage professionnel.

## Comparaison détaillée

### Contrôle des notifications

| Critère | App officielle Stripe | Ce notifier |
|---------|----------------------|-------------|
| Choix des événements | Limité (quelques types prédéfinis) | **231 types d'événements** couverts |
| Filtrage par sévérité | Non | Oui (info, low, medium, high, critical) |
| Filtrage par catégorie | Non | Oui (14 catégories métier) |
| Filtrage personnalisé | Non | Oui (par type, sévérité, catégorie, ou logique custom) |

### Format des messages

| Critère | App officielle Stripe | Ce notifier |
|---------|----------------------|-------------|
| Langue | Anglais uniquement | **Français** (libellés, montants, dates) |
| Format des montants | Brut (ex: `1500`) | **Formaté** (ex: `15,00 €`) |
| Format des dates | Timestamp unix brut | **Lisible** (ex: `16/04/2026 01:05`) |
| Emojis contextuels | Non | Oui (✅ succès, ⚠️ échec, 🚨 fraude, etc.) |
| Couleurs par sévérité | Non | Oui (vert, rouge, jaune, gris) |
| Champs structurés | Liste brute | **Colonnes** avec libellés FR |
| IDs techniques | Proéminents | Discrets (en footer) |
| URLs cliquables | Non | Oui (reçus, factures en ligne) |

### Architecture et fiabilité

| Critère | App officielle Stripe | Ce notifier |
|---------|----------------------|-------------|
| Retry en cas d'échec Slack | Non contrôlable | **Configurable** (backoff exponentiel) |
| Traitement non-bloquant | Inconnu | Oui (tâche de fond FastAPI) |
| Timeout configurable | Non | Oui (`SLACK_HTTP_TIMEOUT`) |
| Logs détaillés | Non | Oui (par module, niveau configurable) |
| Health check | Non | Oui (`GET /`) |

### Personnalisation

| Critère | App officielle Stripe | Ce notifier |
|---------|----------------------|-------------|
| Ajouter un événement | Impossible | Ajouter une entrée dans le catalogue |
| Modifier le format | Impossible | Modifier `formatter.py` |
| Multi-canaux Slack | Non | Possible (routage par catégorie) |
| Intégration dans un flux existant | Indépendant | Intégrable comme module Python |
| Auto-hébergé | Non (SaaS) | **Oui** (ton serveur, tes données) |

### Confidentialité et sécurité

| Critère | App officielle Stripe | Ce notifier |
|---------|----------------------|-------------|
| Données transitent par | Serveurs Stripe + Slack Connect | **Ton serveur uniquement** → Slack |
| Accès tiers aux données | Oui (app Stripe lit ton workspace) | Non (Incoming Webhook = écriture seule) |
| Permissions Slack requises | Larges (lecture + écriture) | **Minimales** (Incoming Webhook uniquement) |
| Vérification de signature | Par Stripe (opaque) | Par toi (HMAC-SHA256, auditable) |
| Code source | Fermé | **Ouvert** (auditable) |

## Cas d'usage concrets

### 1. Équipe commerciale francophone

> "Notre équipe suit les paiements en temps réel mais l'app Stripe affiche tout en anglais avec des montants en centimes."

Avec ce notifier : messages en français, montants formatés (`15,00 €`), dates au format FR.

### 2. Alertes critiques seulement

> "On reçoit trop de bruit avec l'app Stripe. On veut uniquement les échecs de paiement et les litiges."

Avec ce notifier : filtre par sévérité `critical` uniquement, ou par événement spécifique.

### 3. Canaux Slack séparés par type

> "On veut les paiements dans `#revenue`, les litiges dans `#urgent`, et les abonnements dans `#customers`."

Avec ce notifier : routage par catégorie vers des Incoming Webhooks différents.

### 4. Intégration dans un backend existant

> "On a déjà une app FastAPI qui gère les webhooks Stripe pour la base de données. On veut juste ajouter les notifs Slack sans toucher au code existant."

Avec ce notifier : déploiement séparé avec un deuxième endpoint webhook dans Stripe. Zéro modification de l'app existante.

### 5. Conformité et audit

> "On ne veut pas que nos données de paiement transitent par une app tierce."

Avec ce notifier : auto-hébergé, seul un Incoming Webhook Slack est utilisé (écriture seule, pas d'accès au workspace). Le code est ouvert et auditable.

### 6. SaaS avec événements billing complexes

> "On a besoin de suivre les tentatives de paiement échouées, les renouvellements, les changements de plan, et les fins de période d'essai."

Avec ce notifier : 72 événements billing couverts, avec `attempt_count`, `next_payment_attempt`, `trial_end`, `cancel_at_period_end`, etc.

## En résumé

L'app officielle Stripe pour Slack convient si :
- Tu veux juste une notification basique en anglais
- Tu n'as pas besoin de filtrage ou de personnalisation
- La confidentialité des données n'est pas un enjeu

Ce notifier convient si :
- Tu veux des messages **lisibles en français** avec des montants formatés
- Tu as besoin de **filtrer** par type, catégorie ou sévérité
- Tu veux **router** vers plusieurs canaux Slack
- Tu préfères **auto-héberger** et garder le contrôle sur tes données
- Tu veux **intégrer** les notifications dans un flux existant
- Tu as besoin de **logs** et de **retry** fiables
