import sys
import threading

from __datafunction import *
import pygame
from moviepy.editor import VideoFileClip
from moviepy.editor import concatenate_videoclips
import os
import speech_recognition as sr
from displaywork import *
from __keyboardsfunction import keyboardsgen


#ID: 1 = richiestaa prof


connection = create_connection("localhost", "root", "")
#}}} closing the connection function

cursor = connection.cursor(buffered=True) #cursor /Read-only attribute describing the result of a query.


response_data = load_json("../_riconoscimento_messaggio.json")

keyboards=keyboardsgen(cursor)
allKeyboard=keyboards[4]

screen_width, screen_height = pygame.display.Info().current_w, pygame.display.Info().current_h


pygame.init()
#fullscreen


#set as fullscreen with the dimesion of the screen
screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)

sfondo = pygame.image.load("sfondo.jpg")


pygame.transform.scale(sfondo, (screen_width, screen_height))


recognizer = sr.Recognizer()


while True:


    #fullscreen mode
    screen = pygame.display.set_mode(sfondo.get_size())
    pygame.display.flip()


    # Ascolta l'audio dal microfono
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Ascolto")
        audio = recognizer.listen(source, timeout=None, phrase_time_limit=5)


    try:
        #close when esc is pressed



        # load loading video and play it
        #loading_video = VideoFileClip("loading.mp4")
        #pygame.display.set_mode(loading_video.size)
        #pygame.display.set_caption("Loading")
        #loading_video.preview()
        # Utilizza il riconoscimento vocale di Google per trascrivere l'audio
        text = recognizer.recognize_google(audio, language="it-IT")  # Specifica la lingua
        print("Testo trascritto: " + text)
        response = get_response(text,
                                response_data)  # get the type of message and the response(usable if he isn't asking a professor)
        type = response[1]  # get the type of message
        response = response[0]  # get the response

        inQuestoMomento = FindIfOnlyName(text, allKeyboard) #se m ista chiedendo dove sta ora
        if (response == "ricerca professore"):  # if is searching a professor
            output=sand(connection,cursor, text,type,inQuestoMomento)

        else:  # if the message else
            output=response

        addLog(connection,cursor,text,response,output)  # add the log into db
        #lowercase the output
        output=output.lower()
        print(output)
        listaParole = output.split()
        output=output.replace(" ","_") #sostituisco gli spazi con _ per il nome del video



        # se la richiesta è gia stata fatta
        if os.path.exists("/Users/federico/Library/Mobile Documents/com~apple~CloudDocs/Lavori/DB/VoltaBot/video_pronti/" + output + ".mp4"):
            video_da_caricamento = VideoFileClip("/Users/federico/Library/Mobile Documents/com~apple~CloudDocs/Lavori/DB/VoltaBot/video_pronti/" + output + ".mp4")
            final_clip_directory = "/Users/federico/Library/Mobile Documents/com~apple~CloudDocs/Lavori/DB/VoltaBot/video_pronti/" + output + ".mp4"
        else:


            lista = []
            for word in listaParole:  # trovo i video
                lista.append(VideoFileClip("/Users/federico/Library/Mobile Documents/com~apple~CloudDocs/Lavori/DB/VoltaBot/video_clip/" + word + ".mp4"))
            # concateno i video
            video_da_caricamento = concatenate_videoclips(lista)
            # salvo i video nella cartella video_pronti
            final_clip_directory = "/Users/federico/Library/Mobile Documents/com~apple~CloudDocs/Lavori/DB/VoltaBot/video_pronti/" + output + ".mp4"
            video_da_caricamento.write_videofile(final_clip_directory)

            video_da_caricamento = VideoFileClip(final_clip_directory)

            # Inizializza la finestra di Pygames
        screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)

           # Crea un oggetto per la riproduzione del video
        video_player = video_da_caricamento.preview()


        #pygame.transform.scale(video_player, (screen_width, screen_height))




            # Crea una variabile per tenere traccia del tempo trascorso
        clock = pygame.time.Clock()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                # Aggiorna la finestra

                # Regola il clock per mantenere una velocità di riproduzione costante
            clock.tick(30)
            #display sfondo

    except sr.UnknownValueError:
        print("Impossibile riconoscere l'audio")
    except sr.RequestError as e:
        print(f"Errore nella richiesta al servizio di riconoscimento vocale: {e}")
    except Error as e:
        print(e)

pygamw.quit()




