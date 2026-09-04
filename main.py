from generator import generate_payment
from decision_engine import decide_action
from recovery_executor import execute_recovery
from audit import create_audit_record, save_audit_records


def run_recovery_simulation():
    total_recovered = 0
    audit_records = []

    for i in range(1, 11):
        payment = generate_payment(i)

        action = decide_action(payment)

        recovery = execute_recovery(payment, action)

        total_recovered += recovery["recovered_amount"]

        record = create_audit_record(
            payment,
            action,
            recovery
        )

        audit_records.append(record)

    save_audit_records(audit_records)

    return audit_records, total_recovered


if __name__ == "__main__":
    records, total = run_recovery_simulation()

    print("TOTAL REVENUE RECOVERED: Rs.", total)