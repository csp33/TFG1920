import pymongo
import ujson as json
from log.logger import logger
ROUTES_FILE_PATH = '/etc/chatbot/cfg/routes.json'
class MongoHelper(object):
    def __init__(self, collection, db='chatbot_users'):
        # Load parameters from routes file
        try:
            with open(ROUTES_FILE_PATH) as routes_file:
                json_file = json.load(routes_file)
                self.host = json_file['host']
                self.port = json_file['port']
                self.user = json_file.get('user', None)
                self.pwd = json_file.get('pwd', None)
        except:
            logger.exception('Unable to load DB routes.')
        self.db = pymongo.MongoClient(host=self.host, port=self.port)[db]
        self.collection = collection

    def insert_document(self, record):
        return self.db[self.collection].insert_one(record)

    def search(self, query={}):
        return self.db[self.collection].find(query)

    def get_document_by_id(self, identifier):
        return self.search({'_id': identifier})[0]

    def delete_document_by_id(self, identifier):
        return self.delete_document_by_query({'_id': identifier})

    def delete_document_by_query(self, query):
        return self.db[self.collection].delete_many(query)

    def count_documents(self, query):
        return self.db[self.collection].count_documents(query)

    def update_document(self, doc_id, content):
        self.db[self.collection].update_one({'_id': doc_id}, content)

