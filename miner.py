from pygame import *
import pygame
from mp3_tagger import MP3File,VERSION_1,VERSION_2,VERSION_BOTH
mp3 = MP3File('test.mp3')
file = 'zed.mp3'
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load(file)
pygame.mixer.music.play()
while mixer.music.get_busy():
	time.Clock().tick(10)
#pygame.event.wait()
file = 'amerika.mp3'
pygame.mixer.music.load(file)
pygame.mixer.music.play()
while mixer.music.get_busy():
	time.Clock().tick(10)
#pygame.event.wait()
#mp3.artist = 'Mutskajeje'
tags = mp3.get_tags()
print(tags)
mp3.save()
