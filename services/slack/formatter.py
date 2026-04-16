import time
from datetime import datetime

from models.slack_message import SlackAttachment, SlackField, SlackMessage

# --- Couleur de la barre latérale selon la sévérité ---
_COLORS: dict[str, str] = {
    "info": "#cccccc",
    "low": "#cccccc",
    "medium": "#ffcc00",
    "high": "#2eb886",
    "critical": "#e01e5a",
}
_DEFAULT_COLOR = "#cccccc"

# --- Titre humain par event_type : (emoji, label) ---
# Couvre les événements à haute valeur métier. Les autres tombent sur
# le fallback générique (emoji de catégorie + type reformaté).
_TITLES: dict[str, tuple[str, str]] = {
    # Paiements
    "payment_intent.created": ("💳", "Paiement initié"),
    "payment_intent.succeeded": ("✅", "Paiement réussi"),
    "payment_intent.payment_failed": ("⚠️", "Paiement échoué"),
    "payment_intent.canceled": ("🚫", "Paiement annulé"),
    "payment_intent.requires_action": ("🔐", "Action client requise"),
    "payment_intent.processing": ("⏳", "Paiement en cours"),
    "charge.succeeded": ("✅", "Paiement encaissé"),
    "charge.failed": ("⚠️", "Paiement refusé"),
    "charge.captured": ("💰", "Capture du paiement"),
    "charge.refunded": ("↩️", "Remboursement effectué"),
    "charge.expired": ("⌛", "Paiement expiré"),
    "refund.created": ("↩️", "Remboursement créé"),
    "refund.failed": ("⚠️", "Remboursement échoué"),
    "checkout.session.completed": ("🛒", "Commande finalisée"),
    "checkout.session.expired": ("⌛", "Session de paiement expirée"),
    "checkout.session.async_payment_succeeded": ("✅", "Paiement différé réussi"),
    "checkout.session.async_payment_failed": ("⚠️", "Paiement différé échoué"),
    # Litiges / fraude
    "charge.dispute.created": ("🚨", "Litige ouvert"),
    "charge.dispute.updated": ("🚨", "Litige mis à jour"),
    "charge.dispute.closed": ("✅", "Litige clos"),
    "charge.dispute.funds_withdrawn": ("💸", "Fonds retirés (litige)"),
    "charge.dispute.funds_reinstated": ("💰", "Fonds restitués (litige)"),
    "radar.early_fraud_warning.created": ("🚨", "Alerte de fraude (Radar)"),
    "review.opened": ("🔎", "Examen manuel ouvert"),
    "review.closed": ("✅", "Examen manuel clos"),
    # Facturation
    "invoice.created": ("🧾", "Facture créée"),
    "invoice.finalized": ("🧾", "Facture finalisée"),
    "invoice.paid": ("✅", "Facture payée"),
    "invoice.payment_succeeded": ("✅", "Facture réglée"),
    "invoice.payment_failed": ("⚠️", "Échec de paiement de facture"),
    "invoice.payment_action_required": ("🔐", "Action client requise (facture)"),
    "invoice.overdue": ("⏰", "Facture en retard"),
    "invoice.voided": ("🗑️", "Facture annulée"),
    "invoice.upcoming": ("📅", "Facture à venir"),
    "invoice.sent": ("📨", "Facture envoyée"),
    "invoice.finalization_failed": ("⚠️", "Échec de finalisation de facture"),
    "invoice.marked_uncollectible": ("❗", "Facture irrécouvrable"),
    # Abonnements
    "customer.subscription.created": ("🔔", "Abonnement créé"),
    "customer.subscription.updated": ("🔄", "Abonnement mis à jour"),
    "customer.subscription.deleted": ("🔕", "Abonnement annulé"),
    "customer.subscription.paused": ("⏸️", "Abonnement mis en pause"),
    "customer.subscription.resumed": ("▶️", "Abonnement repris"),
    "customer.subscription.trial_will_end": ("⏰", "Fin de période d'essai proche"),
    # Devis
    "quote.created": ("📋", "Devis créé"),
    "quote.accepted": ("✅", "Devis accepté"),
    "quote.canceled": ("🚫", "Devis annulé"),
    "quote.will_expire": ("⏰", "Devis bientôt expiré"),
    # Clients
    "customer.created": ("👤", "Nouveau client"),
    "customer.updated": ("✏️", "Client mis à jour"),
    "customer.deleted": ("🗑️", "Client supprimé"),
    # Moyens de paiement
    "payment_method.attached": ("🔗", "Moyen de paiement ajouté"),
    "payment_method.detached": ("🔓", "Moyen de paiement retiré"),
    "payment_method.automatically_updated": ("🔄", "Carte mise à jour automatiquement"),
    "setup_intent.succeeded": ("✅", "Enregistrement de moyen réussi"),
    "setup_intent.setup_failed": ("⚠️", "Échec d'enregistrement de moyen"),
    # Virements / trésorerie
    "payout.created": ("🏦", "Virement créé"),
    "payout.paid": ("✅", "Virement effectué"),
    "payout.failed": ("⚠️", "Virement échoué"),
    "payout.canceled": ("🚫", "Virement annulé"),
    "topup.succeeded": ("💰", "Rechargement réussi"),
    "topup.failed": ("⚠️", "Rechargement échoué"),
    "transfer.created": ("🔁", "Transfert créé"),
    "transfer.reversed": ("↩️", "Transfert annulé"),
}

# Emoji par catégorie (fallback quand l'event_type n'a pas de titre dédié)
_CATEGORY_EMOJI: dict[str, str] = {
    "payment": "💳",
    "billing": "🧾",
    "risk_fraud": "🚨",
    "customer": "👤",
    "payment_method": "🔗",
    "payout_treasury": "🏦",
    "connect": "🔌",
    "identity": "🪪",
    "financial_connections": "🏛️",
    "issuing": "💳",
    "terminal": "🖥️",
    "climate": "🌱",
    "operations": "⚙️",
    "test": "🧪",
}

# Libellé humain par catégorie (affiché en footer)
_CATEGORY_LABELS: dict[str, str] = {
    "payment": "Paiement",
    "billing": "Facturation",
    "risk_fraud": "Risque / Fraude",
    "customer": "Client",
    "payment_method": "Moyen de paiement",
    "payout_treasury": "Trésorerie",
    "connect": "Connect",
    "identity": "Identity",
    "financial_connections": "Financial Connections",
    "issuing": "Issuing",
    "terminal": "Terminal",
    "climate": "Climate",
    "operations": "Opérations",
    "test": "Test",
}

# Libellés FR pour les champs techniques du catalogue Stripe.
# Valeur None = champ volontairement masqué (consommé ailleurs, ex: currency).
_FIELD_LABELS: dict[str, str | None] = {
    "id": None,
    "currency": None,
    "metadata": None,
    "client_secret": None,
    "object": None,
    "amount": "Montant",
    "amount_total": "Total",
    "amount_due": "Montant dû",
    "amount_paid": "Montant payé",
    "amount_refunded": "Remboursé",
    "amount_captured": "Encaissé",
    "amount_capturable": "Capturable",
    "amount_received": "Reçu",
    "amount_reversed": "Annulé",
    "amount_off": "Réduction",
    "unit_amount": "Prix unitaire",
    "net_amount": "Montant net",
    "customer": "Client",
    "status": "Statut",
    "payment_status": "Statut paiement",
    "reason": "Raison",
    "email": "Email",
    "name": "Nom",
    "phone": "Téléphone",
    "number": "N° facture",
    "description": "Description",
    "type": "Type",
    "mode": "Mode",
    "active": "Actif",
    "card.brand": "Carte",
    "card.last4": "4 derniers",
    "card.exp_month": "Exp. mois",
    "card.exp_year": "Exp. année",
    "last4": "4 derniers",
    "exp_month": "Exp. mois",
    "exp_year": "Exp. année",
    "payment_method_details.type": "Moyen",
    "payment_method": "Moyen",
    "receipt_url": "Reçu",
    "hosted_invoice_url": "Facture en ligne",
    "url": "Lien",
    "return_url": "URL retour",
    "cancellation_reason": "Motif annulation",
    "cancellation_details.reason": "Motif",
    "canceled_at": "Annulé le",
    "failure_code": "Code erreur",
    "failure_message": "Message erreur",
    "failure_reason": "Raison",
    "last_payment_error.code": "Code erreur",
    "last_payment_error.message": "Message erreur",
    "last_payment_error.decline_code": "Code refus",
    "last_setup_error.code": "Code erreur",
    "last_setup_error.message": "Message erreur",
    "last_finalization_error.code": "Code erreur",
    "last_finalization_error.message": "Message erreur",
    "outcome.reason": "Motif",
    "outcome.risk_level": "Niveau de risque",
    "next_action.type": "Prochaine action",
    "trial_end": "Fin essai",
    "current_period_end": "Fin période",
    "current_phase.end_date": "Fin phase",
    "period_end": "Fin période",
    "due_date": "Échéance",
    "next_payment_attempt": "Prochaine tentative",
    "arrival_date": "Arrivée",
    "attempt_count": "Tentatives",
    "charge": "Paiement",
    "invoice": "Facture",
    "subscription": "Abonnement",
    "payment_intent": "Paiement",
    "destination": "Destination",
    "source": "Source",
    "source_transaction": "Transaction source",
    "product": "Produit",
    "interval": "Fréquence",
    "recurring.interval": "Fréquence",
    "institution_name": "Banque",
    "merchant_data.name": "Marchand",
    "display_name": "Nom affiché",
    "nickname": "Nom",
    "evidence_details.due_by": "Preuve avant",
    "percent_off": "Remise %",
    "duration": "Durée",
    "code": "Code",
    "fraud_type": "Type fraude",
    "actionable": "Actionnable",
    "opened_reason": "Motif ouverture",
    "closed_reason": "Motif fermeture",
    "alert_type": "Type alerte",
    "value": "Valeur",
    "charges_enabled": "Paiements actifs",
    "payouts_enabled": "Virements actifs",
    "requirements.disabled_reason": "Raison désactivation",
    "requirements.currently_due": "Infos requises",
    "verification.status": "Vérification",
    "pause_collection.behavior": "Pause",
    "is_default": "Par défaut",
    "cardholder": "Titulaire",
    "card": "Carte",
    "transaction": "Transaction",
    "delivered_at": "Livré le",
    "metric_tons": "Tonnes CO₂",
    "expected_delivery_year": "Année prévue",
    "wallet_provider": "Portefeuille",
    "frozen_time": "Horloge",
    "report_type": "Type rapport",
    "filename": "Fichier",
    "purpose": "Usage",
    "size": "Taille (o)",
    "jurisdiction": "Juridiction",
    "percentage": "Taux %",
    "items.data[].price.id": "Prix",
    "entitlements.data[].lookup_key": "Droit",
    "amount.monetary.value": "Crédit",
    "amount.monetary.currency": None,
    "defaults.tax_behavior": "Comportement fiscal",
    "payouts.schedule.interval": "Fréquence virements",
    "balance_refresh.status": "Rafraîch. solde",
    "ownership_refresh.status": "Rafraîch. titulaire",
    "transaction_refresh.status": "Rafraîch. transactions",
    "action.type": "Action",
    "action.status": "Statut action",
    "action.failure_code": "Code échec",
    "action.failure_message": "Message échec",
    "pending_request.amount": "Montant demandé",
    "current_prices_per_metric_ton": "Prix/tonne",
    "released_at": "Libéré le",
    "released_subscription": "Abonnement libéré",
    "completed_at": "Terminé le",
    "current_phase": "Phase",
    "reconciliation_status": "Statut rapprochement",
    "rejection_reasons": "Motifs rejet",
    "available": "Disponible",
    "pending": "En attente",
    "result.url": "Résultat",
    "error": "Erreur",
    "version": "Version",
    "result_available_until": "Dispo. jusqu'au",
    "sql": "Requête",
    "expires_at": "Expire le",
    "coupon.id": "Coupon",
    "event_name": "Événement",
    "usage": "Usage",
    "fee": "Frais",
}

# Champs contenant un montant en plus petite unité (cents, yen…)
_AMOUNT_FIELDS = frozenset({
    "amount", "amount_total", "amount_due", "amount_paid", "amount_refunded",
    "amount_captured", "amount_capturable", "amount_received", "amount_reversed",
    "amount_off", "unit_amount", "net_amount",
    "pending_request.amount", "amount.monetary.value",
})

# Champs interprétés comme timestamp unix
_TIMESTAMP_FIELDS = frozenset({
    "trial_end", "current_period_end", "period_end", "canceled_at", "due_date",
    "next_payment_attempt", "arrival_date", "evidence_details.due_by",
    "current_phase.end_date", "delivered_at", "released_at", "completed_at",
    "expires_at", "result_available_until", "frozen_time",
})

# Devises sans subdivision (Stripe docs : zero-decimal currencies)
_ZERO_DECIMAL = frozenset({
    "bif", "clp", "djf", "gnf", "jpy", "kmf", "krw", "mga", "pyg",
    "rwf", "ugx", "vnd", "vuv", "xaf", "xof", "xpf",
})
_CURRENCY_SYMBOLS: dict[str, str] = {
    "eur": "€", "usd": "$", "gbp": "£", "jpy": "¥", "chf": "CHF",
    "cad": "CA$", "aud": "AU$",
}

# Préfixes d'IDs Stripe → rendu en `code`
_ID_PREFIXES = (
    "cus_", "sub_", "pi_", "ch_", "in_", "pm_", "pr_", "price_", "prod_",
    "re_", "py_", "ba_", "src_", "si_", "setupintent_", "tok_",
    "dp_", "txn_", "iauth_", "ic_", "ich_", "ipd_", "itxn_", "ipi_",
    "fca_", "vs_", "trr_", "tr_", "po_", "acct_", "an_", "fee_", "evt_",
    "plan_", "qt_", "cs_", "sch_", "cn_", "promo_", "txr_",
)


# Renvoie la couleur de barre latérale Slack selon la sévérité
def _color(severity: str) -> str:
    return _COLORS.get(severity.lower(), _DEFAULT_COLOR)


# Convertit un montant Stripe (plus petite unité) en string monétaire FR
def _format_amount(value, currency: str | None) -> str:
    if not isinstance(value, (int, float)):
        return str(value)
    cur = (currency or "eur").lower()
    symbol = _CURRENCY_SYMBOLS.get(cur, cur.upper())
    if cur in _ZERO_DECIMAL:
        formatted = f"{int(value):,}".replace(",", " ")
        return f"{formatted} {symbol}"
    formatted = f"{value / 100:,.2f}".replace(",", " ").replace(".", ",")
    return f"{formatted} {symbol}"


# Convertit un unix timestamp en date humaine FR
def _format_timestamp(value) -> str:
    if not isinstance(value, (int, float)) or value <= 0:
        return str(value)
    try:
        return datetime.fromtimestamp(int(value)).strftime("%d/%m/%Y %H:%M")
    except (ValueError, OSError, OverflowError):
        return str(value)


# Vérifie si la valeur est un identifiant Stripe (préfixe reconnu)
def _is_stripe_id(value) -> bool:
    return isinstance(value, str) and value.startswith(_ID_PREFIXES)


# Tronque proprement un ID Stripe trop long pour l'affichage
def _short_id(value: str, keep: int = 14) -> str:
    if len(value) <= keep + 2:
        return value
    return f"{value[:keep]}…"


# Convertit une valeur brute en chaîne lisible pour Slack (mrkdwn)
def _format_value(key: str, value, currency: str | None) -> str:
    if value is None:
        return "—"
    if key in _AMOUNT_FIELDS:
        return _format_amount(value, currency)
    if key in _TIMESTAMP_FIELDS:
        return _format_timestamp(value)
    if isinstance(value, bool):
        return "oui" if value else "non"
    if isinstance(value, str):
        if value.startswith(("http://", "https://")):
            return f"<{value}|Ouvrir>"
        if _is_stripe_id(value):
            return f"`{value}`"
        return value
    if isinstance(value, (list, tuple)):
        if not value:
            return "—"
        return ", ".join(str(v) for v in value)
    if isinstance(value, dict):
        if not value:
            return "—"
        return ", ".join(f"{k}: {v}" for k, v in value.items())
    return str(value)


# Génère le titre humain du message Slack (emoji + label) selon le type d'événement
def _human_title(event_type: str, category: str) -> str:
    if event_type in _TITLES:
        emoji, label = _TITLES[event_type]
        return f"{emoji}  {label}"
    emoji = _CATEGORY_EMOJI.get(category, "🔔")
    # Rendu lisible du type : "customer.subscription.updated" → "Customer subscription updated"
    label = event_type.replace(".", " ").replace("_", " ").capitalize()
    return f"{emoji}  {label}"


# Construit la liste des champs Slack à partir du payload Stripe
def _build_fields(payload: dict) -> list[SlackField]:
    currency = payload.get("currency") or payload.get("amount.monetary.currency")
    fields: list[SlackField] = []
    for key, value in payload.items():
        if key in _FIELD_LABELS and _FIELD_LABELS[key] is None:
            continue
        if value is None or value == "" or value == [] or value == {}:
            continue
        label = _FIELD_LABELS.get(key)
        if label is None:
            # Fallback : humanise automatiquement la clé
            label = key.replace("_", " ").replace(".", " · ").capitalize()
        fields.append(SlackField(
            title=label,
            value=_format_value(key, value, currency),
            short=True,
        ))
    return fields


# Construit le message Slack complet (titre humain + champs structurés + footer discret)
def build_message(event_type: str, category: str, severity: str, payload: dict) -> SlackMessage:
    title = _human_title(event_type, category)
    fields = _build_fields(payload)
    category_label = _CATEGORY_LABELS.get(category, category.capitalize())

    footer_parts = [category_label]
    event_id = payload.get("id")
    if isinstance(event_id, str):
        footer_parts.append(_short_id(event_id, keep=20))

    attachment = SlackAttachment(
        color=_color(severity),
        title=title,
        text="",
        fields=fields,
        mrkdwn_in=["fields", "text"],
        footer=" · ".join(footer_parts),
        ts=int(time.time()),
    )

    fallback_text = f"[{severity.upper()}] {category_label} — {event_type}"
    return SlackMessage(text=fallback_text, attachments=[attachment])
