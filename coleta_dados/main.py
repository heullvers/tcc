from bs4 import BeautifulSoup
import requests

from functions import identificar_temporadas, identificar_jogos, getCampeonatos

campeonatos = getCampeonatos()

#Campeonato (FAZER UM FOR PARA PERCORRER OS CAMPEONATOS)
temporadas = identificar_temporadas(campeonatos[1]) ##recebe um array com o link para cada temporada do campeonato

#fazer fatiamento das temporadas
#Temporada (FAZER UM FOR PARA PERCORRER AS TEMPORADAS)
jogos = identificar_jogos(temporadas[0]) ##recebe um array com o link para cada jogo da temporada

jogo = jogos[369]
print(jogo)












