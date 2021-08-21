import time
from concurrent import futures

import grpc
import person_pb2_grpc

from app.service import PersonServicer


# Initialize gRPC server
server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
person_pb2_grpc.add_PersonServiceServicer_to_server(
    PersonServicer(), server)


print("Server starting on port 5005...")
server.add_insecure_port("[::]:5005")
server.start()
# Keep thread alive
try:
    while True:
        time.sleep(86400)
except KeyboardInterrupt:
    server.stop(0)
