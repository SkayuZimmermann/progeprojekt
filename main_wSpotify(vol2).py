import pygame
from pygame import mixer
import math
import random
import sys

#spotify import
import spotipy
from spotipy.oauth2 import SpotifyOAuth
#import os

"""
#id-d environment id-d (seda pole tegelt vaja aga mingi tutorial soovitas)
os.environ['CLIENT_ID'] = '93634ca4f50c4971827d1bd3cb13ce5d'
os.environ['CLIENT_SECRET'] = '154b96ee8635450ca9cf98365964d339'
os.environ['REDIRECT_URI'] = 'http://localhost:7777/callback'

#võtab id-d
client_id = os.environ.get('CLIENT_ID')
client_secret = os.environ.get('CLIENT_SECRET')
redirect_uri = os.environ.get('REDIRECT_URI')
"""
#meie projekti id-d
client_id = '93634ca4f50c4971827d1bd3cb13ce5d'
client_secret = '154b96ee8635450ca9cf98365964d339'
redirect_uri = 'http://localhost:7777/callback'

#lubade scope, mida küsib
scope = 'user-read-currently-playing'

#saab sisselogimisõigused ja tokenid
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id = client_id,
                                               client_secret=client_secret,
                                               redirect_uri=redirect_uri,
                                               scope=scope)
)
#preagu mängiva laulu andmed
def get_current_track():
    result = sp.current_user_playing_track()
    return result
#saab laulu andmed nagu tempo, liveliness, energy jne
def get_audio_features(song_id):
   result = sp.audio_features(song_id)
   return result[0]


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
mängija_asukoht2 = 800
#auto seisab alguses
mängija_asukoha_vahetus1 = 0
mängija_asukoha_vahetus2 = 0

def mängija():
    ekraan.blit(auto,(mängija_asukoht1, mängija_asukoht2))

# takistus
heinapall = pygame.image.load("hay.png")
heinapalli_asukoht1 = random.randint(220, 440)
heinapalli_asukoht2 = 0 - 128

takistuse_kiirus_Y_teljel = 8

def takistus():
    ekraan.blit(heinapall,(heinapalli_asukoht1, heinapalli_asukoht2))

#kui auto puutub heinakuhjaga kokku

def põrge(mängija_asukoht1, mängija_asukoht2, heinapalli_asukoht1, heinapalli_asukoht2):
    if abs(mängija_asukoht1 - heinapalli_asukoht1) < 64 and abs(mängija_asukoht2 - heinapalli_asukoht2) < 64:
        global mängija_asukoha_vahetus1
        global mängija_asukoha_vahetus2
        global takistuse_kiirus_Y_teljel
        global taustapilt_y
        mängija_asukoha_vahetus1 = 0
        mängija_asukoha_vahetus2 = 0
        takistuse_kiirus_Y_teljel = 0
        taustapilt_y = 0
        mängu_lõpp()


    
#praeguse laulu saamine
current_track = get_current_track()
current_track_features = get_audio_features(current_track['item']['id'])
print(current_track_features['tempo'])
if current_track == None:
    print('Pane Spotifys laul käima')
    while current_track == None:
        current_track = get_current_track()
print(f'Praegu mängib: {current_track['item']['name']}')

#tekst ekraanile(praegu lihtsalt, et testida kas saab laulu)
font = pygame.font.SysFont('Arial', 15)
def tekst_ekraanile(tekst, font, teksti_värv, x, y):
    väljund = font.render(tekst, True, teksti_värv)
    ekraan.blit(väljund, (x, y))

mängu_lõpp_font = pygame.font.SysFont('Arial', 50)
def mängu_lõpp():
    väljund = mängu_lõpp_font.render("MÄNGU LÕPP", True, (255, 0, 0))
    ekraan.blit(väljund, (240, 400))


        
#tausta liikumiskiirus
#paramaatrid
tempoMin = 50
tempoMax = 180
tempoRange = (tempoMax - tempoMin)

taustakiirusMin = 1
taustakiirusMax = 10
taustakiirusRange = (taustakiirusMax - taustakiirusMin)
#taustakiiruse arvutamine
taustakiirus = (int(((float(current_track_features['tempo']) - tempoMin) * taustakiirusRange) / tempoRange) + taustakiirusMin)


#mängu tsükkel
running = True
while running:
    
    clock.tick(FPS)
    # liikuv taustapilt
    taustapilt_y += taustakiirus
    #taustapilt_y += 5
    if taustapilt_y >= pikkus:
        taustapilt_y = 0

    ekraan.blit(taustapilt, (0, taustapilt_y - pikkus))
    ekraan.blit(taustapilt, (0, taustapilt_y))
    mängija()
    takistus()
    põrge(mängija_asukoht1, mängija_asukoht2, heinapalli_asukoht1, heinapalli_asukoht2)
    
    

    pygame.display.flip()

    #laulu info ekraanile
    tekst_ekraanile(f'Praegune laul: {current_track['item']['name']}', font, (0, 0, 0), 50, 50)
    tekst_ekraanile(f'Tempo: {int(current_track_features['tempo'])} BPM, {taustakiirus} pixels/frame', font, (0, 0, 0), 80, 70)

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

    # uus heinakuhi tuleb ülevalt alla
    if (heinapalli_asukoht2 >= pikkus - 0 and heinapalli_asukoht2 <= (pikkus +200)):
        heinapalli_asukoht2 = 0 - 128

        heinapalli_asukoht1 = random.randint(220, 240)

    #kui kiiresti heinapall auto suunas sõidab
    heinapalli_asukoht2 += takistuse_kiirus_Y_teljel

    pygame.display.update()