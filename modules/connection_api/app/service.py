from datetime import datetime

from connection_pb2_grpc import ConnectionServiceServicer

from app.helpers import find_contacts

DATE_FORMAT = "%Y-%m-%d"


class ConnectionServicer(ConnectionServiceServicer):

    def FindContacts(self, request, context):

        all_contacts = find_contacts(request.person_id, datetime.strptime(
            request.start_date, DATE_FORMAT), datetime.strptime(request.end_date, DATE_FORMAT))
        return all_contacts
