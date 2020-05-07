from models.Journal.JournalEntry import JournalEntry


class PendingQuestion(JournalEntry):
    def __init__(self, identifier=None, question_id=None, patient_id=None, doctor_id=None, language=None,
                 answering=None, load_from_db=False):
        self._answering = answering
        super().__init__(identifier=identifier, question_id=question_id, patient_id=patient_id, doctor_id=doctor_id,
                         collection_name='pending_questions', load_from_db=load_from_db)

    @property
    def answering(self):
        return self._answering

    @answering.setter
    def answering(self, value):
        self._answering = value
        self.update_field('answering', value)

    def to_dict(self):
        result = super().to_dict()
        result['answering'] = self.answering
        return result

    def from_dict(self, doc):
        self._answering = doc['answering']
        super().from_dict(doc)