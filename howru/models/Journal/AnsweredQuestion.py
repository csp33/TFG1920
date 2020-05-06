from models.Journal.JournalEntry import JournalEntry


class AnsweredQuestion(JournalEntry):
    def __init__(self, identifier=None, question_id=None, patient_id=None, doctor_id=None,
                 answer_date=None, load_from_db=False):
        self._answer_date = answer_date
        super().__init__(identifier=identifier, question_id=question_id, patient_id=patient_id, doctor_id=doctor_id,
                         collection_name='answered_questions', load_from_db=load_from_db)

    @property
    def answer_date(self):
        return self._answer_date

    @answer_date.setter
    def answer_date(self, value):
        self._answer_date = value
        self.update_field('answer_date', value)