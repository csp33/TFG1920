from models.Users.User import User


class Patient(User):
    def __init__(self, identifier=None, name=None, picture=None, gender=None,
                 language=None, load_from_db=False, questions_time=None):
        self._questions_time = questions_time
        super().__init__(name=name,
                         identifier=identifier,
                         picture=picture,
                         gender=gender,
                         language=language,
                         role="Patient",
                         collection_name='patients',
                         load_from_db=load_from_db)

    @property
    def questions_time(self):
        return self._questions_time
    @questions_time.setter
    def questions_time(self, value):
        self._questions_time = value
        self.update_field('questions_time', value)
