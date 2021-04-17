import pygame
import sys
import asyncio
import websockets

pygame.init()

screen = pygame.display.set_mode((1920, 1080), pygame.RESIZABLE)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
           pygame.quit()
           sys.exit()
        elif event.type == pygame.VIDEORESIZE:
            pygame.display.update()

