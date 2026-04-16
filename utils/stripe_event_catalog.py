EVENT_CATALOG: dict[str, dict] = {

    # =========================================================
    # PAYMENT — payment_intent / charge / checkout / refund
    # =========================================================
    "payment_intent.created": {
        "category": "payment", "severity": "low", "object_type": "payment_intent",
        "key_fields": ("id", "amount", "currency", "customer", "status"),
    },
    "payment_intent.processing": {
        "category": "payment", "severity": "medium", "object_type": "payment_intent",
        "key_fields": ("id", "amount", "currency", "status", "payment_method"),
    },
    "payment_intent.requires_action": {
        "category": "payment", "severity": "medium", "object_type": "payment_intent",
        "key_fields": ("id", "amount", "next_action.type", "client_secret"),
    },
    "payment_intent.amount_capturable_updated": {
        "category": "payment", "severity": "medium", "object_type": "payment_intent",
        "key_fields": ("id", "amount", "amount_capturable"),
    },
    "payment_intent.partially_funded": {
        "category": "payment", "severity": "medium", "object_type": "payment_intent",
        "key_fields": ("id", "amount", "amount_received", "currency"),
    },
    "payment_intent.succeeded": {
        "category": "payment", "severity": "high", "object_type": "payment_intent",
        "key_fields": ("id", "amount", "currency", "customer", "latest_charge", "metadata"),
    },
    "payment_intent.payment_failed": {
        "category": "payment", "severity": "critical", "object_type": "payment_intent",
        "key_fields": ("id", "amount", "currency", "customer",
                       "last_payment_error.code", "last_payment_error.message",
                       "last_payment_error.decline_code"),
    },
    "payment_intent.canceled": {
        "category": "payment", "severity": "high", "object_type": "payment_intent",
        "key_fields": ("id", "amount", "customer", "cancellation_reason"),
    },

    "charge.succeeded": {
        "category": "payment", "severity": "high", "object_type": "charge",
        "key_fields": ("id", "amount", "currency", "customer", "payment_intent",
                       "payment_method_details.type", "receipt_url"),
    },
    "charge.failed": {
        "category": "payment", "severity": "critical", "object_type": "charge",
        "key_fields": ("id", "amount", "currency", "failure_code", "failure_message",
                       "outcome.reason", "outcome.risk_level"),
    },
    "charge.captured": {
        "category": "payment", "severity": "high", "object_type": "charge",
        "key_fields": ("id", "amount_captured", "amount", "payment_intent"),
    },
    "charge.pending": {
        "category": "payment", "severity": "medium", "object_type": "charge",
        "key_fields": ("id", "amount", "currency", "payment_method_details.type"),
    },
    "charge.expired": {
        "category": "payment", "severity": "medium", "object_type": "charge",
        "key_fields": ("id", "amount", "payment_intent"),
    },
    "charge.updated": {
        "category": "payment", "severity": "low", "object_type": "charge",
        "key_fields": ("id", "status", "amount"),
    },
    "charge.refunded": {
        "category": "payment", "severity": "high", "object_type": "charge",
        "key_fields": ("id", "amount", "amount_refunded", "currency", "refunded"),
    },
    "charge.refund.updated": {
        "category": "payment", "severity": "medium", "object_type": "refund",
        "key_fields": ("id", "charge", "amount", "status", "failure_reason"),
    },

    "refund.created": {
        "category": "payment", "severity": "high", "object_type": "refund",
        "key_fields": ("id", "charge", "amount", "currency", "reason", "status"),
    },
    "refund.updated": {
        "category": "payment", "severity": "medium", "object_type": "refund",
        "key_fields": ("id", "charge", "status", "failure_reason"),
    },
    "refund.failed": {
        "category": "payment", "severity": "critical", "object_type": "refund",
        "key_fields": ("id", "charge", "amount", "failure_reason"),
    },

    "checkout.session.completed": {
        "category": "payment", "severity": "high", "object_type": "checkout.session",
        "key_fields": ("id", "payment_status", "amount_total", "currency",
                       "customer", "customer_details.email", "mode", "metadata"),
    },
    "checkout.session.async_payment_succeeded": {
        "category": "payment", "severity": "high", "object_type": "checkout.session",
        "key_fields": ("id", "payment_status", "amount_total", "customer"),
    },
    "checkout.session.async_payment_failed": {
        "category": "payment", "severity": "critical", "object_type": "checkout.session",
        "key_fields": ("id", "payment_status", "amount_total", "customer"),
    },
    "checkout.session.expired": {
        "category": "payment", "severity": "medium", "object_type": "checkout.session",
        "key_fields": ("id", "amount_total", "customer"),
    },

    "payment_link.created": {
        "category": "payment", "severity": "info", "object_type": "payment_link",
        "key_fields": ("id", "url", "active"),
    },
    "payment_link.updated": {
        "category": "payment", "severity": "info", "object_type": "payment_link",
        "key_fields": ("id", "active"),
    },

    # =========================================================
    # DISPUTES / FRAUD / REVIEW
    # =========================================================
    "charge.dispute.created": {
        "category": "risk_fraud", "severity": "critical", "object_type": "dispute",
        "key_fields": ("id", "charge", "amount", "currency", "reason", "status",
                       "evidence_details.due_by"),
    },
    "charge.dispute.updated": {
        "category": "risk_fraud", "severity": "high", "object_type": "dispute",
        "key_fields": ("id", "status", "reason", "evidence_details.due_by"),
    },
    "charge.dispute.closed": {
        "category": "risk_fraud", "severity": "high", "object_type": "dispute",
        "key_fields": ("id", "status", "amount", "charge"),
    },
    "charge.dispute.funds_withdrawn": {
        "category": "risk_fraud", "severity": "critical", "object_type": "dispute",
        "key_fields": ("id", "amount", "currency", "charge"),
    },
    "charge.dispute.funds_reinstated": {
        "category": "risk_fraud", "severity": "high", "object_type": "dispute",
        "key_fields": ("id", "amount", "currency", "charge"),
    },

    "radar.early_fraud_warning.created": {
        "category": "risk_fraud", "severity": "critical", "object_type": "radar.early_fraud_warning",
        "key_fields": ("id", "charge", "fraud_type", "actionable"),
    },
    "radar.early_fraud_warning.updated": {
        "category": "risk_fraud", "severity": "high", "object_type": "radar.early_fraud_warning",
        "key_fields": ("id", "charge", "fraud_type", "actionable"),
    },

    "review.opened": {
        "category": "risk_fraud", "severity": "high", "object_type": "review",
        "key_fields": ("id", "charge", "payment_intent", "reason", "opened_reason"),
    },
    "review.closed": {
        "category": "risk_fraud", "severity": "medium", "object_type": "review",
        "key_fields": ("id", "charge", "reason", "closed_reason"),
    },

    # =========================================================
    # BILLING / INVOICE / SUBSCRIPTION / QUOTE
    # =========================================================
    "invoice.created": {
        "category": "billing", "severity": "low", "object_type": "invoice",
        "key_fields": ("id", "customer", "amount_due", "currency", "status"),
    },
    "invoice.finalized": {
        "category": "billing", "severity": "medium", "object_type": "invoice",
        "key_fields": ("id", "number", "customer", "amount_due", "currency", "hosted_invoice_url"),
    },
    "invoice.finalization_failed": {
        "category": "billing", "severity": "critical", "object_type": "invoice",
        "key_fields": ("id", "customer", "last_finalization_error.code",
                       "last_finalization_error.message"),
    },
    "invoice.paid": {
        "category": "billing", "severity": "high", "object_type": "invoice",
        "key_fields": ("id", "number", "customer", "amount_paid", "currency"),
    },
    "invoice.payment_succeeded": {
        "category": "billing", "severity": "high", "object_type": "invoice",
        "key_fields": ("id", "customer", "amount_paid", "currency", "subscription"),
    },
    "invoice.payment_failed": {
        "category": "billing", "severity": "critical", "object_type": "invoice",
        "key_fields": ("id", "customer", "amount_due", "currency",
                       "attempt_count", "next_payment_attempt"),
    },
    "invoice.payment_action_required": {
        "category": "billing", "severity": "high", "object_type": "invoice",
        "key_fields": ("id", "customer", "amount_due", "hosted_invoice_url"),
    },
    "invoice.payment_attempt_required": {
        "category": "billing", "severity": "high", "object_type": "invoice",
        "key_fields": ("id", "customer", "amount_due"),
    },
    "invoice.overdue": {
        "category": "billing", "severity": "high", "object_type": "invoice",
        "key_fields": ("id", "customer", "amount_due", "due_date"),
    },
    "invoice.overpaid": {
        "category": "billing", "severity": "medium", "object_type": "invoice",
        "key_fields": ("id", "customer", "amount_paid", "amount_due"),
    },
    "invoice.will_be_due": {
        "category": "billing", "severity": "medium", "object_type": "invoice",
        "key_fields": ("id", "customer", "amount_due", "due_date"),
    },
    "invoice.upcoming": {
        "category": "billing", "severity": "info", "object_type": "invoice",
        "key_fields": ("customer", "amount_due", "currency", "subscription", "period_end"),
    },
    "invoice.sent": {
        "category": "billing", "severity": "info", "object_type": "invoice",
        "key_fields": ("id", "customer", "hosted_invoice_url"),
    },
    "invoice.updated": {
        "category": "billing", "severity": "low", "object_type": "invoice",
        "key_fields": ("id", "status", "amount_due"),
    },
    "invoice.voided": {
        "category": "billing", "severity": "medium", "object_type": "invoice",
        "key_fields": ("id", "customer", "amount_due"),
    },
    "invoice.deleted": {
        "category": "billing", "severity": "low", "object_type": "invoice",
        "key_fields": ("id", "customer"),
    },
    "invoice.marked_uncollectible": {
        "category": "billing", "severity": "high", "object_type": "invoice",
        "key_fields": ("id", "customer", "amount_due"),
    },
    "invoice_payment.paid": {
        "category": "billing", "severity": "high", "object_type": "invoice_payment",
        "key_fields": ("id", "invoice", "amount_paid", "currency", "status"),
    },

    "invoiceitem.created": {
        "category": "billing", "severity": "low", "object_type": "invoiceitem",
        "key_fields": ("id", "customer", "amount", "currency", "description"),
    },
    "invoiceitem.deleted": {
        "category": "billing", "severity": "low", "object_type": "invoiceitem",
        "key_fields": ("id", "customer"),
    },

    "customer.subscription.created": {
        "category": "billing", "severity": "high", "object_type": "subscription",
        "key_fields": ("id", "customer", "status", "items.data[].price.id",
                       "current_period_end", "trial_end"),
    },
    "customer.subscription.updated": {
        "category": "billing", "severity": "medium", "object_type": "subscription",
        "key_fields": ("id", "customer", "status", "cancel_at_period_end",
                       "current_period_end"),
    },
    "customer.subscription.deleted": {
        "category": "billing", "severity": "high", "object_type": "subscription",
        "key_fields": ("id", "customer", "status", "canceled_at", "cancellation_details.reason"),
    },
    "customer.subscription.paused": {
        "category": "billing", "severity": "high", "object_type": "subscription",
        "key_fields": ("id", "customer", "pause_collection.behavior"),
    },
    "customer.subscription.resumed": {
        "category": "billing", "severity": "high", "object_type": "subscription",
        "key_fields": ("id", "customer", "status"),
    },
    "customer.subscription.trial_will_end": {
        "category": "billing", "severity": "medium", "object_type": "subscription",
        "key_fields": ("id", "customer", "trial_end"),
    },
    "customer.subscription.pending_update_applied": {
        "category": "billing", "severity": "medium", "object_type": "subscription",
        "key_fields": ("id", "customer", "status"),
    },
    "customer.subscription.pending_update_expired": {
        "category": "billing", "severity": "medium", "object_type": "subscription",
        "key_fields": ("id", "customer"),
    },

    "subscription_schedule.created": {
        "category": "billing", "severity": "medium", "object_type": "subscription_schedule",
        "key_fields": ("id", "customer", "status", "current_phase"),
    },
    "subscription_schedule.updated": {
        "category": "billing", "severity": "low", "object_type": "subscription_schedule",
        "key_fields": ("id", "status", "current_phase"),
    },
    "subscription_schedule.canceled": {
        "category": "billing", "severity": "high", "object_type": "subscription_schedule",
        "key_fields": ("id", "customer", "canceled_at"),
    },
    "subscription_schedule.completed": {
        "category": "billing", "severity": "medium", "object_type": "subscription_schedule",
        "key_fields": ("id", "customer", "completed_at"),
    },
    "subscription_schedule.released": {
        "category": "billing", "severity": "medium", "object_type": "subscription_schedule",
        "key_fields": ("id", "customer", "released_at", "released_subscription"),
    },
    "subscription_schedule.aborted": {
        "category": "billing", "severity": "high", "object_type": "subscription_schedule",
        "key_fields": ("id", "customer", "status"),
    },
    "subscription_schedule.expiring": {
        "category": "billing", "severity": "medium", "object_type": "subscription_schedule",
        "key_fields": ("id", "customer", "current_phase.end_date"),
    },

    "quote.created": {
        "category": "billing", "severity": "medium", "object_type": "quote",
        "key_fields": ("id", "customer", "status", "amount_total", "currency"),
    },
    "quote.finalized": {
        "category": "billing", "severity": "medium", "object_type": "quote",
        "key_fields": ("id", "customer", "amount_total", "expires_at"),
    },
    "quote.accepted": {
        "category": "billing", "severity": "high", "object_type": "quote",
        "key_fields": ("id", "customer", "amount_total", "subscription", "invoice"),
    },
    "quote.canceled": {
        "category": "billing", "severity": "medium", "object_type": "quote",
        "key_fields": ("id", "customer", "amount_total"),
    },
    "quote.will_expire": {
        "category": "billing", "severity": "medium", "object_type": "quote",
        "key_fields": ("id", "customer", "expires_at"),
    },

    "credit_note.created": {
        "category": "billing", "severity": "medium", "object_type": "credit_note",
        "key_fields": ("id", "invoice", "customer", "amount", "currency", "reason"),
    },
    "credit_note.updated": {
        "category": "billing", "severity": "low", "object_type": "credit_note",
        "key_fields": ("id", "status"),
    },
    "credit_note.voided": {
        "category": "billing", "severity": "medium", "object_type": "credit_note",
        "key_fields": ("id", "invoice", "customer"),
    },

    "coupon.created": {
        "category": "billing", "severity": "info", "object_type": "coupon",
        "key_fields": ("id", "name", "percent_off", "amount_off", "duration"),
    },
    "coupon.updated": {
        "category": "billing", "severity": "info", "object_type": "coupon",
        "key_fields": ("id", "name"),
    },
    "coupon.deleted": {
        "category": "billing", "severity": "info", "object_type": "coupon",
        "key_fields": ("id", "name"),
    },
    "promotion_code.created": {
        "category": "billing", "severity": "info", "object_type": "promotion_code",
        "key_fields": ("id", "code", "coupon.id", "active"),
    },
    "promotion_code.updated": {
        "category": "billing", "severity": "info", "object_type": "promotion_code",
        "key_fields": ("id", "code", "active"),
    },

    "plan.created": {
        "category": "billing", "severity": "info", "object_type": "plan",
        "key_fields": ("id", "nickname", "amount", "currency", "interval"),
    },
    "plan.updated": {
        "category": "billing", "severity": "info", "object_type": "plan",
        "key_fields": ("id", "active"),
    },
    "plan.deleted": {
        "category": "billing", "severity": "info", "object_type": "plan",
        "key_fields": ("id",),
    },
    "price.created": {
        "category": "billing", "severity": "info", "object_type": "price",
        "key_fields": ("id", "product", "unit_amount", "currency", "recurring.interval"),
    },
    "price.updated": {
        "category": "billing", "severity": "info", "object_type": "price",
        "key_fields": ("id", "active"),
    },
    "price.deleted": {
        "category": "billing", "severity": "info", "object_type": "price",
        "key_fields": ("id",),
    },
    "product.created": {
        "category": "billing", "severity": "info", "object_type": "product",
        "key_fields": ("id", "name", "active"),
    },
    "product.updated": {
        "category": "billing", "severity": "info", "object_type": "product",
        "key_fields": ("id", "name", "active"),
    },
    "product.deleted": {
        "category": "billing", "severity": "info", "object_type": "product",
        "key_fields": ("id", "name"),
    },

    "tax_rate.created": {
        "category": "billing", "severity": "info", "object_type": "tax_rate",
        "key_fields": ("id", "display_name", "percentage", "jurisdiction"),
    },
    "tax_rate.updated": {
        "category": "billing", "severity": "info", "object_type": "tax_rate",
        "key_fields": ("id", "active"),
    },
    "tax.settings.updated": {
        "category": "billing", "severity": "medium", "object_type": "tax.settings",
        "key_fields": ("status", "defaults.tax_behavior"),
    },

    # Billing meters / credits / alerts
    "billing.alert.triggered": {
        "category": "billing", "severity": "high", "object_type": "billing.alert",
        "key_fields": ("id", "alert_type", "value"),
    },
    "billing.credit_balance_transaction.created": {
        "category": "billing", "severity": "medium", "object_type": "billing.credit_balance_transaction",
        "key_fields": ("id", "customer", "type", "amount"),
    },
    "billing.credit_grant.created": {
        "category": "billing", "severity": "medium", "object_type": "billing.credit_grant",
        "key_fields": ("id", "customer", "amount.monetary.value", "amount.monetary.currency"),
    },
    "billing.credit_grant.updated": {
        "category": "billing", "severity": "low", "object_type": "billing.credit_grant",
        "key_fields": ("id", "customer"),
    },
    "billing.meter.created": {
        "category": "billing", "severity": "info", "object_type": "billing.meter",
        "key_fields": ("id", "display_name", "event_name", "status"),
    },
    "billing.meter.updated": {
        "category": "billing", "severity": "info", "object_type": "billing.meter",
        "key_fields": ("id", "status"),
    },
    "billing.meter.deactivated": {
        "category": "billing", "severity": "medium", "object_type": "billing.meter",
        "key_fields": ("id", "display_name"),
    },
    "billing.meter.reactivated": {
        "category": "billing", "severity": "medium", "object_type": "billing.meter",
        "key_fields": ("id", "display_name"),
    },

    "billing_portal.configuration.created": {
        "category": "billing", "severity": "info", "object_type": "billing_portal.configuration",
        "key_fields": ("id", "active", "is_default"),
    },
    "billing_portal.configuration.updated": {
        "category": "billing", "severity": "info", "object_type": "billing_portal.configuration",
        "key_fields": ("id", "active"),
    },
    "billing_portal.session.created": {
        "category": "billing", "severity": "info", "object_type": "billing_portal.session",
        "key_fields": ("id", "customer", "url", "return_url"),
    },

    "entitlements.active_entitlement_summary.updated": {
        "category": "billing", "severity": "medium", "object_type": "entitlements.active_entitlement_summary",
        "key_fields": ("customer", "entitlements.data[].lookup_key"),
    },

    # =========================================================
    # CUSTOMER
    # =========================================================
    "customer.created": {
        "category": "customer", "severity": "medium", "object_type": "customer",
        "key_fields": ("id", "email", "name", "phone", "metadata"),
    },
    "customer.updated": {
        "category": "customer", "severity": "low", "object_type": "customer",
        "key_fields": ("id", "email", "name"),
    },
    "customer.deleted": {
        "category": "customer", "severity": "high", "object_type": "customer",
        "key_fields": ("id", "email"),
    },
    "customer.discount.created": {
        "category": "customer", "severity": "low", "object_type": "discount",
        "key_fields": ("id", "customer", "coupon.id"),
    },
    "customer.discount.updated": {
        "category": "customer", "severity": "low", "object_type": "discount",
        "key_fields": ("id", "customer", "coupon.id"),
    },
    "customer.discount.deleted": {
        "category": "customer", "severity": "low", "object_type": "discount",
        "key_fields": ("id", "customer"),
    },
    "customer.source.created": {
        "category": "customer", "severity": "low", "object_type": "source",
        "key_fields": ("id", "customer", "type", "last4"),
    },
    "customer.source.updated": {
        "category": "customer", "severity": "low", "object_type": "source",
        "key_fields": ("id", "customer", "type"),
    },
    "customer.source.deleted": {
        "category": "customer", "severity": "low", "object_type": "source",
        "key_fields": ("id", "customer", "type"),
    },
    "customer.source.expiring": {
        "category": "customer", "severity": "medium", "object_type": "source",
        "key_fields": ("id", "customer", "exp_month", "exp_year", "last4"),
    },
    "customer.tax_id.created": {
        "category": "customer", "severity": "low", "object_type": "tax_id",
        "key_fields": ("id", "customer", "type", "value"),
    },
    "customer.tax_id.updated": {
        "category": "customer", "severity": "low", "object_type": "tax_id",
        "key_fields": ("id", "customer", "verification.status"),
    },
    "customer.tax_id.deleted": {
        "category": "customer", "severity": "low", "object_type": "tax_id",
        "key_fields": ("id", "customer"),
    },

    "customer_cash_balance_transaction.created": {
        "category": "customer", "severity": "medium", "object_type": "customer_cash_balance_transaction",
        "key_fields": ("id", "customer", "type", "net_amount", "currency"),
    },
    "cash_balance.funds_available": {
        "category": "customer", "severity": "medium", "object_type": "cash_balance",
        "key_fields": ("customer", "available"),
    },

    # =========================================================
    # PAYMENT METHOD / SETUP INTENT / MANDATE / SOURCE
    # =========================================================
    "payment_method.attached": {
        "category": "payment_method", "severity": "medium", "object_type": "payment_method",
        "key_fields": ("id", "customer", "type", "card.brand", "card.last4"),
    },
    "payment_method.detached": {
        "category": "payment_method", "severity": "medium", "object_type": "payment_method",
        "key_fields": ("id", "type"),
    },
    "payment_method.updated": {
        "category": "payment_method", "severity": "low", "object_type": "payment_method",
        "key_fields": ("id", "customer", "type"),
    },
    "payment_method.automatically_updated": {
        "category": "payment_method", "severity": "medium", "object_type": "payment_method",
        "key_fields": ("id", "customer", "card.brand", "card.last4", "card.exp_month", "card.exp_year"),
    },

    "setup_intent.created": {
        "category": "payment_method", "severity": "low", "object_type": "setup_intent",
        "key_fields": ("id", "customer", "status", "usage"),
    },
    "setup_intent.succeeded": {
        "category": "payment_method", "severity": "medium", "object_type": "setup_intent",
        "key_fields": ("id", "customer", "payment_method"),
    },
    "setup_intent.setup_failed": {
        "category": "payment_method", "severity": "critical", "object_type": "setup_intent",
        "key_fields": ("id", "customer", "last_setup_error.code", "last_setup_error.message"),
    },
    "setup_intent.canceled": {
        "category": "payment_method", "severity": "medium", "object_type": "setup_intent",
        "key_fields": ("id", "customer", "cancellation_reason"),
    },
    "setup_intent.requires_action": {
        "category": "payment_method", "severity": "medium", "object_type": "setup_intent",
        "key_fields": ("id", "customer", "next_action.type"),
    },

    "mandate.updated": {
        "category": "payment_method", "severity": "medium", "object_type": "mandate",
        "key_fields": ("id", "status", "payment_method", "type"),
    },

    "source.canceled": {
        "category": "payment_method", "severity": "medium", "object_type": "source",
        "key_fields": ("id", "type", "status"),
    },
    "source.chargeable": {
        "category": "payment_method", "severity": "medium", "object_type": "source",
        "key_fields": ("id", "type", "amount", "currency"),
    },
    "source.failed": {
        "category": "payment_method", "severity": "critical", "object_type": "source",
        "key_fields": ("id", "type", "status", "failure_reason"),
    },
    "source.mandate_notification": {
        "category": "payment_method", "severity": "medium", "object_type": "source_mandate_notification",
        "key_fields": ("id", "source.id", "type", "reason"),
    },
    "source.refund_attributes_required": {
        "category": "payment_method", "severity": "high", "object_type": "source",
        "key_fields": ("id", "type", "amount"),
    },
    "source.transaction.created": {
        "category": "payment_method", "severity": "medium", "object_type": "source_transaction",
        "key_fields": ("id", "source", "amount", "currency", "type"),
    },
    "source.transaction.updated": {
        "category": "payment_method", "severity": "low", "object_type": "source_transaction",
        "key_fields": ("id", "source", "status"),
    },

    # =========================================================
    # PAYOUT / TRANSFER / TOPUP / BALANCE / RESERVE
    # =========================================================
    "payout.created": {
        "category": "payout_treasury", "severity": "medium", "object_type": "payout",
        "key_fields": ("id", "amount", "currency", "arrival_date", "status", "destination"),
    },
    "payout.paid": {
        "category": "payout_treasury", "severity": "high", "object_type": "payout",
        "key_fields": ("id", "amount", "currency", "arrival_date"),
    },
    "payout.failed": {
        "category": "payout_treasury", "severity": "critical", "object_type": "payout",
        "key_fields": ("id", "amount", "currency", "failure_code", "failure_message"),
    },
    "payout.canceled": {
        "category": "payout_treasury", "severity": "high", "object_type": "payout",
        "key_fields": ("id", "amount", "currency"),
    },
    "payout.updated": {
        "category": "payout_treasury", "severity": "low", "object_type": "payout",
        "key_fields": ("id", "status", "amount"),
    },
    "payout.reconciliation_completed": {
        "category": "payout_treasury", "severity": "medium", "object_type": "payout",
        "key_fields": ("id", "amount", "currency", "reconciliation_status"),
    },

    "transfer.created": {
        "category": "payout_treasury", "severity": "high", "object_type": "transfer",
        "key_fields": ("id", "amount", "currency", "destination", "source_transaction"),
    },
    "transfer.updated": {
        "category": "payout_treasury", "severity": "low", "object_type": "transfer",
        "key_fields": ("id", "amount", "destination"),
    },
    "transfer.reversed": {
        "category": "payout_treasury", "severity": "high", "object_type": "transfer",
        "key_fields": ("id", "amount", "amount_reversed", "destination"),
    },

    "topup.created": {
        "category": "payout_treasury", "severity": "medium", "object_type": "topup",
        "key_fields": ("id", "amount", "currency", "status"),
    },
    "topup.succeeded": {
        "category": "payout_treasury", "severity": "high", "object_type": "topup",
        "key_fields": ("id", "amount", "currency"),
    },
    "topup.failed": {
        "category": "payout_treasury", "severity": "critical", "object_type": "topup",
        "key_fields": ("id", "amount", "failure_code", "failure_message"),
    },
    "topup.canceled": {
        "category": "payout_treasury", "severity": "medium", "object_type": "topup",
        "key_fields": ("id", "amount"),
    },
    "topup.reversed": {
        "category": "payout_treasury", "severity": "high", "object_type": "topup",
        "key_fields": ("id", "amount", "amount_reversed"),
    },

    "balance.available": {
        "category": "payout_treasury", "severity": "low", "object_type": "balance",
        "key_fields": ("available", "pending"),
    },
    "balance_settings.updated": {
        "category": "payout_treasury", "severity": "medium", "object_type": "balance_settings",
        "key_fields": ("payouts.schedule.interval",),
    },

    "reserve.hold.created": {
        "category": "payout_treasury", "severity": "high", "object_type": "reserve.hold",
        "key_fields": ("id", "amount", "currency", "reason"),
    },
    "reserve.hold.updated": {
        "category": "payout_treasury", "severity": "medium", "object_type": "reserve.hold",
        "key_fields": ("id", "amount", "status"),
    },
    "reserve.plan.created": {
        "category": "payout_treasury", "severity": "high", "object_type": "reserve.plan",
        "key_fields": ("id", "status"),
    },
    "reserve.plan.updated": {
        "category": "payout_treasury", "severity": "medium", "object_type": "reserve.plan",
        "key_fields": ("id", "status"),
    },
    "reserve.plan.disabled": {
        "category": "payout_treasury", "severity": "high", "object_type": "reserve.plan",
        "key_fields": ("id",),
    },
    "reserve.plan.expired": {
        "category": "payout_treasury", "severity": "medium", "object_type": "reserve.plan",
        "key_fields": ("id",),
    },
    "reserve.release.created": {
        "category": "payout_treasury", "severity": "medium", "object_type": "reserve.release",
        "key_fields": ("id", "amount", "currency"),
    },

    # =========================================================
    # CONNECT (account / person / capability / external_account / application_fee)
    # =========================================================
    "account.updated": {
        "category": "connect", "severity": "medium", "object_type": "account",
        "key_fields": ("id", "charges_enabled", "payouts_enabled",
                       "requirements.disabled_reason", "requirements.currently_due"),
    },
    "account.application.authorized": {
        "category": "connect", "severity": "high", "object_type": "application",
        "key_fields": ("id", "name"),
    },
    "account.application.deauthorized": {
        "category": "connect", "severity": "critical", "object_type": "application",
        "key_fields": ("id", "name"),
    },
    "account.external_account.created": {
        "category": "connect", "severity": "medium", "object_type": "external_account",
        "key_fields": ("id", "account", "object", "last4", "currency"),
    },
    "account.external_account.updated": {
        "category": "connect", "severity": "low", "object_type": "external_account",
        "key_fields": ("id", "account", "status"),
    },
    "account.external_account.deleted": {
        "category": "connect", "severity": "medium", "object_type": "external_account",
        "key_fields": ("id", "account"),
    },

    "capability.updated": {
        "category": "connect", "severity": "medium", "object_type": "capability",
        "key_fields": ("id", "account", "status", "requirements.disabled_reason"),
    },

    "person.created": {
        "category": "connect", "severity": "medium", "object_type": "person",
        "key_fields": ("id", "account", "relationship.representative", "requirements.currently_due"),
    },
    "person.updated": {
        "category": "connect", "severity": "low", "object_type": "person",
        "key_fields": ("id", "account", "verification.status"),
    },
    "person.deleted": {
        "category": "connect", "severity": "medium", "object_type": "person",
        "key_fields": ("id", "account"),
    },

    "application_fee.created": {
        "category": "connect", "severity": "medium", "object_type": "application_fee",
        "key_fields": ("id", "amount", "currency", "charge", "account"),
    },
    "application_fee.refunded": {
        "category": "connect", "severity": "medium", "object_type": "application_fee",
        "key_fields": ("id", "amount", "amount_refunded", "charge"),
    },
    "application_fee.refund.updated": {
        "category": "connect", "severity": "low", "object_type": "fee_refund",
        "key_fields": ("id", "fee", "amount"),
    },

    # =========================================================
    # IDENTITY
    # =========================================================
    "identity.verification_session.created": {
        "category": "identity", "severity": "low", "object_type": "identity.verification_session",
        "key_fields": ("id", "type", "status", "client_secret"),
    },
    "identity.verification_session.processing": {
        "category": "identity", "severity": "low", "object_type": "identity.verification_session",
        "key_fields": ("id", "type", "status"),
    },
    "identity.verification_session.requires_input": {
        "category": "identity", "severity": "medium", "object_type": "identity.verification_session",
        "key_fields": ("id", "last_error.code", "last_error.reason"),
    },
    "identity.verification_session.verified": {
        "category": "identity", "severity": "high", "object_type": "identity.verification_session",
        "key_fields": ("id", "type", "verified_outputs"),
    },
    "identity.verification_session.canceled": {
        "category": "identity", "severity": "medium", "object_type": "identity.verification_session",
        "key_fields": ("id", "type"),
    },
    "identity.verification_session.redacted": {
        "category": "identity", "severity": "medium", "object_type": "identity.verification_session",
        "key_fields": ("id",),
    },

    # =========================================================
    # FINANCIAL CONNECTIONS
    # =========================================================
    "financial_connections.account.created": {
        "category": "financial_connections", "severity": "medium", "object_type": "financial_connections.account",
        "key_fields": ("id", "institution_name", "category", "status"),
    },
    "financial_connections.account.account_numbers_updated": {
        "category": "financial_connections", "severity": "medium", "object_type": "financial_connections.account",
        "key_fields": ("id", "institution_name"),
    },
    "financial_connections.account.deactivated": {
        "category": "financial_connections", "severity": "high", "object_type": "financial_connections.account",
        "key_fields": ("id", "institution_name", "status"),
    },
    "financial_connections.account.disconnected": {
        "category": "financial_connections", "severity": "high", "object_type": "financial_connections.account",
        "key_fields": ("id", "institution_name"),
    },
    "financial_connections.account.reactivated": {
        "category": "financial_connections", "severity": "medium", "object_type": "financial_connections.account",
        "key_fields": ("id", "institution_name"),
    },
    "financial_connections.account.refreshed_balance": {
        "category": "financial_connections", "severity": "low", "object_type": "financial_connections.account",
        "key_fields": ("id", "balance_refresh.status"),
    },
    "financial_connections.account.refreshed_ownership": {
        "category": "financial_connections", "severity": "low", "object_type": "financial_connections.account",
        "key_fields": ("id", "ownership_refresh.status"),
    },
    "financial_connections.account.refreshed_transactions": {
        "category": "financial_connections", "severity": "low", "object_type": "financial_connections.account",
        "key_fields": ("id", "transaction_refresh.status"),
    },
    "financial_connections.account.upcoming_account_number_expiry": {
        "category": "financial_connections", "severity": "medium", "object_type": "financial_connections.account",
        "key_fields": ("id", "institution_name"),
    },

    # =========================================================
    # ISSUING
    # =========================================================
    "issuing_authorization.created": {
        "category": "issuing", "severity": "high", "object_type": "issuing.authorization",
        "key_fields": ("id", "amount", "currency", "card", "merchant_data.name", "status"),
    },
    "issuing_authorization.request": {
        "category": "issuing", "severity": "critical", "object_type": "issuing.authorization",
        "key_fields": ("id", "amount", "currency", "card", "merchant_data.name", "pending_request.amount"),
    },
    "issuing_authorization.updated": {
        "category": "issuing", "severity": "low", "object_type": "issuing.authorization",
        "key_fields": ("id", "status", "amount"),
    },
    "issuing_card.created": {
        "category": "issuing", "severity": "medium", "object_type": "issuing.card",
        "key_fields": ("id", "cardholder", "type", "status", "last4"),
    },
    "issuing_card.updated": {
        "category": "issuing", "severity": "low", "object_type": "issuing.card",
        "key_fields": ("id", "status"),
    },
    "issuing_cardholder.created": {
        "category": "issuing", "severity": "medium", "object_type": "issuing.cardholder",
        "key_fields": ("id", "name", "email", "status", "type"),
    },
    "issuing_cardholder.updated": {
        "category": "issuing", "severity": "low", "object_type": "issuing.cardholder",
        "key_fields": ("id", "status", "requirements.disabled_reason"),
    },
    "issuing_dispute.created": {
        "category": "issuing", "severity": "high", "object_type": "issuing.dispute",
        "key_fields": ("id", "amount", "currency", "transaction", "status", "reason"),
    },
    "issuing_dispute.submitted": {
        "category": "issuing", "severity": "high", "object_type": "issuing.dispute",
        "key_fields": ("id", "amount", "transaction", "reason"),
    },
    "issuing_dispute.closed": {
        "category": "issuing", "severity": "medium", "object_type": "issuing.dispute",
        "key_fields": ("id", "status", "amount"),
    },
    "issuing_dispute.updated": {
        "category": "issuing", "severity": "low", "object_type": "issuing.dispute",
        "key_fields": ("id", "status"),
    },
    "issuing_dispute.funds_reinstated": {
        "category": "issuing", "severity": "high", "object_type": "issuing.dispute",
        "key_fields": ("id", "amount", "currency"),
    },
    "issuing_dispute.funds_rescinded": {
        "category": "issuing", "severity": "critical", "object_type": "issuing.dispute",
        "key_fields": ("id", "amount", "currency"),
    },
    "issuing_personalization_design.activated": {
        "category": "issuing", "severity": "medium", "object_type": "issuing.personalization_design",
        "key_fields": ("id", "status", "name"),
    },
    "issuing_personalization_design.deactivated": {
        "category": "issuing", "severity": "medium", "object_type": "issuing.personalization_design",
        "key_fields": ("id", "name"),
    },
    "issuing_personalization_design.rejected": {
        "category": "issuing", "severity": "high", "object_type": "issuing.personalization_design",
        "key_fields": ("id", "rejection_reasons"),
    },
    "issuing_personalization_design.updated": {
        "category": "issuing", "severity": "low", "object_type": "issuing.personalization_design",
        "key_fields": ("id", "status"),
    },
    "issuing_token.created": {
        "category": "issuing", "severity": "medium", "object_type": "issuing.token",
        "key_fields": ("id", "card", "status", "wallet_provider"),
    },
    "issuing_token.updated": {
        "category": "issuing", "severity": "low", "object_type": "issuing.token",
        "key_fields": ("id", "status"),
    },
    "issuing_transaction.created": {
        "category": "issuing", "severity": "high", "object_type": "issuing.transaction",
        "key_fields": ("id", "amount", "currency", "card", "merchant_data.name", "type"),
    },
    "issuing_transaction.updated": {
        "category": "issuing", "severity": "low", "object_type": "issuing.transaction",
        "key_fields": ("id", "amount"),
    },
    "issuing_transaction.purchase_details_receipt_updated": {
        "category": "issuing", "severity": "low", "object_type": "issuing.transaction",
        "key_fields": ("id", "purchase_details.receipt"),
    },

    # =========================================================
    # TERMINAL
    # =========================================================
    "terminal.reader.action_succeeded": {
        "category": "terminal", "severity": "high", "object_type": "terminal.reader",
        "key_fields": ("id", "action.type", "action.status"),
    },
    "terminal.reader.action_failed": {
        "category": "terminal", "severity": "critical", "object_type": "terminal.reader",
        "key_fields": ("id", "action.type", "action.failure_code", "action.failure_message"),
    },
    "terminal.reader.action_updated": {
        "category": "terminal", "severity": "low", "object_type": "terminal.reader",
        "key_fields": ("id", "action.status", "action.type"),
    },

    # =========================================================
    # CLIMATE
    # =========================================================
    "climate.order.created": {
        "category": "climate", "severity": "medium", "object_type": "climate.order",
        "key_fields": ("id", "amount_total", "currency", "metric_tons"),
    },
    "climate.order.canceled": {
        "category": "climate", "severity": "medium", "object_type": "climate.order",
        "key_fields": ("id", "amount_total", "cancellation_reason"),
    },
    "climate.order.delayed": {
        "category": "climate", "severity": "medium", "object_type": "climate.order",
        "key_fields": ("id", "expected_delivery_year"),
    },
    "climate.order.delivered": {
        "category": "climate", "severity": "high", "object_type": "climate.order",
        "key_fields": ("id", "delivered_at", "metric_tons"),
    },
    "climate.order.product_substituted": {
        "category": "climate", "severity": "medium", "object_type": "climate.order",
        "key_fields": ("id", "product"),
    },
    "climate.product.created": {
        "category": "climate", "severity": "info", "object_type": "climate.product",
        "key_fields": ("id", "name"),
    },
    "climate.product.pricing_updated": {
        "category": "climate", "severity": "info", "object_type": "climate.product",
        "key_fields": ("id", "current_prices_per_metric_ton"),
    },

    # =========================================================
    # OPERATIONS (file / reporting / sigma)
    # =========================================================
    "file.created": {
        "category": "operations", "severity": "info", "object_type": "file",
        "key_fields": ("id", "filename", "purpose", "size"),
    },
    "reporting.report_run.succeeded": {
        "category": "operations", "severity": "info", "object_type": "reporting.report_run",
        "key_fields": ("id", "report_type", "status", "result.url"),
    },
    "reporting.report_run.failed": {
        "category": "operations", "severity": "high", "object_type": "reporting.report_run",
        "key_fields": ("id", "report_type", "error"),
    },
    "reporting.report_type.updated": {
        "category": "operations", "severity": "info", "object_type": "reporting.report_type",
        "key_fields": ("id", "name", "version"),
    },
    "sigma.scheduled_query_run.created": {
        "category": "operations", "severity": "info", "object_type": "scheduled_query_run",
        "key_fields": ("id", "status", "sql", "result_available_until"),
    },

    # =========================================================
    # TEST HELPERS (mode test uniquement)
    # =========================================================
    "test_helpers.test_clock.created": {
        "category": "test", "severity": "info", "object_type": "test_helpers.test_clock",
        "key_fields": ("id", "frozen_time", "status"),
    },
    "test_helpers.test_clock.advancing": {
        "category": "test", "severity": "info", "object_type": "test_helpers.test_clock",
        "key_fields": ("id", "frozen_time"),
    },
    "test_helpers.test_clock.ready": {
        "category": "test", "severity": "info", "object_type": "test_helpers.test_clock",
        "key_fields": ("id", "frozen_time"),
    },
    "test_helpers.test_clock.internal_failure": {
        "category": "test", "severity": "medium", "object_type": "test_helpers.test_clock",
        "key_fields": ("id", "status"),
    },
    "test_helpers.test_clock.deleted": {
        "category": "test", "severity": "info", "object_type": "test_helpers.test_clock",
        "key_fields": ("id",),
    },
}
