from models.Users.User import User


class Doctor(User):
    def __init__(self, name=None, identifier=None, picture=None, gender=None, email=None,
                 language=None, load_from_db=False):
        self.email = email
        super().__init__(name=name,
                         identifier=identifier,
                         picture=picture,
                         gender=gender,
                         language=language,
                         role="Doctor",
                         collection_name='doctors',
                         load_from_db=load_from_db)
