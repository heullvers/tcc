from bs4 import BeautifulSoup
import requests

url_campeonato = 'https://www.academiadasapostasbrasil.com/stats/competition/espanha/7'
r = requests.get(url_campeonato)

soup = BeautifulSoup(r.content, 'html.parser')

#Identificação do código das temporadas para que possar ser analisado cada temporada de um campeonato
options_temporadas = soup.find('ul', class_="search-filters").find('select').find_all('option')
codigo_temporadas = []
for option in options_temporadas:
    codigo_temporadas.append(option['value']) 


link_alternar_temporadas = []
for codigo in codigo_temporadas:
    link = url_campeonato + '/' + codigo
    link_alternar_temporadas.append(link)

#Primeira temporada (FAZER UM FOR PARA PERCORRER AS TEMPORADAS)
url_temporada = link_alternar_temporadas[0]
r = requests.get(url_temporada)
soup = BeautifulSoup(r.content, 'html.parser')

rodada_dados = soup.find('tr', class_="competition-tr-title")

#Captura o link para alternar entre as rodadas
link_alternar_rodada = rodada_dados.find('td', id="week-gr").find(class_="group-url")['value']

#Captura a rodada atual se o campeonato estiver em andamento, ou a última rodada se o campeonato já estiver encerrado
ultima_rodada = int(rodada_dados.find('td', id="week-gr").span.text)

#Links das rodadas do ano
link_rodadas_do_ano = []
for i in range(ultima_rodada, 0, -1):
    link_rodada = link_alternar_rodada + str(i)
    link_rodadas_do_ano.append(link_rodada)

#Rodada (FAZER UM FOR PARA PERCORRER AS RODADAS)
url_rodada = link_rodadas_do_ano[1]
r = requests.get(url_rodada)
soup = BeautifulSoup(r.content, 'html.parser')

jogos = soup.find('table', class_="competition-rounds").find_all('tr')
link_jogos = []

##Ao verificar se existe dados do jogo pra capturar, verificar se existe ficha, e caso exista ficha verificar se tem placar
for jogo in jogos:
    ficha = jogo.find(class_="aa-icon-player")
    if(ficha): #existe ficha do jogo
        link = jogo.find_all('td')[6].find('a')['href']
        link_jogos.append(link)

print(link_jogos)












