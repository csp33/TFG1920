from helpers.MongoHelper import MongoHelper
from log.logger import logger
from models.keyboards import flag


class User(object):
    def __init__(self, name, identifier, picture, country, gender, role, language, collection_name, load_from_db):
        self.db = MongoHelper(collection_name)
        self.identifier = identifier
        self.role = role
        if load_from_db:
            self.load_from_db()
        else:
            self._name = name
            self._picture = picture
            self._country = country
            self._gender = gender
            self._language = language

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value
        self.update_field('name', self._name)

    @property
    def picture(self):
        return self._picture
    @picture.setter
    def picture(self, value):
        self._picture = value
        self.update_field('picture', self._picture)

    @property
    def country(self):
        return self._country
    @country.setter
    def country(self, value):
        self._country = value
        self.update_field('country', self._country)

    @property
    def gender(self):
        return self._gender
    @gender.setter
    def gender(self, value):
        self._gender = value
        self.update_field('gender', self._gender)

    @property
    def language(self):
        if not self._language:
            doc = self.db.get_document_by_id(self.identifier)
            self._language = doc['language']
        return self._language

    # Language must be normalized
    @language.setter
    def language(self, value):
        self._language = 'ES' if value == flag('es') else 'EN'
        self.update_field('language', self._language)

    def to_db(self):
        logger.debug("Inserting user %d role %d into database...", self.identifier, self.role)
        record = {
            'name': self._name,
            '_id': self.identifier,
            'picture': self._picture,
            'country': self._country,
            'gender': self._gender,
            'language': self._language
        }
        return self.db.insert_document(record)
    def exists(self):
        return self.db.count_documents({'_id': self.identifier})

    def load_from_db(self):
        try:
            doc = self.db.get_document_by_id(self.identifier)
            self._name = doc['name']
            self._picture = doc['picture']
            self._country = doc['country']
            self._gender = doc['gender']
            self._language = doc['language']
        except:
            logger.exception(f'Unable to retrieve user {self.identifier} from DB.')
            raise Exception

    def update_field(self, field, value):
        self.db.update_document(self.identifier, {'$set':{field: value}})
