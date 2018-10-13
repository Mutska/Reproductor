from pygame import *
import pygame

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