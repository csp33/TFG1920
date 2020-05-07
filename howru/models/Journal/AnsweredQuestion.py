from models.Journal.JournalEntry import JournalEntry


class AnsweredQuestion(JournalEntry):
    def __init__(self, identifier=None, question_id=None, patient_id=None, doctor_id=None,
                 answer_date=None, response=None, load_from_db=False):
        self._response = response
        self._answer_date = answer_date
        super().__init__(identifier=identifier, question_id=question_id, patient_id=patient_id, doctor_id=doctor_id,
                         collection_name='answered_questions', load_from_db=load_from_db)

    def to_dict(self):
        result = super().to_dict()
        result['response'] = self.response
        result['answer_date'] = self.answer_date
        return result

    @property
    def answer_date(self):
        return self._answer_date

    @answer_date.setter
    def answer_date(self, value):
        self._answer_date = value
        self.update_field('answer_date', value)

    @property
    def response(self):
        return self._response
    @response.setter
    def response(self, value):
        self._response = value
        self.update_field('response', value)