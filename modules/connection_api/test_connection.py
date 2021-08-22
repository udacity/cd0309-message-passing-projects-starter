import grpc
import connection_pb2
import connection_pb2_grpc

"""
Sample implementation of a writer that can be used to write messages to gRPC.
"""

print("Sending sample payload...")

channel = grpc.insecure_channel("localhost:5005")
stub = connection_pb2_grpc.ConnectionServiceStub(channel)

# Update this with desired payload
print("Testing Find Contacts API")
find_contacts = connection_pb2.ConnectionRequest(
    person_id=1,
    start_date="2019-04-04",
    end_date="2021-09-04",
    meters=100,
)
response = stub.FindContacts(find_contacts)
print(response)
print("DONE: Testing Find Contacts API")
