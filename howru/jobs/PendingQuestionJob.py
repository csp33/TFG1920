import time
from datetime import datetime, timedelta
import pytz
from telegram import ReplyKeyboardRemove

from config.messages import messages
from helpers.MongoHelper import MongoHelper
from log.logger import logger
from models import keyboards
from models.Question import Question
from models.Users.Patient import Patient


class PendingQuestionJob(object):
    def __init__(self, context, patient_id):
        self.pending_db = MongoHelper(db='journal', collection='pending_questions')
        self.answered_db = MongoHelper(db='journal', collection='answered_questions')
        self.patient = Patient(identifier=patient_id, load_from_db=True)
        self._create_job(context)

    def job_callback(self, context):
        pending_questions = self._get_pending_questions()
        for task in pending_questions:
            question = Question(identifier=task['question_id'], load_from_db=True)
            self.pending_db.update_document(task['_id'], {'$set': {'answering': True}})
            context.bot.send_message(chat_id=self.patient.identifier, text=question.text,
                                     reply_markup=keyboards.get_custom_keyboard(question.responses))
            while not self.is_question_answered(task):
                time.sleep(1)
        message = messages[self.patient.language]['finish_answering'] if pending_questions.count() else \
        messages[self.patient.language]['no_questions']

        context.bot.send_message(chat_id=self.patient.identifier, text=message,
                                 reply_markup=ReplyKeyboardRemove())

    def _create_job(self, context):
        context.job_queue.run_daily(callback=self.job_callback,
                                    time=self.patient.schedule,
                                    name=f'{self.patient.identifier}_pending_questions_job')
        # TODO store jobs using pickle https://github.com/python-telegram-bot/python-telegram-bot/wiki/Code-snippets#save-and-load-jobs-using-pickle

    def is_question_answered(self, question_task):
        now = datetime.now()
        today = datetime(now.year, now.month, now.day)
        tomorrow = today + timedelta(days=1)
        return self.answered_db.count_documents(
            {
                'question_id': question_task['question_id'],
                'patient_id': self.patient.identifier,
                'answer_date': {'$gte': today, '$lt': tomorrow}
            })

    def _get_pending_questions(self):
        # TODO return objects instead of dicts...
        return self.pending_db.search({
            'patient_id': self.patient.identifier
        })
