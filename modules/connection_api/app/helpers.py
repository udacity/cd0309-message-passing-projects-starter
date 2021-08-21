from app.db_helpers.models import Person, db_session


def get_person_from_id(person_id):
    return db_session.query(Person).get(person_id)


def get_all_persons():
    return db_session.query(Person).all()

def put_person(person_id, person_full_name, person_last_name, person_company):
    new_person = Person()
    new_person.id = person_id
    new_person.first_name = person_full_name
    new_person.last_name = person_last_name
    new_person.company_name = person_company
    db_session.add(new_person)
    db_session.commit()

    return new_person
