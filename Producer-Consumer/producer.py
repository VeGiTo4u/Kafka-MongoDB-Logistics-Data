import pandas as pd
from confluent_kafka import SerializingProducer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer
from confluent_kafka.serialization import StringSerializer

# -----------------------------
# Delivery Report Callback
# -----------------------------
def delivery_report(err, msg):
    if err is not None:
        print(f"Message delivery failed: {err}")
        return
    print(f"Record {msg.key()} successfully produced to {msg.topic()} [{msg.partition()}] at offset {msg.offset()}")
    print("====================================")

# -----------------------------
# Kafka Configuration
# -----------------------------
kafka_config = {
    'bootstrap.servers': 'pkc-l7pr2.ap-south-1.aws.confluent.cloud:9092',
    'security.protocol': 'SASL_SSL',
    'sasl.mechanisms': 'PLAIN',
    'sasl.username': 'FZBOYWFTQJJYEYJI',
    'sasl.password': 'cflt4KkUeQ62wf1l7oaBSPGhtqCBJEbL+/86rxNNj65ZWXCGIQQus+X00dX3HX8g'
}

# -----------------------------
# Schema Registry Configuration
# -----------------------------
schema_registry_client = SchemaRegistryClient({
    "url": "https://psrc-4x6n5v3.us-east-2.aws.confluent.cloud",
    "basic.auth.user.info": "{}:{}".format(
        'YRJSAGLV5HKBBJPU',
        'cflt5FVT4wFd9i7ZKooNdRx+oY8QUu/cK/WjMzRaxJakfzS2PLafGu8A6Sm/xTrg'
    )
})

# Fetch latest Avro schema
def get_latest_schema(subject_name):
    schema_response = schema_registry_client.get_latest_version(subject_name)
    return schema_response.schema.schema_str

schema_str = get_latest_schema('logistics_data-value')
avro_serializer = AvroSerializer(schema_registry_client, schema_str)

# Key serializer
key_serializer = StringSerializer('utf_8')

# Initialize producer
producer = SerializingProducer({
    'bootstrap.servers': kafka_config['bootstrap.servers'],
    'security.protocol': kafka_config['security.protocol'],
    'sasl.mechanisms': kafka_config['sasl.mechanisms'],
    'sasl.username': kafka_config['sasl.username'],
    'sasl.password': kafka_config['sasl.password'],
    'key.serializer': key_serializer,
    'value.serializer': avro_serializer
})

# -----------------------------
# Load CSV
# -----------------------------
df = pd.read_csv('delivery_trip_truck_data.csv', header=0)
df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]  # normalize headers
print("Columns in CSV:", list(df.columns))

# -----------------------------
# Safe string conversion for Avro
# -----------------------------
def safe_string(val):
    if pd.isna(val):
        return None
    return str(val)

# -----------------------------
# Mapping function to match Avro schema
# -----------------------------
def map_row_to_schema(row):
    return {
        "gps_provider": safe_string(row.get("gpsprovider")),
        "booking_id": safe_string(row.get("bookingid")),
        "market_regular": safe_string(row.get("market_regular")),
        "booking_id_date": safe_string(row.get("bookingid_date")),
        "vehicle_number": safe_string(row.get("vehicle_no")),
        "origin_location": safe_string(row.get("origin_location")),
        "destination_location": safe_string(row.get("destination_location")),
        "origin_latitude_longitude": safe_string(row.get("org_lat_lon")),
        "destination_latitude_longitude": safe_string(row.get("des_lat_lon")),
        "data_pin_time": safe_string(row.get("data_ping_time")),
        "planned_eta": safe_string(row.get("planned_eta")),
        "current_location": safe_string(row.get("current_location")),
        "destination_location_2": safe_string(row.get("destinationlocation")),
        "actual_eta": safe_string(row.get("actual_eta")),
        "current_latitude": safe_string(row.get("curr_lat")),
        "current_longitude": safe_string(row.get("curr_lon")),
        "on_time": safe_string(row.get("ontime")),
        "delay": safe_string(row.get("delay")),
        "origin_location_code": safe_string(row.get("originlocation_code")),
        "destination_location_code": safe_string(row.get("destinationlocation_code")),
        "trip_start_date": safe_string(row.get("trip_start_date")),
        "trip_end_date": safe_string(row.get("trip_end_date")),
        "transportation_distance_km": int(row.get("transportation_distance_in_km")) if pd.notna(row.get("transportation_distance_in_km")) else None,
        "vehicle_type": safe_string(row.get("vehicletype")),
        "min_km_per_day": safe_string(row.get("minimum_kms_to_be_covered_in_a_day")),
        "driver_name": safe_string(row.get("driver_name")),
        "driver_mobile_number": safe_string(row.get("drivermobileno")),
        "customer_id": safe_string(row.get("customerid")),
        "customer_name_code": safe_string(row.get("customernamecode")),
        "supplier_id": safe_string(row.get("supplierid")),
        "supplier_name_code": safe_string(row.get("suppliernamecode")),
        "material_shipped": safe_string(row.get("material_shipped"))
    }

# -----------------------------
# Produce messages
# -----------------------------
for idx, row in df.iterrows():
    key = safe_string(row.get("gpsprovider")) or "unknown_key"
    value = map_row_to_schema(row)

    producer.produce(
        topic='logistics_data',
        key=key,
        value=value,
        on_delivery=delivery_report
    )

# Flush remaining messages
producer.flush()
print("All records published successfully.")