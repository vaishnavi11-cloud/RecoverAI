import json


def create_audit_record(payment, action, recovery):
    return {
        "payment_id": payment["payment_id"],
        "amount": payment["amount"],
        "failure_reason": payment["failure_reason"],
        "retry_count": payment["retry_count"],
        "customer_history": payment["customer_history"],
        "previous_successful_payments": payment["previous_successful_payments"],
        "action": action,
        "result": recovery["result"],
        "recovered_amount": recovery["recovered_amount"],
        "success_probability": recovery["success_probability"]
    }


def save_audit_records(records):
    with open("audit_log.json", "w") as file:
        json.dump(records, file, indent=4)