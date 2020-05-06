import bson

from helpers.MongoHelper import MongoHelper
from log.logger import logger


class JournalEntry(object):
    def __init__(self, identifier, question_id, patient_id, doctor_id, collection_name, load_from_db):
        self.type = collection_name
        self.db = MongoHelper(db='users', collection=self.type)
        self._identifier = str(identifier) if identifier else bson.ObjectId()
        if load_from_db:
            self.load_from_db()
        else:
            self._question_id = question_id
            self._patient_id = patient_id
            self._doctor_id = doctor_id

    def to_dict(self):
        return {
            '_id': self._identifier,
            'question_id': self._question_id,
            'patient_id': self._patient_id,
            'doctor_id': self._doctor_id,
        }

    def from_dict(self, doc):
        self._question_id = doc['question_id']
        self._patient_id = doc['patient_id']
        self._doctor_id = doc['doctor_id']
        self._language = doc['language']

    def to_db(self):
        logger.debug("Inserting journal entry %d type %d into database...", self.identifier, self.type)
        record = self.to_dict()
        return self.db.insert_document(record)

    def load_from_db(self):
        try:
            doc = self.db.get_document_by_id(self.identifier)
            self.from_dict(doc)
        except:
            logger.exception(f'Unable to retrieve user {self.identifier} from DB.')
            raise Exception

    def update_field(self, field, value):
        self.db.update_document(self.identifier, {'$set': {field: value}})

    @property
    def identifier(self):
        return self._identifier

    @identifier.setter
    def identifier(self, value):
        raise Exception("Identifier can not be changed")

    @property
    def question_id(self):
        return self._question_id

    @question_id.setter
    def question_id(self, value):
        self._question_id = value
        self.update_field('question_id', value)

    @property
    def patient_id(self):
        return self._patient_id

    @patient_id.setter
    def patient_id(self, value):
        self._patient_id = value
        self.update_field('patient_id', value)

    @property
    def doctor_id(self):
        return self._doctor_id

    @doctor_id.setter
    def doctor_id(self, value):
        self._doctor_id = value
        self.update_field('doctor_id', value)

    @property
    def language(self):
        if not self._language:
            doc = self.db.get_document_by_id(self.identifier)
            self._language = doc['language']
        return self._language

    # Language must be normalized
    @language.setter
    def language(self, value):
        self._language = value
        self.update_field('language', self._language)

