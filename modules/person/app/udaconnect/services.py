import logging
from datetime import datetime, timedelta
from typing import Dict, List

from app import db
from app.udaconnect.models import Person
from app.udaconnect.schemas import  PersonSchema
from geoalchemy2.functions import ST_AsText, ST_Point
from sqlalchemy.sql import text

import os
import json
from kafka import KafkaProducer

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger("person-api")


class PersonService:
    @staticmethod
    def create(person: Dict) -> Person:
        new_person = Person()
        new_person.first_name = person["first_name"]
        new_person.last_name = person["last_name"]
        new_person.company_name = person["company_name"]

        kafka_bootstrap_servers = os.environ["KAFKA_BOOTSTRAP_SERVERS"]
        producer_config = {
            'bootstrap_servers': kafka_bootstrap_servers,
            'client_id': 'location-producer',
            'value_serializer': lambda v: json.dumps(v).encode('utf-8'),
        }

        producer = KafkaProducer(**producer_config)

        kafka_topic = 'person-topic'
        producer.send(kafka_topic, value=person)

        return new_person

    @staticmethod
    def retrieve(person_id: int) -> Person:
        person = db.session.query(Person).get(person_id)
        return person

    @staticmethod
    def retrieve_all() -> List[Person]:
        return db.session.query(Person).all()
