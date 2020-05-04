from telegram import ReplyKeyboardRemove
from telegram.ext import ConversationHandler, CommandHandler, MessageHandler, Filters

from models import keyboards
from models.Patient import Patient
from log.logger import logger

GENDER, OTHER_GENDER, PICTURE, COUNTRY, LANGUAGE = range(5)
patient = Patient()

def start(update, context):
    user = update.message.from_user
    logger.info(f'User {user.username} name {user.first_name} id {user.id} started a new conversation')
    context.bot.send_message(chat_id=user.id,
                             text=f'Hi {user.first_name}. Welcome to HOW-R-U psychologist bot.')
    context.bot.send_message(chat_id=user.id,
                             text=f'Please select a language:\nElija un idioma por favor:',
                             reply_markup=keyboards.language_keyboard)
    patient.name = user.first_name
    patient.identifier = user.id
    return LANGUAGE


def language(update, context):
    user = update.message.from_user
    language = update.message.text
    logger.info(f'User {user.username} name {user.first_name} id {user.id} chose language {language}')
    patient.language = language
    context.bot.send_message(chat_id=user.id,
                             text=f'Please specify your gender:',
                             reply_markup=keyboards.gender_keyboard)
    return GENDER


def gender(update, context):
    user = update.message.from_user
    logger.info(
        f'User {user.username} name {user.first_name} id {user.id} chose gender {update.message.text}')
    update.message.reply_text('Please send a photo of yourself or send /skip if you don\'t want to.',
                              reply_markup=ReplyKeyboardRemove())
    patient.gender = update.message.text
    return PICTURE


def picture(update, context):
    user = update.message.from_user
    photo_file = update.message.photo[-1].get_file()
    pic_name = f'pics/{user.id}.jpg'
    photo_file.download(pic_name)
    logger.info(f'User {user.username} name {user.first_name} {user.last_name} id {user.id} sent picture {pic_name}')
    update.message.reply_text('Please write your county name.')
    patient.picture = pic_name
    return COUNTRY


def skip_picture(update, context):
    user = update.message.from_user
    logger.info(
        f'User {user.username} name {user.first_name} id {user.id} did not send a picture, using default')
    patient.picture = f'pics/default_profile_picture.jpg'
    update.message.reply_text('Please write your county name.')
    return COUNTRY


def country(update, context):
    user = update.message.from_user
    country = update.message.text
    logger.info(f'User {user.username} name {user.first_name} id {user.id} chose country {country}')
    patient.country = country
    result = patient.to_db()
    logger.info(result)
    update.message.reply_text('You have been successfully registered into the system.')
    return ConversationHandler.END


start_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states={
        LANGUAGE: [MessageHandler(Filters.regex(f'^({keyboards.flag("es")}|{keyboards.flag("gb")})$'), language)],
        GENDER: [MessageHandler(Filters.regex('^(Male|Female|Other)$'), gender)],
        PICTURE: [MessageHandler(Filters.photo, picture),
                  CommandHandler('skip', skip_picture)
                  ],
        COUNTRY: [MessageHandler(Filters.text, country)]
    },
    fallbacks=[]
)
