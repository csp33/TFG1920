from datetime import datetime

from telegram.ext import ConversationHandler, MessageHandler, Filters

from helpers.MongoHelper import MongoHelper
from log.logger import logger
from models.Journal.AnsweredQuestion import AnsweredQuestion

ANSWERING = range(1)


class QuestionHandler(object):
    def __init__(self):
        self.pending_db = MongoHelper(db='journal', collection='pending_questions')
        self.answered_db = MongoHelper(db='journal', collection='answered_questions')

    def answer_question(self, update, context):
        logger.info("asdasdad")
        user = update.message.from_user
        # Get question that is being answered from DB:
        question_task = self._get_pending_question_task(str(user.id))
        # Get response
        response = update.message.text
        logger.info(
            f'User {user.username} name {user.first_name} id {user.id} answered to question {question_task["question_id"]}')
        # Create answered question entry

        answered_question = AnsweredQuestion(patient_id=user.id, doctor_id=question_task['doctor_id'],
                                              answer_date=datetime.now())
        answered_question.to_db()
        # TODO gitanadaaa
        self.answered_db.insert_document(
            {'patient_id': user.id, 'doctor_id': question_task['doctor_id'],
             'answer_date': datetime.now()})
        # Delete question from pending
        logger.info(f'Deleting question task {question_task["_id"]} from pending_db...')
        self.pending_db.delete_document_by_id(question_task['_id'])

    def _get_pending_question_task(self, user_id):
        logger.info("user id", user_id)
        return self.pending_db.search_one({
            'patient_id': user_id,
            'answering': True
        })


instance = QuestionHandler()
question_handler = ConversationHandler(
    entry_points=[MessageHandler(Filters.text, instance.answer_question)],
    states={
        ANSWERING: [MessageHandler(Filters.text, instance.answer_question)]
    },
    fallbacks=[]
)
