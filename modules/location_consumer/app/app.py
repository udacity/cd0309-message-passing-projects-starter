import logging
from datetime import datetime, timedelta
from typing import Dict, List

from geoalchemy2.functions import ST_AsText, ST_Point
from sqlalchemy import create_engine, BigInteger, Column, Date, DateTime, ForeignKey, Integer, String
from geoalchemy2 import Geometry
from geoalchemy2.shape import to_shape
from shapely.geometry.point import Point
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from marshmallow import Schema, fields
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.ext.hybrid import hybrid_property

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
logger = logging.getLogger("location-consumer")


Base = declarative_base()

class Location(Base):
    __tablename__ = "location"

    id = Column(BigInteger, primary_key=True)
    person_id = Column(Integer, nullable=False)
    coordinate = Column(Geometry("POINT"), nullable=False)
    creation_time = Column(DateTime, nullable=False, default=datetime.utcnow)
    _wkt_shape: str = None

    @property
    def wkt_shape(self) -> str:
        # Persist binary form into readable text
        if not self._wkt_shape:
            point: Point = to_shape(self.coordinate)
            # normalize WKT returned by to_wkt() from shapely and ST_AsText() from DB
            self._wkt_shape = point.to_wkt().replace("POINT ", "ST_POINT")
        return self._wkt_shape

    @wkt_shape.setter
    def wkt_shape(self, v: str) -> None:
        self._wkt_shape = v

    def set_wkt_with_coords(self, lat: str, long: str) -> str:
        self._wkt_shape = f"ST_POINT({lat} {long})"
        return self._wkt_shape

    @hybrid_property
    def longitude(self) -> str:
        coord_text = self.wkt_shape
        return coord_text[coord_text.find(" ") + 1 : coord_text.find(")")]

    @hybrid_property
    def latitude(self) -> str:
        coord_text = self.wkt_shape
        return coord_text[coord_text.find("(") + 1 : coord_text.find(" ")]

class LocationSchema(Schema):
    id = fields.Integer()
    person_id = fields.Integer()
    longitude = fields.String(attribute="longitude")
    latitude = fields.String(attribute="latitude")
    creation_time = fields.DateTime()

    class Meta:
        model = Location


class LocationService:
    @staticmethod
    def create(location: Dict) -> Location:
        validation_results: Dict = LocationSchema().validate(location)
        if validation_results:
            logger.warning(f"Unexpected data format in payload: {validation_results}")
            raise Exception(f"Invalid payload: {validation_results}")

        new_location = Location()
        new_location.person_id = location["person_id"]
        new_location.creation_time = location["creation_time"]
        new_location.coordinate = ST_Point(location["latitude"], location["longitude"])
        db.add(new_location)
        db.commit()

        return new_location


# Kafka consumer configuration
kafka_bootstrap_servers = os.environ["KAFKA_BOOTSTRAP_SERVERS"]
consumer_config = {
    'bootstrap_servers': kafka_bootstrap_servers,
    'group_id': 'location-consumer-group',
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
            location = json.loads(msg.value.decode('utf-8'))

            # Create a person using PersonService
            LocationService.create(location)

            logger.info(f'Location created: {location}')
        except json.JSONDecodeError as e:
            logger.error(f'Error decoding JSON: {e}')

except KeyboardInterrupt:
    pass
finally:
    # Close the consumer
    consumer.close()