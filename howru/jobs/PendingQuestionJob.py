from datetime import datetime

from helpers.MongoHelper import MongoHelper
from log.logger import logger
from models import keyboards
from models.Question import Question
from models.Users.Patient import Patient



class PendingQuestionJob(object):
    def __init__(self, context, patient_id):
        self.db = MongoHelper(db='journal', collection='pending_questions')
        self.patient = Patient(identifier=patient_id, load_from_db=True)
        self._create_global_job(context)

    def global_callback(self, context):
        pending_questions = self._get_pending_questions()
        logger.info(pending_questions.count())
        for task in pending_questions:
            logger.info(f'Processing task {task}')
            question = Question(identifier=task['question_id'], load_from_db=True)
            self._create_question_job(context, question)
            # Set answering = true in db
            self.db.update_document(task['_id'], {'$set': {'answering': True}})
            # To avoid concurrency
            #while len(context.job_queue.jobs()):
             #   time.sleep(5)

    def _create_global_job(self, context):
        context.job_queue.run_daily(callback=self.global_callback,
                                    time=datetime.now(),
                                    name=f'{self.patient.identifier}_pending_questions_job')
        # TODO store jobs using pickle https://github.com/python-telegram-bot/python-telegram-bot/wiki/Code-snippets#save-and-load-jobs-using-pickle

    def question_callback(self, context):
        question = context.job.context
        context.bot.send_message(chat_id=self.patient.identifier, text=question.text,
                                 reply_markup=keyboards.get_custom_keyboard(question.responses))

    def _create_question_job(self, context, question):
        logger.info("Created job for question %s patient %s", question.identifier, self.patient.identifier)
        context.job_queue.run_once(callback=self.question_callback,
                                   context=question,
                                   when=datetime.now(),
                                   name=f'{self.patient.identifier}_pending_questions_job')

    def _get_pending_questions(self):
        logger.info(self.patient.identifier)
        return self.db.search({
            'patient_id': self.patient.identifier
        })
