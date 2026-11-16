import json
import random
import uuid
from datetime import UTC, datetime
from pathlib import Path

from faker import Faker

fake = Faker()

OUTPUT_DIR = Path("data/landing")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

CHANNELS = ["MOBILE_APP", "WEB_PORTAL", "POS_TERMINAL", "ATM"]
CURRENCIES = ["EUR", "USD", "GBP", "CAD", "INR"]
TXN_TYPES = ["PURCHASE", "TRANSFER", "WITHDRAWAL", "REFUND"]

def generate_record(record_type="valid"):
    txn_id = str(uuid.uuid4())
    account_id = f"ACC-{random.randint(10000, 99999)}"
    timestamp = datetime.now(UTC).isoformat()

    if record_type == "valid":
        return {
            "transaction_id": txn_id,
            "account_id": account_id,
            "user_id": f"USR-{random.randint(1000, 4000)}",
            "amount": round(random.uniform(5.0, 3500.0), 2),
            "currency": random.choice(CURRENCIES),
            "txn_type": random.choice(TXN_TYPES),
            "channel": random.choice(CHANNELS),
            "merchant_category": fake.bs(),
            "location_country": fake.country_code(),
            "event_timestamp": timestamp,
            "is_suspicious_flag": False
        }

    elif record_type == "fraud_candidate":
        # Sudden spike or high-risk withdrawal
        return {
            "transaction_id": txn_id,
            "account_id": account_id,
            "user_id": f"USR-{random.randint(1000, 4000)}",
            "amount": round(random.uniform(9500.0, 50000.0), 2),
            "currency": random.choice(CURRENCIES),
            "txn_type": "TRANSFER",
            "channel": "MOBILE_APP",
            "merchant_category": "Cryptocurrency Exchange",
            "location_country": "KY",  # Cayman Islands
            "event_timestamp": timestamp,
            "is_suspicious_flag": True
        }

    elif record_type == "poison_pill":
        # Missing critical keys, invalid types, or malformed schema
        bad_types = [
            {"transaction_id": None, "account_id": account_id, "amount": "INVALID_AMOUNT"},
            {"txn_id_broken": txn_id, "amount": -9999.00, "channel": 12345},
            {"transaction_id": txn_id, "account_id": account_id, "amount": None, "malformed": True}
        ]
        corrupted = random.choice(bad_types)
        corrupted["event_timestamp"] = timestamp
        return corrupted


def generate_batch(batch_id: int, total_records: int = 500):
    records = []
    for _ in range(total_records):
        rand = random.random()
        if rand < 0.85:
            records.append(generate_record("valid"))
        elif rand < 0.95:
            records.append(generate_record("fraud_candidate"))
        else:
            records.append(generate_record("poison_pill"))

    filename = OUTPUT_DIR / f"transactions_batch_{batch_id}_{int(datetime.now().timestamp())}.json"
    with open(filename, "w") as f:
        f.writelines(json.dumps(rec) + "\n" for rec in records)
    print(f"Generated {total_records} records to {filename}")


if __name__ == "__main__":
    for b in range(1, 4):
        generate_batch(batch_id=b, total_records=300)