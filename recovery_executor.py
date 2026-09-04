import random


def calculate_success_probability(payment, action):

    # Base probability based on recovery action
    if action == "RETRY_PAYMENT":
        probability = 0.60

    elif action == "SEND_PAYMENT_LINK":
        probability = 0.45

    elif action == "OFFER_ALTERNATIVE_METHOD":
        probability = 0.55

    else:
        return 0.0

    # Customer history adjustment
    if payment["customer_history"] == "good":
        probability += 0.15

    elif payment["customer_history"] == "average":
        probability += 0.05

    else:
        probability -= 0.05

    # Previous successful payments
    previous = payment["previous_successful_payments"]

    if previous >= 10:
        probability += 0.10

    elif previous >= 5:
        probability += 0.05

    # Retry count adjustment
    retry_count = payment["retry_count"]

    if retry_count == 0:
        probability += 0.05

    elif retry_count >= 2:
        probability -= 0.10

    # Failure reason adjustment
    reason = payment["failure_reason"]

    if reason == "network_error":
        probability += 0.10

    elif reason == "bank_error":
        probability += 0.05

    elif reason == "card_declined":
        probability -= 0.05

    elif reason == "insufficient_funds":
        probability -= 0.10

    # Keep probability realistic
    probability = max(0.05, min(probability, 0.95))

    return probability


def execute_recovery(payment, action):

    success_probability = calculate_success_probability(
        payment,
        action
    )

    success = random.random() < success_probability

    if success:
        recovered_amount = payment["amount"]
        result = "SUCCESS"

    else:
        recovered_amount = 0
        result = "FAILED"

    return {
        "result": result,
        "recovered_amount": recovered_amount,
        "success_probability": success_probability
    }