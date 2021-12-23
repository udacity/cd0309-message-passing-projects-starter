import grpc
import location_pb2
import location_pb2_grpc

print("Sending location payload ....")

channel = grpc.insecure_channel("localhost:5005")
stub = location_pb2_grpc.LocationServiceStub(channel)

location = location_pb2.LocationMessage(
    person_id=500,
    latitude="900",
    longitude="-900"
)

response = stub.createLocation(location)