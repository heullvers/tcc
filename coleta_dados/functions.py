from bs4 import BeautifulSoup
import requests


def getCampeonatos():
    campeonatos = ['https://www.academiadasapostasbrasil.com/stats/competition/brasil/26', 'https://www.academiadasapostasbrasil.com/stats/competition/inglaterra/8',
    'https://www.academiadasapostasbrasil.com/stats/competition/espanha/7', 'https://www.academiadasapostasbrasil.com/stats/competition/alemanha/9', 
    'https://www.academiadasapostasbrasil.com/stats/competition/portugal/63', 'https://www.academiadasapostasbrasil.com/stats/competition/franca/16',
    'https://www.academiadasapostasbrasil.com/stats/competition/italia/13']

    return campeonatos

def identificar_temporadas(url_campeonato):
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

    return link_alternar_temporadas


def identificar_jogos(url_temporada):
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

    link_jogos = []
    for pagina in link_paginas_jogos:
        r = requests.get(pagina)
        soup = BeautifulSoup(r.content, 'html.parser')
        jogos = soup.find('table', class_="competition-rounds").find_all('tr')
        
        for jogo in jogos:
            ficha = jogo.find(class_="aa-icon-player") #icone de ficha do jogo
            if(ficha):
                placar_info = jogo.find_all('td')[3] #informacoes do placar
                placar = placar_info.text.strip() #placar do jogo
                em_andamento = placar_info['class'] #vetor com as classes de placar

                if((placar != 'Postponed') and ('gameinlive' not in em_andamento)): #existe ficha do jogo, jogo não foi adiado, jogo não está em andamento
                    link = ficha.parent #o pai do elemento ficha, possui o link do jogo
                    link = link['href']
                    link_jogos.append(link)

    return link_jogos