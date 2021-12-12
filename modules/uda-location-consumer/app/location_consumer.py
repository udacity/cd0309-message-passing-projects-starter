import json
import os

from kafka import KafkaConsumer
import time

kafka_url = "udaconnect-kafka-0.udaconnect-kafka-headless.default.svc.cluster.local:9092"
kafka_topic = "test"

print('started listening ' + kafka_topic)

DB_USERNAME = os.environ["DB_USERNAME"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
DB_HOST = os.environ["DB_HOST"]
DB_PORT = os.environ["DB_PORT"]
DB_NAME = os.environ["DB_NAME"]


kafka_consumer = KafkaConsumer(kafka_topic, bootstrap_servers=kafka_url)

def save_in_db(location):
    from sqlalchemy import create_engine

    engine = create_engine(f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}", echo=True)
    conn = engine.connect()

    person_id = int(location["userId"])
    latitude, longitude = int(location["latitude"]), int(location["longitude"])

    insert = "INSERT INTO location (person_id, coordinate) VALUES ({}, ST_Point({}, {}))" \
        .format(person_id, latitude, longitude)

    print(insert)
    conn.execute(insert)


for location in kafka_consumer:
    message = location.value.decode('utf-8')
    print('{}'.format(message))
    location_message = json.loads(message)
    save_in_db(location_message)