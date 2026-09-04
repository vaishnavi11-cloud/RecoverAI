def decide_action(payment):
    reason = payment["failure_reason"]
    retry_count = payment["retry_count"]
    history = payment["customer_history"]
    previous_payments = payment["previous_successful_payments"]

    # Temporary technical failure
    if reason == "network_error" and retry_count < 2:
        return "RETRY_PAYMENT"

    # Bank-side temporary issue
    elif reason == "bank_error" and retry_count < 2:
        return "RETRY_PAYMENT"

    # Customer may pay later
    elif reason == "insufficient_funds":
        if history == "good" or previous_payments >= 5:
            return "SEND_PAYMENT_LINK"
        else:
            return "STOP"

    # Declined card: offer another method to good customers
    elif reason == "card_declined":
        if history == "good" and retry_count < 2:
            return "OFFER_ALTERNATIVE_METHOD"
        else:
            return "STOP"

    else:
        return "STOP"
def get_decision_rule(payment, action):

    reason = payment["failure_reason"]
    retry_count = payment["retry_count"]
    history = payment["customer_history"]
    previous_payments = payment["previous_successful_payments"]

    if action == "RETRY_PAYMENT":
        return (
            f"Rule applied: {reason} is treated as a temporary issue, "
            f"and retry count ({retry_count}) is below the maximum limit of 2."
        )

    elif action == "SEND_PAYMENT_LINK":
        return (
            f"Rule applied: The payment failed due to insufficient funds, "
            f"and the customer has {history} history with "
            f"{previous_payments} previous successful payments."
        )

    elif action == "OFFER_ALTERNATIVE_METHOD":
        return (
            "Rule applied: The card was declined, but the customer has "
            "a good payment history and the retry limit has not been reached."
        )

    else:
        return (
            "Rule applied: The payment does not satisfy the conditions "
            "for another recovery action, so RecoverAI stops recovery."
        )