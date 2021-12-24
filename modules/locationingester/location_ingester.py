from json import loads
from kafka import KafkaConsumer
import os
from sqlalchemy import create_engine
from geoalchemy2.functions import ST_Point

TOPIC_NAME = 'location'
DB_USERNAME = os.environ['DB_USERNAME']
DB_PASS = os.environ['DB_PASSWORD']
DB_HOST = os.environ['DB_HOST']
DB_PORT = os.environ['DB_PORT']
DB_NAME = os.environ['DB_NAME']
KAFKA_SERVER = os.environ['KAFKA_SERVER']

# DB_USERNAME = 'DB_USERNAME'
# DB_PASS = 'DB_PASSWORD'
# DB_HOST = 'DB_HOST'
# DB_PORT = 'DB_PORT'
# DB_NAME = 'DB_NAME'
# KAFKA_SERVER = 'KAFKA_SERVER'

consumer = KafkaConsumer(TOPIC_NAME, bootstrap_servers=KAFKA_SERVER,
                         value_deserializer=lambda x: loads(x.decode('utf-8')))


def add_loc_record_to_db(location):
    conn_string = 'postgresql://%s:%s@%s:%s/%s' % (DB_USERNAME, DB_PASS, DB_HOST, DB_PORT, DB_NAME)
    print(conn_string)
    db_engine = create_engine(conn_string)
    db_con = db_engine.connect()

    person_id = location['person_id']
    latitude = location['latitude']
    longitude = location['longitude']

    insert_sql = "insert into location (person_id, coordinate) VALUES ({}, ST_Point({}, {}))".format(person_id, latitude, longitude)
    print(insert_sql)
    db_con.execute(insert_sql)


def start_consumer():
    while True:
        for message in consumer:
            location = message.value
            print(location)
            print('person_id: %d' % location['person_id'])
            print('latitude: %s' % location['latitude'])
            print('longitude: %s' % location['longitude'])
            add_loc_record_to_db(location)


if __name__ == '__main__':
    start_consumer()