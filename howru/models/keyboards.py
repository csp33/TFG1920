from telegram import ReplyKeyboardMarkup
OFFSET = 127462 - ord('A')

def flag(code):
    code = code.upper()
    return chr(ord(code[0]) + OFFSET) + chr(ord(code[1]) + OFFSET)

gender_keyboard =ReplyKeyboardMarkup([['Male', 'Female', 'Other']])
language_keyboard =ReplyKeyboardMarkup([[flag('es'), flag('gb')]])