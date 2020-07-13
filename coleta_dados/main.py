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

#link da primeira página
link_ver_jogos = url_temporada + '/all-games'
r = requests.get(link_ver_jogos)
soup = BeautifulSoup(r.content, 'html.parser')

#identifica quantidade de páginas a percorrer
qnt_paginas = soup.find('div', class_="pagination")
if(not qnt_paginas):
    qnt_paginas = 1
else:
    qnt_paginas = qnt_paginas.ul.find_all('li')
    qnt_paginas = len(qnt_paginas) - 2

#guarda o link das páginas com os jogos
link_paginas_jogos = []
link_paginas_jogos.append(link_ver_jogos)

#manipulação para a criação da url da página que exibe os jogos
for i in range(2, qnt_paginas + 1, 1):
    url = link_ver_jogos + '/page/' + str(i)
    link_paginas_jogos.append(url)
    










'''

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


##Ao verificar se existe dados do jogo pra capturar, verificar se existe ficha, verificar se existe se jogo foi adiado (pois nesses jogos existe ficha), verificar se jogo está em andamento
for jogo in jogos:
    ficha = jogo.find(class_="aa-icon-player") #icone de ficha do jogo

    placar_info = jogo.find_all('td')[3]
    placar = placar_info.text.strip() #placar do jogo
    em_andamento = placar_info['class'] #vetor com as classes de placar
    
    if((ficha) and (placar != 'Postponed') and ('gameinlive' not in em_andamento)): #existe ficha do jogo, jogo não foi adiado, jogo não está em andamento
        link = jogo.find_all('td')[6].find('a')['href'] #posição 6 pois sempre é o sexta coluna(td) dentro da linha(tr)
        link_jogos.append(link)

#Jogo (FAZER UM FOR PARA PERCORRER OS JOGOS)
jogo = link_jogos[0]
'''











