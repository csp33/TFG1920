from telegram import ReplyKeyboardMarkup


def flag(code):
    OFFSET = 127462 - ord('A')
    code = code.upper()
    return chr(ord(code[0]) + OFFSET) + chr(ord(code[1]) + OFFSET)


gender_keyboard = {
    'ES': ReplyKeyboardMarkup([['Masculino', 'Femenino', 'Otro']]),
    'EN': ReplyKeyboardMarkup([['Male', 'Female', 'Other']])
}
language_keyboard = ReplyKeyboardMarkup([[flag('es'), flag('gb')]])
config_keyboard = {
    'ES': ReplyKeyboardMarkup([['Cambiar imagen de perfil'], ['Cambiar nombre'], ["Cambiar género"], ['Cambiar idioma'],
                               ['Establecer horario']]),
    'EN': ReplyKeyboardMarkup(
        [['Change profile picture'], ['Change name'], ["Change gender"], ['Change language'], ['Set schedule']]),
}
