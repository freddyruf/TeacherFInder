from __datafunction import create_connection, feedbacktry, addLog
from __keyboardsfunction import keyboardsgen
import time
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
def sand(cursor,connection,nome,time):
    global output
    global feedresponse
    global feedmessage

    nome = mostSimilarFromList(
        nome, allKeyboard)  # modify the message text to the name of the professor (to work in some functions)
    ora=time.tm_hour
    giorno=time.tm_wday+1
    info = prof_info(nome, ora,
                     giorno)  # get the info about the professor (ora and giorno can be '-1' if not found)

    if not isinstance(info, dict):  # if the professor is not in a class
        output = info
        cursor.send(output.encode('utf-8'))

    else:  # if he is in school
        output = f"{info['Classe']};{info['Palazzina']};{info['Piano']};{info['Aula']}"
        cursor.send(output.encode('utf-8'))




    feeding = feedbacktry(nome, "From server", output)  # ask for feedback
    feedoutput = feeding[1]
    feedresponse = feeding[2]
    feedmessage = feeding[3]
    if (feeding[0]):
        cursor.send(b"Potresti darci un feedback?")
    else:
        addLog(connection,cursor,feedmessage,feedresponse,output)  # add the log into db

    return [output, feedresponse, feedmessage]


def sandOne(connection,response,message):
    global output
    global output
    global feedresponse
    global feedmessage
    connection.send(response)
    output = response  # save the response

    feeding = feedbacktry(message, type, output)  # ask for feedback
    output=feeding[1]
    feedresponse=feeding[2]
    feedmessage=feeding[3]
    if (feeding[0]):
        connection.send(b"Potresti darci un feedback?")

    else:
        addLog(connection,cursor,feedmessage,feedresponse,output)  # add the log into db

    return [output,feedresponse,feedmessage]  # stop the function