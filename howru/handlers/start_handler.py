from telegram import ReplyKeyboardRemove
from telegram.ext import ConversationHandler, CommandHandler, MessageHandler, Filters

from models import keyboards
from models.Patient import Patient
from log.logger import logger
from config.messages import messages

GENDER, PICTURE, COUNTRY, LANGUAGE = range(4)
patient = Patient()


def start(update, context):
    user = update.message.from_user
    patient.name = user.first_name
    patient.identifier = user.id
    # Check that user is not registered
    if patient.exists():
        context.bot.send_message(chat_id=user.id,
                                 text=messages[patient.language]['already_exists'])
        return ConversationHandler.END

    logger.info(f'User {user.username} name {user.first_name} id {user.id} started a new conversation')
    context.bot.send_message(chat_id=user.id,
                             text=f'Hi {user.first_name}. Welcome to HOW-R-U psychologist bot.\n'
                                  f'Hola {user.first_name}. Bienvenido al bot psicólogo HOW-R-U')
    context.bot.send_message(chat_id=user.id,
                             text=f'Please select a language:\n'
                                  f'Elija un idioma por favor:',
                             reply_markup=keyboards.language_keyboard)

    return LANGUAGE


def language(update, context):
    user = update.message.from_user
    language = update.message.text
    logger.info(f'User {user.username} name {user.first_name} id {user.id} chose language {language}')
    patient.language = language
    context.bot.send_message(chat_id=user.id,
                             text=messages[patient.language]['choose_gender'],
                             reply_markup=keyboards.gender_keyboard[patient.language])
    return GENDER


def gender(update, context):
    user = update.message.from_user
    logger.info(
        f'User {user.username} name {user.first_name} id {user.id} chose gender {update.message.text}')
    update.message.reply_text(messages[patient.language]['choose_pic'], reply_markup=ReplyKeyboardRemove())
    patient.gender = update.message.text
    return PICTURE


def picture(update, context):
    user = update.message.from_user
    photo_file = update.message.photo[-1].get_file()
    pic_name = f'pics/{user.id}.jpg'
    photo_file.download(pic_name)
    logger.info(f'User {user.username} name {user.first_name} {user.last_name} id {user.id} sent picture {pic_name}')
    update.message.reply_text(messages[patient.language]['choose_country'])
    patient.picture = pic_name
    return COUNTRY


def skip_picture(update, context):
    user = update.message.from_user
    logger.info(
        f'User {user.username} name {user.first_name} id {user.id} did not send a picture, using default')
    patient.picture = f'pics/default_profile_picture.png'
    update.message.reply_text(messages[patient.language]['choose_country'])
    return COUNTRY


def country(update, context):
    user = update.message.from_user
    country = update.message.text
    logger.info(f'User {user.username} name {user.first_name} id {user.id} chose country {country}')
    patient.country = country
    result = patient.to_db()
    update.message.reply_text(messages[patient.language]['registration_ok'])
    return ConversationHandler.END


start_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states={
        LANGUAGE: [MessageHandler(Filters.regex(f'^({keyboards.flag("es")}|{keyboards.flag("gb")})$'), language)],
        GENDER: [MessageHandler(Filters.regex('^(Male|Female|Other|Masculino|Femenino|Otro)$'), gender)],
        PICTURE: [MessageHandler(Filters.photo, picture),
                  CommandHandler('skip', skip_picture)
                  ],
        COUNTRY: [MessageHandler(Filters.text, country)]
    },
    fallbacks=[]
)
