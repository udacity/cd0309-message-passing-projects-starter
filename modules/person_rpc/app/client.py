from __future__ import print_function

import logging

import grpc
import persons_pb2
import persons_pb2_grpc
import os
from typing import Dict, List

grpc_server_address = os.environ["GRPC_SERVER_ADDRESS"]


def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    with grpc.insecure_channel(grpc_server_address) as channel:
        stub = persons_pb2_grpc.PersonServiceStub(channel=channel)
        logging.info("get list user")
        request = persons_pb2.RetrieveAllPersonsRequest()
        list_persons: persons_pb2.ListPerson = stub.RetrieveAllPersons(request)
        for person in list_persons.persons:
            logging.info("id: %s, name: %s, company: %s", person.id, person.first_name, person.company_name)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    run()