import random


failure_reasons = [
    "network_error",
    "insufficient_funds",
    "card_declined",
    "bank_error"
]

customer_histories = [
    "good",
    "average",
    "poor"
]


def generate_payment(payment_number):

    customer_history = random.choice(customer_histories)

    if customer_history == "good":
        previous_successful_payments = random.randint(5, 20)

    elif customer_history == "average":
        previous_successful_payments = random.randint(1, 5)

    else:
        previous_successful_payments = random.randint(0, 1)

    payment = {
        "payment_id": f"PAY{payment_number:03}",
        "amount": random.randint(100, 10000),
        "failure_reason": random.choice(failure_reasons),
        "retry_count": random.randint(0, 2),
        "status": "failed",
        "customer_history": customer_history,
        "previous_successful_payments": previous_successful_payments
    }

    return payment


if __name__ == "__main__":
    for i in range(1, 11):
        payment = generate_payment(i)
        print(payment)