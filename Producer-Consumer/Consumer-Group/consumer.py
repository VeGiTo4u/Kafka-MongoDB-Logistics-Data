from confluent_kafka import DeserializingConsumer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroDeserializer
from confluent_kafka.serialization import StringDeserializer
from pymongo import MongoClient
import certifi

# -----------------------------
# Helper function to get latest schema
# -----------------------------
def get_latest_schema(schema_registry_client: SchemaRegistryClient, subject_name: str) -> str:
    schema_obj = schema_registry_client.get_latest_version(subject_name)
    return schema_obj.schema.schema_str

# -----------------------------
# Kafka Consumer Config
# -----------------------------
consumer_conf = {
    "bootstrap.servers": "pkc-l7pr2.ap-south-1.aws.confluent.cloud:9092",
    "security.protocol": "SASL_SSL",
    "sasl.mechanism": "PLAIN",
    "sasl.username": "FZBOYWFTQJJYEYJI",
    "sasl.password": "cflt4KkUeQ62wf1l7oaBSPGhtqCBJEbL+/86rxNNj65ZWXCGIQQus+X00dX3HX8g",
    "group.id": "logistics-consumer-group",
    "auto.offset.reset": "earliest",
}

# -----------------------------
# Schema Registry
# -----------------------------
schema_registry_conf = {
    "url": "https://psrc-4x6n5v3.us-east-2.aws.confluent.cloud",
    "basic.auth.user.info": "{}:{}".format(
        'YRJSAGLV5HKBBJPU',
        'cflt5FVT4wFd9i7ZKooNdRx+oY8QUu/cK/WjMzRaxJakfzS2PLafGu8A6Sm/xTrg'
    )
}

schema_registry_client = SchemaRegistryClient(schema_registry_conf)

# -----------------------------
# Deserializers
# -----------------------------
key_deserializer = StringDeserializer('utf_8')
value_schema = get_latest_schema(schema_registry_client, "logistics_data-value")
value_deserializer = AvroDeserializer(schema_registry_client, value_schema)

consumer_conf["key.deserializer"] = key_deserializer
consumer_conf["value.deserializer"] = value_deserializer

consumer = DeserializingConsumer(consumer_conf)
consumer.subscribe(["logistics_data"])

# -----------------------------
# MongoDB Connection with SSL fix for Mac
# -----------------------------
mongo_client = MongoClient(
    "mongodb+srv://Krrish4u:cmJSVGFnl82p7rcb@logistic-data-cluster.mdvxkjn.mongodb.net/?retryWrites=true&w=majority",
    tlsCAFile=certifi.where()
)
db = mongo_client["logistic_db"]
collection = db["logistic_data"]

# -----------------------------
# Validation / Cleaning Function
# -----------------------------
def validate_and_clean(record):
    if not record.get("booking_id") or record["booking_id"] in ["", "NULL", "NA"]:
        return None
    if not record.get("customer_id") or record["customer_id"] in ["", "NULL", "NA"]:
        return None
    if not record.get("supplier_id") or record["supplier_id"] in ["", "NULL", "NA"]:
        return None

    # Fill defaults for optional fields
    record["booking_id_date"] = record.get("booking_id_date") or "NA"
    record["vehicle_number"] = record.get("vehicle_number") or "NA"
    record["gps_provider"] = record.get("gps_provider") or "NOT PROVIDED"
    record["origin_location"] = (record.get("origin_location") or "NA").title()
    record["destination_location"] = (record.get("destination_location") or "NA").title()
    record["current_location"] = (record.get("current_location") or "NA").title()
    record.pop("destination_location_2", None)
    record["on_time"] = "Yes" if record.get("on_time") == "G" else "No"
    record["delay"] = "Yes" if record.get("delay") == "R" else "No"
    tsd = record.get("trip_start_date", "")
    if tsd and len(tsd.split(":")) == 2:
        record["trip_start_date"] = tsd + ":00"
    record["trip_end_date"] = record.get("trip_end_date") or "NA"
    record["vehicle_type"] = (record.get("vehicle_type") or "NA").title()
    record["min_km_per_day"] = record.get("min_km_per_day") or "NA"
    record["driver_name"] = (record.get("driver_name") or "NA").title()
    record["driver_mobile_number"] = record.get("driver_mobile_number") or "NA"
    record["customer_name_code"] = (record.get("customer_name_code") or "NA").title()
    record["supplier_name_code"] = (record.get("supplier_name_code") or "NA").title()
    record["material_shipped"] = (record.get("material_shipped") or "NA").title()

    return record

# -----------------------------
# Consume Loop
# -----------------------------
print("Starting Kafka consumer...")

try:
    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            print(f"Consumer error: {msg.error()}")
            continue

        record = msg.value()
        if record:
            cleaned = validate_and_clean(record)
            if cleaned:
                if collection.find_one({"booking_id": cleaned["booking_id"]}):
                    print(f"Duplicate booking_id {cleaned['booking_id']} skipped.")
                else:
                    collection.insert_one(cleaned)
                    print(f"Inserted record: {cleaned['booking_id']}")

except KeyboardInterrupt:
    print("Consumer stopped.")

finally:
    consumer.close()