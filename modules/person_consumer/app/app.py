import logging
from datetime import datetime, timedelta
from typing import Dict, List

from geoalchemy2.functions import ST_AsText, ST_Point
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from marshmallow import Schema, fields

import os
import json
from kafka import KafkaConsumer

DB_USERNAME = os.environ["DB_USERNAME"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
DB_HOST = os.environ["DB_HOST"]
DB_PORT = os.environ["DB_PORT"]
DB_NAME = os.environ["DB_NAME"]

SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

logging.basicConfig(level= logging.INFO)

logging.info(SQLALCHEMY_DATABASE_URI)

engine = create_engine(SQLALCHEMY_DATABASE_URI)
Session = sessionmaker(bind=engine)
db = Session()


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("person-consumer")


Base = declarative_base()

class Person(Base):
    __tablename__ = 'person'

    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    company_name = Column(String)

class PersonSchema(Schema):
    id = fields.Integer()
    first_name = fields.String()
    last_name = fields.String()
    company_name = fields.String()

    class Meta:
        model = Person


class PersonService:
    @staticmethod
    def create(person: Dict) -> Person:
        new_person = Person()
        new_person.first_name = person["first_name"]
        new_person.last_name = person["last_name"]
        new_person.company_name = person["company_name"]

        db.add(new_person)
        db.commit()

        return new_person


# Kafka consumer configuration
kafka_bootstrap_servers = os.environ["KAFKA_BOOTSTRAP_SERVERS"]
consumer_config = {
    'bootstrap_servers': kafka_bootstrap_servers,
    'group_id': 'person-consumer-group',
    'auto_offset_reset': 'earliest',
    'enable_auto_commit': True,
}

# Create Kafka consumer
kafka_topic = os.environ["KAFKA_TOPIC"]
consumer = KafkaConsumer(kafka_topic, **consumer_config)

try:
    for msg in consumer:
        try:
            # Process the received message
            person_data = json.loads(msg.value.decode('utf-8'))

            # Create a person using PersonService
            PersonService.create(person_data)

            logger.info(f'Person created: {person_data}')
        except json.JSONDecodeError as e:
            logger.error(f'Error decoding JSON: {e}')

except KeyboardInterrupt:
    pass
finally:
    # Close the consumer
    consumer.close()