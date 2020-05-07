from telegram import ReplyKeyboardRemove, ChatAction
from telegram.ext import ConversationHandler, CommandHandler, MessageHandler, Filters

from models import keyboards
from models.Patient import Patient
from log.logger import logger
from config.messages import messages

PROCESS_PROFILE_PIC, PROCESS_NAME, PROCESS_GENDER, CHOOSING, PROCESS_LANGUAGE = range(5)


class ConfigHandler(object):
    def __init__(self):
        self.patient = Patient()

    def config_menu(self, update, context):
        context.bot.send_message(chat_id=self.user.id,
                                 text=messages[self.patient.language]['select_config'],
                                 reply_markup=keyboards.config_keyboard[self.patient.language])
        return CHOOSING

    def config(self, update, context):
        self.user = update.message.from_user
        logger.info(f'User {self.user.username} name {self.user.first_name} id {self.user.id} started the configurator')
        try:
            self.patient = Patient(identifier=self.user.id, load_from_db=True)
        except Exception:
            logger.info(f'User {self.user.username} name {self.user.first_name} id {self.user.id} was not registered')
            update.message.reply_text('You must register first by clicking /start\n'
                                      'Debes registrarte primero pulsando /start.', reply_markup=ReplyKeyboardRemove())
            return ConversationHandler.END
        return self.config_menu(update, context)

    def ask_profile_pic(self, update, context):
        # Send current picture
        picture_path = self.patient.picture
        logger.error(picture_path)
        update.message.reply_text(messages[self.patient.language]['current_picture'],
                                  reply_markup=ReplyKeyboardRemove())
        update.message.reply_photo(open(picture_path, 'rb'))
        update.message.reply_text(messages[self.patient.language]['change_picture'], reply_markup=ReplyKeyboardRemove())
        return PROCESS_PROFILE_PIC

    def process_profile_pic(self, update, context):
        photo_file = update.message.photo[-1].get_file()
        pic_name = f'pics/{self.user.id}.jpg'
        photo_file.download(pic_name)
        self.patient.picture = pic_name
        logger.info(f'User {self.user.username} name {self.user.first_name} id {self.user.id} changed profile picture')
        update.message.reply_text(messages[self.patient.language]['picture_updated'],
                                  reply_markup=ReplyKeyboardRemove())
        return self.config_menu(update, context)

    def ask_change_name(self, update, context):
        logger.info(f'User {self.user.username} name {self.user.first_name} id {self.user.id} asked to change name')
        update.message.reply_text(messages[self.patient.language]['current_name'] + self.patient.name)
        update.message.reply_text(messages[self.patient.language]['change_name'], reply_markup=ReplyKeyboardRemove())
        return PROCESS_NAME

    def process_name(self, update, context):
        old_name = self.patient.name
        name = update.message.text
        self.patient.name = name
        logger.info(f'User {self.user.username} old  name {old_name} id {self.user.id} changed name to {name}')
        update.message.reply_text(messages[self.patient.language]['name_updated'])
        return self.config_menu(update, context)

    def ask_change_gender(self, update, context):
        logger.info(f'User {self.user.username} name {self.user.first_name} id {self.user.id} asked to change gender')
        update.message.reply_text(messages[self.patient.language]['current_gender'] + self.patient.gender)
        update.message.reply_text(messages[self.patient.language]['change_gender'],
                                  reply_markup=keyboards.gender_keyboard[self.patient.language])
        return PROCESS_GENDER

    def process_gender(self, update, context):
        gender = update.message.text
        self.patient.gender = gender
        logger.info(f'User {self.user.username} name {self.patient.name} id {self.user.id} changed gender to {gender}')
        update.message.reply_text(messages[self.patient.language]['gender_updated'])
        return self.config_menu(update, context)

    def ask_change_language(self, update, context):
        logger.info(f'User {self.user.username} name {self.user.first_name} id {self.user.id} asked to change language')
        update.message.reply_text(messages[self.patient.language]['current_language'] + self.patient.language)
        update.message.reply_text(messages[self.patient.language]['change_language'],
                                  reply_markup=keyboards.language_keyboard)
        return PROCESS_LANGUAGE

    def process_language(self, update, context):
        language = update.message.text
        self.patient.language = language
        logger.info(f'User {self.user.username} name {self.patient.name} id {self.user.id} changed language to {language}')
        update.message.reply_text(messages[self.patient.language]['language_updated'])
        return self.config_menu(update, context)

    def cancel(self, update, context):
        logger.info(
            f'User {self.user.username} name {self.user.first_name} id {self.user.id} cancelled current operation.')
        return self.config_menu(update, context)

    def _exit(self, update, context):
        logger.info(f'User {self.user.username} name {self.user.first_name} id {self.user.id} close the configurator.')
        update.message.reply_text(messages[self.patient.language]['exit_configurator'],
                                  reply_markup=ReplyKeyboardRemove())
        return ConversationHandler.END


instance = ConfigHandler()
config_handler = ConversationHandler(
    entry_points=[CommandHandler('config', instance.config)],
    states={
        CHOOSING: [MessageHandler(Filters.regex('^(Cambiar imagen de perfil|Change profile picture)$'),
                                  instance.ask_profile_pic),
                   MessageHandler(Filters.regex('^(Cambiar nombre|Change name)$'), instance.ask_change_name),
                   MessageHandler(Filters.regex('^(Cambiar género|Change gender)$'), instance.ask_change_gender),
                   MessageHandler(Filters.regex(f'^(Cambiar idioma|Change language)$'),
                                  instance.ask_change_language)
                   ],
        PROCESS_GENDER: [
            MessageHandler(Filters.regex('^(Male|Female|Other|Masculino|Femenino|Otro)$'), instance.process_gender)],
        PROCESS_PROFILE_PIC: [MessageHandler(Filters.photo, instance.process_profile_pic)],
        PROCESS_NAME: [MessageHandler(Filters.text, instance.process_name)],
        PROCESS_LANGUAGE: [MessageHandler(Filters.regex(f'^({keyboards.flag("es")}|{keyboards.flag("gb")})$'),
                                           instance.process_language)]
    },
    fallbacks=[CommandHandler('cancel', instance.cancel),
               CommandHandler('exit', instance._exit)]
)
