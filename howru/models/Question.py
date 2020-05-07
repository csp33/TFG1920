import bson

from helpers.MongoHelper import MongoHelper
from log.logger import logger


class Question(object):
    def __init__(self, identifier, text=None, responses=None, creator_id=None, public=None, load_from_db=None, language=None):
        self.db = MongoHelper(collection='questions', db='questions')
        self._identifier = str(identifier) if identifier else bson.ObjectId()
        if load_from_db:
            self.load_from_db()
        else:
            self._text = str(text)
            self._responses = responses if isinstance(responses, list) else [str(responses)]
            self._creator_id = bson.ObjectId(creator_id)
            self._public = str(public)
            self._language = str(language)


    def to_dict(self):
        return {
            '_id': self._identifier,
            'text': self._text,
            'responses': self._responses,
            'creator_id': self._creator_id,
            'public': self._public,
            'language': self._language
        }

    def to_db(self):
        logger.debug("Inserting question %d into database...", self.identifier)
        record = self.to_dict()
        return self.db.insert_document(record)

    def exists(self):
        return self.db.count_documents({'_id': self.identifier})

    def load_from_db(self):
        try:
            doc = self.db.get_document_by_id(bson.ObjectId(self.identifier))
            self.from_dict(doc)
        except:
            logger.exception(f'Unable to retrieve question {self.identifier} from DB.')
            raise Exception

    def from_dict(self, doc):
        self._text = doc['text']
        self._responses = doc['responses']
        self._creator_id = doc['creator_id']
        self._language = doc['language']
        self._public = doc['public']

    def update_field(self, field, value):
        self.db.update_document(self.identifier, {'$set': {field: value}})

    @property
    def identifier(self):
        return self._identifier

    @identifier.setter
    def identifier(self, value):
        raise Exception("Identifier can not be changed")

    @property
    def text(self):
        return self._text
    @text.setter
    def text(self, value):
        self._text = str(value)
        self.update_field('text', value)

    @property
    def responses(self):
        return self._responses
    @responses.setter
    def responses(self, value):
        if isinstance(value, list):
            self._responses = value
        else:
            self._responses = [str(value)]
        self.update_field('responses', value)

    @property
    def creator_id(self):
        return self._creator_id
    @creator_id.setter
    def creator_id(self, value):
        self._creator_id = value
        self.update_field('creator_id', value)

    @property
    def public(self):
        return self._public
    @public.setter
    def public(self, value):
        self._public = value
        self.update_field('public', value)
    @property
    def language(self):
        return self._language
    @language.setter
    def language(self, value):
        self._language = value
        self.update_field('language', value)
