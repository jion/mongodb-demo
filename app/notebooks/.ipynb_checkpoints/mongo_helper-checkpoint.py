import json
import time
from pymongo import MongoClient, UpdateOne

# Connect to MongoDB
client = MongoClient('mongodb://mongodb:27017/')
db = client.demo

def load_jsonl(file_path):
    """Load JSON lines from a file."""
    with open(file_path, 'r') as file:
        for line in file:
            yield json.loads(line)

def insert_separate_entities(file_path):
    """Insert data into separate collections."""
    customers, addresses, payments, subscriptions = [], [], [], []

    for record in load_jsonl(file_path):
        customer = record["customer"]
        customer["merchant_user_id"] = customer.pop("merchant_user_id")
        customers.append(customer)

        for address in record["addresses"]:
            addresses.append(address)

        for payment in record["payments"]:
            payments.append(payment)

        for subscription in record["subscriptions"]:
            subscriptions.append(subscription)

    start_time = time.time()
    db.customers.insert_many(customers)
    db.addresses.insert_many(addresses)
    db.payments.insert_many(payments)
    db.subscriptions.insert_many(subscriptions)
    end_time = time.time()

    print("Separate Entities Write Time:", end_time - start_time)

def insert_embedded_model(file_path):
    """Insert data into a single collection with embedded documents."""
    embedded_customers = []

    for record in load_jsonl(file_path):
        customer = record["customer"]
        customer["addresses"] = record["addresses"]
        customer["payments"] = record["payments"]
        customer["subscriptions"] = record["subscriptions"]
        embedded_customers.append(customer)

    start_time = time.time()
    db.embedded_customers.insert_many(embedded_customers)
    end_time = time.time()

    print("Embedded Model Write Time:", end_time - start_time)

def query_separate_entities(merchant_user_id):
    """Query data from separate collections."""
    start_time = time.time()
    subscriptions = db.subscriptions.find({"customer": merchant_user_id})
    for sub in subscriptions:
        customer = db.customers.find_one({"merchant_user_id": sub['customer']})
        address = db.addresses.find_one({"customer": sub['customer'], "address_type": "shipping_address"})
        payment = db.payments.find_one({"customer": sub['customer']})
        print(sub, customer, address, payment)
    end_time = time.time()

    print("Separate Entities Read Time:", end_time - start_time)

def query_embedded_model(merchant_user_id):
    """Query data from the embedded model."""
    start_time = time.time()
    embedded_customers = db.embedded_customers.find({"subscriptions.customer": merchant_user_id})
    for customer in embedded_customers:
        for subscription in customer['subscriptions']:
            print(subscription, customer['first_name'], customer['last_name'])
    end_time = time.time()

    print("Embedded Model Read Time:", end_time - start_time)

def update_separate_entities(file_path):
    """Update data in separate collections."""
    updated_customers, updated_subscriptions = [], []

    for record in load_jsonl(file_path):
        updated_customers.append(record["customer"])
        updated_subscriptions.extend(record["subscriptions"])

    start_time = time.time()
    db.customers.bulk_write([UpdateOne({"merchant_user_id": doc["merchant_user_id"]}, {"$set": doc}) for doc in updated_customers])
    db.subscriptions.bulk_write([UpdateOne({"customer": doc["customer"], "merchant_order_id": doc["merchant_order_id"]}, {"$set": doc}) for doc in updated_subscriptions])
    end_time = time.time()

    print("Separate Entities Update Time:", end_time - start_time)

def update_embedded_model(file_path):
    """Update data in the embedded model."""
    updated_embedded_customers = []

    for record in load_jsonl(file_path):
        customer = record["customer"]
        customer["addresses"] = record["addresses"]
        customer["payments"] = record["payments"]
        customer["subscriptions"] = record["subscriptions"]
        updated_embedded_customers.append(customer)

    start_time = time.time()
    db.embedded_customers.bulk_write([UpdateOne({"merchant_user_id": doc["merchant_user_id"]}, {"$set": doc}) for doc in updated_embedded_customers])
    end_time = time.time()

    print("Embedded Model Update Time:", end_time - start_time)