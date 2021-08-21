import grpc
import person_pb2
import person_pb2_grpc

"""
Sample implementation of a writer that can be used to write messages to gRPC.
"""

print("Sending sample payload...")

channel = grpc.insecure_channel("localhost:5005")
stub = person_pb2_grpc.PersonServiceStub(channel)

# Update this with desired payload
print("Testing Person Create API")
create_person = person_pb2.Person(
    id=100,
    first_name="asdcmweocmwe",
    last_name="3",
    company_name="BS",
)
response = stub.Create(create_person)
print(response)
print("DONE: Testing Person Create API")


print("Testing Person GET API")
get_person = person_pb2.PersonRequest(
    id=1,
)
response = stub.Get(get_person)
print(response)
print("DONE: Testing Person GET API")


print("Testing Person GET ALL API")
get_all_person = person_pb2.PersonRequest()
response = stub.GetAll(get_all_person)
print(response)
print("DONE: Testing Person GET ALL API")
