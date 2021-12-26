import logging
from datetime import datetime
from typing import Dict, List

import requests
from app import db
from app.udaconnect.models import Connection, Location, Person
from app.udaconnect.schemas import ConnectionSchema, LocationSchema, PersonSchema
from geoalchemy2.functions import ST_AsText, ST_Point
from sqlalchemy.sql import text
from app.config import CONNECTION_API_ENDPOINT

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger("udaconnect-api")


class PersonService:
    @staticmethod
    def create(person: Dict) -> Person:
        new_person = Person()
        new_person.first_name = person["first_name"]
        new_person.last_name = person["last_name"]
        new_person.company_name = person["company_name"]

        db.session.add(new_person)
        db.session.commit()

        return new_person

    @staticmethod
    def retrieve(person_id: int) -> Person:
        person = db.session.query(Person).get(person_id)
        return person

    @staticmethod
    def retrieve_all() -> List[Person]:
        return db.session.query(Person).all()

    @staticmethod
    def find_contacts(person_id: int, start_date: str, end_date: str, meters=5
                      ) -> List[Connection]:

        connections_list = []
        api_path = '/connections/%s/connection' % person_id
        query_string = '?start_date=%s&end_date=%s&distance=%s' % (start_date, end_date, meters)
        logger.info('api_path %s' % api_path)
        logger.info('query_string %s' % query_string)
        conn_url = CONNECTION_API_ENDPOINT + api_path + query_string
        logger.info('conn_url %s' % conn_url)
        connections = requests.get(conn_url)
        connections = connections.json()

        for connection in connections:
            location = Location()
            location.id = connection['location']["id"]
            location.person_id = connection['location']["person_id"]
            location.creation_time = datetime.fromisoformat(connection['location']["creation_time"])
            location.coordinate = ST_Point(connection['location']["latitude"], connection['location']["longitude"])
            location.set_wkt_with_coords(connection['location']["latitude"], connection['location']["longitude"])
            person = Person()
            person.id = connection['person']['id']
            person.first_name = connection['person']['first_name']
            person.last_name = connection['person']['last_name']
            person.company_name = connection['person']['company_name']

            connection = Connection(location, person)

            connections_list.append(connection)

        return connections_list

    @staticmethod
    def retrieve_locations(person_id: int) -> List[Location]:
        return db.session.query(Location).filter(Location.person_id == person_id).all()

