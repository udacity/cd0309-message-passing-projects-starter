from concurrent import futures
import os
import grpc
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import logging
import persons_pb2
import persons_pb2_grpc

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

Base = declarative_base()

class Person(Base):
    __tablename__ = 'person'

    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    company_name = Column(String)

class PersonServicer(persons_pb2_grpc.PersonServiceServicer):
    def RetrieveAllPersons(self, request, context):
        persons = db.query(Person).all()
        logging.info(persons)

        grpc_persons = persons_pb2.ListPerson(persons=[
            persons_pb2.Person(id=p.id, first_name=p.first_name, last_name=p.last_name, company_name=p.company_name)
            for p in persons
        ])

        return grpc_persons

def serve():
    logging.info("Server is starting...")
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    persons_pb2_grpc.add_PersonServiceServicer_to_server(
        PersonServicer(), server
    )
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()
    logging.info("Server started")


if __name__ == "__main__":
    serve()