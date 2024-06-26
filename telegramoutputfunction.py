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
def sand(connection,cursor,message,inQuestoMomento,bot):
    global feedbot
    global feedresponse
    global feedmessage
    message.text=message.text.replace("'","`").replace("‘","`").replace("’","`")
    original_message= message.text
    message.text = mostSimilarFromList(
        message.text.upper(), allKeyboard)  # modify the message text to the name of the professor (to work in some functions)
    if (inQuestoMomento):
        ora=-1
        giorno=-1
    else:
        ora = FindTime(original_message)  # search the time
        giorno = findDay(original_message)  # search the day

    info = prof_info(message, ora,
                     giorno)  # get the info about the professor (ora and giorno can be '-1' if not found)

    if not isinstance(info, dict):  # if the professor is not in a class
        output = info
        bot.send_message(message.chat.id, text=info)

    else:  # if he is in school
        output = f"Il prof {message.text.title()} si trova nella classe {info['Classe']} in: \n-Palazzina: {info['Palazzina']} \n-Piano: {info['Piano']} \n-Aula: {info['Aula']}"
        bot.send_message(message.chat.id, text=output)




    message.text = original_message  # original message
    feeding = feedbacktry(message, type, output)  # ask for feedback
    feedbot = feeding[1]
    feedresponse = feeding[2]
    feedmessage = feeding[3]
    if (feeding[0]):
        bot.send_message(message.chat.id, text="Potresti darci un feedback? " + polliceInSu + " o " + polliceInGiù,
                         reply_markup=emojiKeyboard)  # ask the user what he wants to do
    else:
        addLog(connection,cursor,message,feedmessage,feedresponse,feedbot)  # add the log into db

    return [feedbot, feedresponse, feedmessage]

def sandOne(connection,cursor,message,type,response,bot):
    global output
    global feedbot
    global feedresponse
    global feedmessage
    bot.send_message(message.chat.id, text=response)  # send the response of type of message requested
    output = response  # save the response

    feeding = feedbacktry(message, type, output)  # ask for feedback
    feedbot=feeding[1]
    feedresponse=feeding[2]
    feedmessage=feeding[3]
    if (feeding[0]):
        bot.send_message(message.chat.id, text="Potresti darci un feedback? " + polliceInSu + " o " + polliceInGiù,
                         reply_markup=emojiKeyboard)  # ask the user what he wants to do
        return [feedbot,feedresponse,feedmessage]  # if the user wants to give feedback, stop the function
    else:
        addLog(connection,cursor,message,feedmessage,feedresponse,feedbot)  # add the log into db
        return [feedbot,feedresponse,feedmessage]  # stop the function