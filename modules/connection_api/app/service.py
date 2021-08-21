from person_pb2 import Person, PersonList
from person_pb2_grpc import PersonServiceServicer

from app.helpers import get_person_from_id, get_all_persons, put_person


class PersonServicer(PersonServiceServicer):
    def Create(self, request, context):

        put_person(request.id, request.first_name, request.last_name, request.company_name)
        return Person(
            id=request.id,
            first_name=request.first_name,
            last_name=request.last_name,
            company_name=request.company_name,
        )

    def Get(self, request, context):

        required_person = get_person_from_id(request.id)
        return Person(
            id=required_person.id,
            first_name=required_person.first_name,
            last_name=required_person.last_name,
            company_name=required_person.company_name,
        )

    def GetAll(self, request, context):

        result = PersonList()

        result.persons.extend(
            map(
                lambda each_person: Person(
                    id=each_person.id,
                    first_name=each_person.first_name,
                    last_name=each_person.last_name,
                    company_name=each_person.company_name,
                ), get_all_persons()))
        return result
