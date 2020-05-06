from models.Users.User import User


class Patient(User):
    def __init__(self, name=None, identifier=None, picture=None, gender=None,
                 language=None, load_from_db=False):
        super().__init__(name=name,
                         identifier=identifier,
                         picture=picture,
                         gender=gender,
                         language=language,
                         role="Patient",
                         collection_name='patients',
                         load_from_db=load_from_db)
