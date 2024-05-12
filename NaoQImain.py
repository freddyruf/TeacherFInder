import time

import naoqi
import paramiko
import speech_recognition as sr

from __datafunction import *
from __keyboardsfunction import keyboardsgen
from __stringworksfunction import *


Host = "192.168.66.218"
ftpUsername = "nao"
ftpPw = "pepper"

localpath = 'records/record.wav'
remotepath = '/home/nao/record.wav'

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(Host, username=ftpUsername, password=ftpPw)
sftp = ssh.open_sftp()

robot = naoqi.ALProxy("ALAudioRecorder", Host, 9559)
robot.stopMicrophonesRecording()


connection = create_connection("localhost", "root", "")

cursor = connection.cursor(buffered=True) #cursor /Read-only attribute describing the result of a query.

response_data = load_json("_riconoscimento_messaggio.json")

keyboards=keyboardsgen(cursor) #ottengo le liste dei professori
tastiera1=keyboards[0]
tastiera2=keyboards[1]
tastiera3=keyboards[2]
tastiera4=keyboards[3]
allKeyboard=keyboards[4] #contiene semplicemente tutti i professori

r = sr.Recognizer("it-IT")

def processInfo(text,inQuestoMomento): #dal messaggio iniziale ottengo il risultato e lo preparo al invio
    professore = mostSimilarFromList(
        text.upper(),
        allKeyboard)  # trovo il nome del professore
    if (inQuestoMomento): #se sto cercando per ora
        ora = -1
        giorno = -1
    else:
        ora = FindTime(text)  # search the time
        giorno = findDay(text)  # search the day

    info = prof_info(professore, ora,
                     giorno)  # get the info about the professor (ora and giorno can be '-1' if not found)

    if not isinstance(info, dict):  # se non è un dizionario, allora è il messaggio completo da inviare al utente
        output = info

    else:  # if he is in school
        output = f"Il prof {professore.title()} si trova nella classe {info['Classe']} in palazzina: {info['Palazzina']}, piano: {info['Piano']}, aula: {info['Aula']}"

    return output


#main
if __name__ == "__main__":

    while True:

        robot.say("In ascolto")
        print("In ascolto \n\n")
        robot.startMicrophonesRecording("/home/nao/record.wav", "wav", 16000, (0, 0, 1, 0))
        time.sleep(5)
        robot.stopMicrophonesRecording()
        print("ascoltato \n\n")

        sftp.get(remotepath, localpath)

        try:
            # Ascolta l'audio dal microfono
            audiofile = sr.WavFile("records/record.wav")

            with audiofile as source: # riconoscimento vocale
                r.adjust_for_ambient_noise(source)
                X = r.record(source)
                text = r.recognize(X)
            print(text)

            response = get_response(text, response_data)  # cerca di capire cosa è stato chiesto
            type = response[1]  # tipo ti risposta, es "ricerca professore" o "saluto"
            response = response[0]  # risposta, es "ciao" o "tutto bene"

            inQuestoMomento = FindIfOnlyName(text, allKeyboard)  #se è stata specificata l'ora, return:boolean
            if (response == "ricerca professore"):  # se sta cercando un professore
                output = processInfo(text, inQuestoMomento)

            else:  # se non sta cercando un professore
                output = response

            addLog(connection, cursor, text, response, output)  # aggiorno il log

            robot.say(output)

        except KeyboardInterrupt:
            print("Stoppato!")
            break
        except sr.UnknownValueError:
            robot.say("Non riesco a capire cio che dici")
        except sr.RequestError as e:
            print(f"Errore nella richiesta al servizio di riconoscimento vocale: {e}")
        except Error as e:
            print(e)

    sftp.close()
    ssh.close()






