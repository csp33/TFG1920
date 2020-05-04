from models.User import User


class Doctor(User):
    def __init__(self, name=None, identifier=None, picture=None, country=None, gender=None, email=None,
                 language=None):
        self.email = email
        super().__init__(name=name,
                         identifier=identifier,
                         picture=picture,
                         country=country,
                         gender=gender,
                         language=language,
                         role="Doctor",
                         collection_name='doctors')
