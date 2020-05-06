from telegram import ReplyKeyboardMarkup

def get_custom_keyboard(values, max_column=2):
    #row_size = len(options) / max_column
    schema = [[value] for value in values]
    return ReplyKeyboardMarkup(schema)

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
    'ES': ReplyKeyboardMarkup([
        ['Cambiar imagen de perfil', 'Cambiar nombre'],
        ["Cambiar género", 'Cambiar idioma'],
        ['Establecer horario', "Ver mi perfil"]
    ]
    ),
    'EN': ReplyKeyboardMarkup(
        [
            ['Change profile picture', 'Change name'],
            ["Change gender", 'Change language'],
            ['Set schedule', "View my profile"]
        ]
    ),
}
