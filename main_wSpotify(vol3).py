import pygame
from pygame import mixer
import math
import random
import sys
import time
import random

#spotify import
import spotipy
from spotipy.oauth2 import SpotifyOAuth

import os
#vahetab working directory faili asukoha directoriks
os.chdir(os.path.dirname(os.path.abspath(__file__)))
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
    ooteaeg = 1#sekundites
    result = None
    result = sp.current_user_playing_track()
    if result != None:
        return result
    else:
        print('Pane Spotifys laul käima')
        start_time = time.monotonic()
        while result == None and (start_time + ooteaeg > time.monotonic()):
            result = None
            result = sp.current_user_playing_track()
        if result == None:
            print('Sa ei pannud Spotifys laulu käima')
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
mängija_asukoht2 = 600
#auto seisab alguses
mängija_asukoha_vahetus1 = 0
mängija_asukoha_vahetus2 = 0
#mängu skoor alguses
skoor = 0

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
        global taustakiirus
        global taustapilt_y
        mängija_asukoha_vahetus1 = 0
        mängija_asukoha_vahetus2 = 0
        taustakiirus = 0
        taustapilt_y = 0
        mängu_lõpp()
    elif mängija_asukoht1 < 160 or mängija_asukoht1 > 480:
        mängija_asukoha_vahetus1 = 0
        mängija_asukoha_vahetus2 = 0
        taustakiirus = 0
        taustapilt_y = 0
        mängu_lõpp()



#praeguse laulu saamine
current_track = get_current_track()
if current_track == None:
    current_track = {'timestamp': 1700760967441, 'context': {'external_urls': {'spotify': 'https://open.spotify.com/artist/0du5cEVh5yTK9QJze8zA0C'}, 'href': 'https://api.spotify.com/v1/artists/0du5cEVh5yTK9QJze8zA0C', 'type': 'artist', 'uri': 'spotify:artist:0du5cEVh5yTK9QJze8zA0C'}, 'progress_ms': 4680, 'item': {'album': {'album_type': 'album', 'artists': [{'external_urls': {'spotify': 'https://open.spotify.com/artist/0du5cEVh5yTK9QJze8zA0C'}, 'href': 'https://api.spotify.com/v1/artists/0du5cEVh5yTK9QJze8zA0C', 'id': '0du5cEVh5yTK9QJze8zA0C', 'name': 'Bruno Mars', 'type': 'artist', 'uri': 'spotify:artist:0du5cEVh5yTK9QJze8zA0C'}], 'available_markets': ['AE', 'AG', 'AL', 'AR', 'AT', 'BA', 'BB', 'BD', 'BE', 'BG', 'BH', 'BO', 'BR', 'BS', 'BZ', 'CH', 'CL', 'CO', 'CR', 'CW', 'CY', 'CZ', 'DE', 'DK', 'DM', 'DO', 'DZ', 'EC', 'EE', 'EG', 'ES', 'FI', 'FR', 'GB', 'GD', 'GR', 'GT', 'GY', 'HN', 'HR', 'HT', 'HU', 'ID', 'IE', 'IL', 'IN', 'IQ', 'IS', 'IT', 'JM', 'JO', 'JP', 'KN', 'KR', 'KW', 'LB', 'LC', 'LI', 'LK', 'LT', 'LU', 'LV', 'LY', 'MA', 'ME', 'MK', 'MT', 'MX', 'NI', 'NL', 'NO', 'OM', 'PA', 'PE', 'PK', 'PL', 'PS', 'PT', 'PY', 'QA', 'RO', 'RS', 'SA', 'SE', 'SG', 'SI', 'SK', 'SR', 'SV', 'TN', 'TR', 'TT', 'UA', 'UY', 'VC', 'VE', 'XK', 'ZA'], 'external_urls': {'spotify': 'https://open.spotify.com/album/6J84szYCnMfzEcvIcfWMFL'}, 'href': 'https://api.spotify.com/v1/albums/6J84szYCnMfzEcvIcfWMFL', 'id': '6J84szYCnMfzEcvIcfWMFL', 'images': [{'height': 640, 'url': 'https://i.scdn.co/image/ab67616d0000b273f60070dce96a2c1b70cf6ff0', 'width': 640}, {'height': 300, 'url': 'https://i.scdn.co/image/ab67616d00001e02f60070dce96a2c1b70cf6ff0', 'width': 300}, {'height': 64, 'url': 'https://i.scdn.co/image/ab67616d00004851f60070dce96a2c1b70cf6ff0', 'width': 64}], 'name': 'Doo-Wops & Hooligans', 'release_date': '2010-10-05', 'release_date_precision': 'day', 'total_tracks': 12, 'type': 'album', 'uri': 'spotify:album:6J84szYCnMfzEcvIcfWMFL'}, 'artists': [{'external_urls': {'spotify': 'https://open.spotify.com/artist/0du5cEVh5yTK9QJze8zA0C'}, 'href': 'https://api.spotify.com/v1/artists/0du5cEVh5yTK9QJze8zA0C', 'id': '0du5cEVh5yTK9QJze8zA0C', 'name': 'Bruno Mars', 'type': 'artist', 'uri': 'spotify:artist:0du5cEVh5yTK9QJze8zA0C'}], 'available_markets': ['AE', 'AG', 'AL', 'AR', 'AT', 'BA', 'BB', 'BD', 'BE', 'BG', 'BH', 'BO', 'BR', 'BS', 'BZ', 'CH', 'CL', 'CO', 'CR', 'CW', 'CY', 'CZ', 'DE', 'DK', 'DM', 'DO', 'DZ', 'EC', 'EE', 'EG', 'ES', 'FI', 'FR', 'GB', 'GD', 'GR', 'GT', 'GY', 'HN', 'HR', 'HT', 'HU', 'ID', 'IE', 'IL', 'IN', 'IQ', 'IS', 'IT', 'JM', 'JO', 'JP', 'KN', 'KR', 'KW', 'LB', 'LC', 'LI', 'LK', 'LT', 'LU', 'LV', 'LY', 'MA', 'ME', 'MK', 'MT', 'MX', 'NI', 'NL', 'NO', 'OM', 'PA', 'PE', 'PK', 'PL', 'PS', 'PT', 'PY', 'QA', 'RO', 'RS', 'SA', 'SE', 'SG', 'SI', 'SK', 'SR', 'SV', 'TN', 'TR', 'TT', 'UA', 'UY', 'VC', 'VE', 'XK', 'ZA'], 'disc_number': 1, 'duration_ms': 189109, 'explicit': False, 'external_ids': {'isrc': 'USAT21001886'}, 'external_urls': {'spotify': 'https://open.spotify.com/track/386RUes7n1uM1yfzgeUuwp'}, 'href': 'https://api.spotify.com/v1/tracks/386RUes7n1uM1yfzgeUuwp', 'id': '386RUes7n1uM1yfzgeUuwp', 'is_local': False, 'name': 'The Lazy Song', 'popularity': 81, 'preview_url': 'https://p.scdn.co/mp3-preview/8a6cd6679fc2a388b989a09b571194723d45cb71?cid=93634ca4f50c4971827d1bd3cb13ce5d', 'track_number': 5, 'type': 'track', 'uri': 'spotify:track:386RUes7n1uM1yfzgeUuwp'}, 'currently_playing_type': 'track', 'actions': {'disallows': {'resuming': True}}, 'is_playing': True}

print(current_track)
current_track_features = get_audio_features(current_track['item']['id'])
#print(current_track_features['tempo'])
print(f'Praegu mängib: {current_track['item']['name']}')

#tekst ekraanile(praegu lihtsalt, et testida kas saab laulu)
font = pygame.font.SysFont('Arial', 15)
font2 = pygame.font.SysFont('Arial', 35)
def tekst_ekraanile(tekst, font, teksti_värv, x, y):
    väljund = font.render(tekst, True, teksti_värv)
    ekraan.blit(väljund, (x, y))

game_over = False
def mängu_lõpp():
    global game_over
    mängu_lõpp_font = pygame.font.SysFont('Arial', 50)
    väljund = mängu_lõpp_font.render("MÄNGU LÕPP", True, (255, 0, 0))
    ekraan.blit(väljund, (240, 400))
    font = pygame.font.SysFont('Arial', 25)
    restart = font.render("VAJUTA SPACEBAR, ET UUESTI MÄNGIDA", True, (255, 0, 0))
    ekraan.blit(restart, (200, 500))
    skoori_font = pygame.font.SysFont('Arial', 50)
    punktid = skoori_font.render("Sinu skoor on: "+str(skoor), True, (255, 0, 0))
    ekraan.blit(punktid, (230, 450))

    

    game_over = True


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

    #skoor ekraanile
    tekst_ekraanile(f'Skoor: {str(skoor)}', font2, (255, 0, 0), 610, 900)
    

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
            #kui vajutada spacebar, siis paneb mängija ning takistused algsetele koordinaatidele tagasi
            if event.key == pygame.K_SPACE and game_over:
                mängija_asukoht1 = 320 
                mängija_asukoht2 = 600
                mängija_asukoha_vahetus1 = 0
                mängija_asukoha_vahetus2 = 0
                taustakiirus = (int(((float(current_track_features['tempo']) - tempoMin) * taustakiirusRange) / tempoRange) + taustakiirusMin)
                taustapilt_y = 0
                heinapalli_asukoht1 = random.randint(220, 440)
                heinapalli_asukoht2 = 0 - 128
                skoor = 0
                game_over = False
            

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
        skoor += 1

        heinapalli_asukoht1 = random.randint(220, 440)

    #kui kiiresti heinapall auto suunas sõidab
    heinapalli_asukoht2 += taustakiirus

    
    pygame.display.update()