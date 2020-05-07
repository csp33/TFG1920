from datetime import datetime

import pytz

from helpers import UTCTime
from models.Users.User import User


class Patient(User):
    def __init__(self, identifier=None, name=None, picture=None, gender=None,
                 language=None, load_from_db=False, schedule=None):
        self._schedule = schedule
        super().__init__(name=name,
                         identifier=identifier,
                         picture=picture,
                         gender=gender,
                         language=language,
                         role="Patient",
                         collection_name='patients',
                         load_from_db=load_from_db)

    @property
    def schedule(self):
        return self._schedule

    @schedule.setter
    def schedule(self, value):
        utc_result = UTCTime.get_utc_result(value)
        self._schedule = utc_result
        self.update_field('schedule', utc_result)

    def to_dict(self):
        result = super().to_dict()
        result['schedule'] = self.schedule
        return result

    def from_dict(self, doc):
        self._schedule = doc['schedule']
        super().from_dict(doc)
