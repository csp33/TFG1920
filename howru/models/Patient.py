from models.User import User


class Patient(User):
    def __init__(self, name=None, identifier=None, picture=None, country=None, gender=None,
                 language=None):
        super().__init__(name=name,
                         identifier=identifier,
                         picture=picture,
                         country=country,
                         gender=gender,
                         language=language,
                         role="Patient",
                         collection_name='patients')
