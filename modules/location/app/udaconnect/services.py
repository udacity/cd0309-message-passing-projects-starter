import logging
from datetime import datetime, timedelta
from typing import Dict, List

from app import db
from app.udaconnect.models import Connection, Location, Person
from app.udaconnect.schemas import ConnectionSchema, LocationSchema, PersonSchema
from geoalchemy2.functions import ST_AsText, ST_Point
from sqlalchemy.sql import text
import os
import json

from kafka import KafkaProducer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("location-api")

class LocationService:
    @staticmethod
    def retrieve(location_id) -> Location:
        location, coord_text = (
            db.session.query(Location, Location.coordinate.ST_AsText())
            .filter(Location.id == location_id)
            .one()
        )

        # Rely on database to return text form of point to reduce overhead of conversion in app code
        location.wkt_shape = coord_text
        return location

    @staticmethod
    def create(location: Dict):
        validation_results: Dict = LocationSchema().validate(location)
        if validation_results:
            logger.warning(f"Unexpected data format in payload: {validation_results}")
            raise Exception(f"Invalid payload: {validation_results}")
        
        kafka_bootstrap_servers = os.environ["KAFKA_BOOTSTRAP_SERVERS"]
        logging.info(kafka_bootstrap_servers)
        producer_config = {
            'bootstrap_servers': kafka_bootstrap_servers,
            'client_id': 'location-producer',
            'value_serializer': lambda v: json.dumps(v).encode('utf-8'),
        }

        producer = KafkaProducer(**producer_config)
        creation_time_str = location["creation_time"]
        location["creation_time"] = datetime.fromisoformat(creation_time_str)

        location_data = {
            'person_id': location["person_id"],
            'latitude': location["latitude"],
            'longitude': location["longitude"],
            'creation_time': location["creation_time"].isoformat()
        }

        kafka_topic = 'location-topic'
        producer.send(kafka_topic, value=location_data)

        return location
