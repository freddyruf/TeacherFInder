from moviepy.editor import *
import pygame
from moviepy.editor import VideoFileClip
import os

# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


string="Il prof Cesinaro Stefano si trova nella classe 5BI nel piano T della 5 palazzina nel aula 33"
string=string.lower()
listaParole=string.split()

#se la richiesta è gia stata fatta
if os.path.exists("/Users/federico/PycharmProjects/pythonProject/video_pronti"):
    final_clip = VideoFileClip("/Users/federico/PycharmProjects/pythonProject/video_pronti/"+string+".mp4")
else:

    lista=[]
    for word in listaParole: #trovo i video
        lista.append(VideoFileClip("/Users/federico/PycharmProjects/pythonProject/video_clip/"+word+".mp4"))
    #concateno i video
    final_clip = concatenate_videoclips(lista)
    #salvo i video nella cartella video_pronti
    final_clip_directory="/Users/federico/PycharmProjects/pythonProject/video_pronti/"+string+".mp4"
    final_clip.write_videofile(final_clip_directory)


# Inizializza Pygame
pygame.init()

# Carica il video
video = VideoFileClip(final_clip_directory)

# Inizializza la finestra di Pygame
screen = pygame.display.set_mode((video.size))

# Crea un oggetto per la riproduzione del video
video_player = video.preview()

# Crea una variabile per tenere traccia del tempo trascorso
clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    running=False
    # Aggiorna la finestra


    # Regola il clock per mantenere una velocità di riproduzione costante
    clock.tick(30)



# Chiudi Pygame
pygame.quit()



# See PyCharm help at https://www.jetbrains.com/help/pycharm/
