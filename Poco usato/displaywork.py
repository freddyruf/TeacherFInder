import pyrogram
import mysql.connector
from pyrogram.types import ReplyKeyboardMarkup

from __datafunction import *
from __keyboardsfunction import keyboardsgen
from __stringworksfunction import *


connection = create_connection("localhost", "root", "")
#}}} closing the connection function

cursor = connection.cursor(buffered=True) #cursor /Read-only attribute describing the result of a query.


keyboards=keyboardsgen(cursor)
tastiera1=keyboards[0]
tastiera2=keyboards[1]
tastiera3=keyboards[2]
tastiera4=keyboards[3]
allKeyboard=keyboards[4]

emojiKey=[[polliceInSu,polliceInGiù]]
emojiKeyboard = ReplyKeyboardMarkup(emojiKey, one_time_keyboard=True, resize_keyboard=True) #make keyboard object
def sand(connection,cursor,messaggio_originale,type,inQuestoMomento):
    global feedbot
    global feedresponse
    global feedmessage
    nome = mostSimilarFromList(
        messaggio_originale.upper(), allKeyboard)  # modify the message text to the name of the professor (to work in some functions)

    if (inQuestoMomento):
        ora=-1
        giorno=-1
    else:
        ora = FindTime(messaggio_originale)  # search the time
        print(ora)
        giorno = findDay(messaggio_originale)  # search the day


    info = prof_info(nome, ora,
                     giorno)  # get the info about the professor (ora and giorno can be '-1' if not found)

    if not isinstance(info, dict):  # if the professor is not in a class
        output = info


    else:  # if he is in school
        output = f"Il prof {nome.title()} si trova nella classe {info['Classe']} in Palazzina: {info['Palazzina']} Piano: {info['Piano']} Aula: {info['Aula']}"


    return output

