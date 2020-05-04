from helpers.MongoHelper import MongoHelper
from log.logger import logger

class User(object):
    def __init__(self, name, identifier, picture, country, gender, role, language, collection_name):
        self.name = name
        self.identifier = identifier
        self.picture = picture
        self.country = country
        self.gender = gender
        self.role = role
        self.language = language
        self.db = MongoHelper(collection_name)

    def to_db(self):
        logger.debug("Inserting user %d role %d into database...", self.identifier, self.role)
        record = {
            'name': self.name,
            '_id': self.identifier,
            'picture': self.picture,
            'country': self.country,
            'gender': self.gender,
            'language': self.language
        }
        return self.db.insert_document(record)