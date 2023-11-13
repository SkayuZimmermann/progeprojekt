import pygame
from pygame import mixer
import math
import random
import sys

pygame.init()
clock = pygame.time.Clock()
FPS = 60

#mängu ekraan
laius = 747
pikkus = 980
ekraan = pygame.display.set_mode((laius, pikkus))
pygame.display.set_caption("Proge mäng")

#taustapilt
taustapilt = pygame.image.load("taustapilt.png")
taustapilt_rect = taustapilt.get_rect()

taustapilt_y = 0


#auto, mängija
auto = pygame.image.load("auto.png")
mängija_asukoht1 = 320
mängija_asukoht2 = 850
#auto seisab alguses
mängija_asukoha_vahetus1 = 0
mängija_asukoha_vahetus2 = 0

def mängija():
    ekraan.blit(auto,(mängija_asukoht1, mängija_asukoht2))




#mängu tsükkel
running = True
while running:
    
    clock.tick(FPS)
    # liikuv taustapilt
    taustapilt_y += 5
    if taustapilt_y >= pikkus:
        taustapilt_y = 0

    ekraan.blit(taustapilt, (0, taustapilt_y - pikkus))
    ekraan.blit(taustapilt, (0, taustapilt_y))
    mängija()

    pygame.display.flip()

    

    # mängu sulgemine

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # auto liikumine w, a, s, d nuppude abil

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                mängija_asukoha_vahetus1 = -5
            if event.key == pygame.K_d:
                mängija_asukoha_vahetus1 = 5
            if event.key == pygame.K_w:
                mängija_asukoha_vahetus2 = -5
            if event.key == pygame.K_s:
                mängija_asukoha_vahetus2 = 5

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a or event.key == pygame.K_d:
                mängija_asukoha_vahetus1 = 0
            if event.key == pygame.K_w or event.key == pygame.K_s:
                mängija_asukoha_vahetus2 = 0

    mängija_asukoht1 += mängija_asukoha_vahetus1
    mängija_asukoht2 += mängija_asukoha_vahetus2 

    # et auto ekraanist välja ei sõidaks
    if mängija_asukoht1 <= -20:
        mängija_asukoht1 = -20
    elif mängija_asukoht1 >= 639:
        mängija_asukoht1 = 639
    if mängija_asukoht2 >= 852:
        mängija_asukoht2 = 852
    elif mängija_asukoht2 <= 0:
        mängija_asukoht2 = 0

    pygame.display.update()