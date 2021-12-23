from concurrent import futures

import grpc
import location_pb2
import location_pb2_grpc
from json import dumps
from kafka import KafkaProducer

TOPIC_NAME = 'location'
KAFKA_SERVER = 'localhost:9092'

kafka_producer = KafkaProducer(bootstrap_servers=KAFKA_SERVER,
                               value_serializer=lambda v: dumps(v).encode('utf-8'))


class LocationgRPCServer(location_pb2_grpc.LocationServiceServicer):
    def createLocation(self, request, context):
        print("Received location")

        location_value = {
            "person_id": request.person_id,
            "latitude": request.latitude,
            "longitude": request.longitude
        }

        print('Received from client: %s' % location_value)

        # insert to kafka
        send_message_to_kafka(location_value)
        return location_pb2.LocationMessage(**location_value)


def send_message_to_kafka(location):
    kafka_producer.send(TOPIC_NAME, value=location)
    kafka_producer.flush()


def start_server():
    # Initialize gRPC server
    loc_server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
    location_pb2_grpc.add_LocationServiceServicer_to_server(LocationgRPCServer(),loc_server)

    print("Server starting on port 5005...")
    loc_server.add_insecure_port("[::]:5005")
    loc_server.start()
    loc_server.wait_for_termination()


if __name__ == '__main__':
    start_server()
