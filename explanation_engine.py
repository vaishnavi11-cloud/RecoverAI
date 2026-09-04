def explain_decision(payment, action):

    reason = payment["failure_reason"]
    retry_count = payment["retry_count"]
    history = payment["customer_history"]
    previous_payments = payment["previous_successful_payments"]

    if action == "RETRY_PAYMENT":
        return (
            f"The payment failed because of {reason}. "
            f"This is treated as a temporary issue, and the payment has only "
            f"been retried {retry_count} time(s). "
            f"Therefore, RecoverAI chose to retry the payment."
        )

    elif action == "SEND_PAYMENT_LINK":
        return (
            f"The payment failed because of insufficient funds. "
            f"The customer has a {history} payment history and "
            f"{previous_payments} previous successful payment(s). "
            f"This indicates a reasonable chance of payment later, "
            f"so RecoverAI chose to send a payment link."
        )

    elif action == "OFFER_ALTERNATIVE_METHOD":
        return (
            f"The card was declined, but the customer has a good payment history "
            f"and the retry limit has not been exceeded. "
            f"Therefore, RecoverAI chose to offer an alternative payment method."
        )

    else:
        return (
            f"RecoverAI decided to stop further recovery attempts because the "
            f"payment context does not meet the conditions for another recovery action. "
            f"Failure reason: {reason}, retry count: {retry_count}, "
            f"customer history: {history}."
        )
def calculate_confidence(payment, action):

    score = 50

    history = payment["customer_history"]
    previous_payments = payment["previous_successful_payments"]
    retry_count = payment["retry_count"]

    if history == "good":
        score += 20

    elif history == "average":
        score += 10

    if previous_payments >= 10:
        score += 15

    elif previous_payments >= 5:
        score += 10

    if retry_count < 2:
        score += 10

    if action == "STOP":
        score -= 10

    return min(score, 95)

def get_confidence_factors(payment, action):

    factors = [
        ("Base decision confidence", 50)
    ]

    history = payment["customer_history"]
    previous_payments = payment["previous_successful_payments"]
    retry_count = payment["retry_count"]

    if history == "good":
        factors.append(
            ("Good customer history", 20)
        )

    elif history == "average":
        factors.append(
            ("Average customer history", 10)
        )

    if previous_payments >= 10:
        factors.append(
            ("10+ previous successful payments", 15)
        )

    elif previous_payments >= 5:
        factors.append(
            ("5+ previous successful payments", 10)
        )

    if retry_count < 2:
        factors.append(
            ("Retry limit not reached", 10)
        )

    if action == "STOP":
        factors.append(
            ("Low recovery opportunity", -10)
        )

    return factors
def get_decision_rule(payment, action):

    reason = payment["failure_reason"]
    retry_count = payment["retry_count"]
    history = payment["customer_history"]
    previous_payments = payment["previous_successful_payments"]

    if action == "RETRY_PAYMENT":

        if reason == "network_error":
            return (
                "Rule: Network errors are treated as temporary failures. "
                "Retry the payment when retry count is below 2."
            )

        elif reason == "bank_error":
            return (
                "Rule: Bank errors may be temporary. "
                "Retry the payment when retry count is below 2."
            )

    elif action == "SEND_PAYMENT_LINK":

        return (
            "Rule: For insufficient funds, send a payment link when "
            "the customer has good history or at least 5 previous successful payments."
        )

    elif action == "OFFER_ALTERNATIVE_METHOD":

        return (
            "Rule: For a declined card, offer an alternative payment method "
            "to good customers when retry count is below 2."
        )

    elif action == "STOP":

        return (
            "Rule: Stop recovery when the customer does not meet "
            "the conditions for another recovery attempt."
        )

    return "No specific decision rule found."
def calculate_priority(payment):

    amount = payment["amount"]
    history = payment["customer_history"]
    previous_payments = payment["previous_successful_payments"]

    score = 0

    # Higher-value payments get more attention
    if amount >= 8000:
        score += 40

    elif amount >= 5000:
        score += 25

    else:
        score += 10

    # Reliable customers get higher priority
    if history == "good":
        score += 30

    elif history == "average":
        score += 15

    # Customers with successful history are valuable
    if previous_payments >= 10:
        score += 20

    elif previous_payments >= 5:
        score += 10

    return score