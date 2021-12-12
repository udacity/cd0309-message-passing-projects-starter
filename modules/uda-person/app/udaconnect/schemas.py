from app.udaconnect.models import Person
from marshmallow import Schema, fields



class PersonSchema(Schema):
    id = fields.Integer()
    first_name = fields.String()
    last_name = fields.String()
    company_name = fields.String()

    class Meta:
        model = Person

