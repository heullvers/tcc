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

def identificar_minuto_expulsoes(time):
    minutos_expulsoes = []
    string = str(time).replace('tr&gt;','').replace('th&gt;','').replace('td&gt;','').replace('&lt;','').replace('&gt','').replace('/','').replace(';','').replace('span','').replace('undermark','').replace('overermark','').replace('class=','').replace('\""','').replace('.','')
    string_split = string.split()
    
    if (("aa-icon-RC'" in string_split) or ("aa-icon-Y2C'" in string_split)):
        posicao = 0
        posicoes = []
        for pos in string_split:
            if((pos == "aa-icon-RC'") or (pos == "aa-icon-Y2C'")):
                posicoes.append(posicao + 4)
            posicao += 1

        for pos in posicoes:
            minuto = string_split[pos]
            minuto = minuto.replace("'",'')
            if '+' in minuto:
                minuto = minuto.split('+')
                minuto = int(minuto[0])+ int(minuto[1])
            else:
                minuto = int(minuto)
            minutos_expulsoes.append(minuto)

    minutos_expulsoes_organizado = minutos_expulsoes[0:]
    
    for i in range(4- len(minutos_expulsoes)):
        minutos_expulsoes_organizado.append(None)

    ##retorna dois arrays, um organizado para as variáveis receberem os valores e outro que será usado para verificar os placares momentaneos posteriormente
    return [minutos_expulsoes_organizado, minutos_expulsoes]


def verifica_tempo_gols(time):
    minutos_gols = []
    gols_results_string = str(time).replace('tr&gt;','').replace('th&gt;','').replace('td&gt;','').replace('&lt;','').replace('&gt','').replace('/','').replace(';','').replace('span','').replace('undermark','').replace('overermark','').replace('class=','').replace('\""','').replace('.','')
    gols_results_string_split = gols_results_string.split()

    if ("aa-icon-G'" in gols_results_string_split) or ("aa-icon-PG'" in gols_results_string_split) or ("aa-icon-OG'" in gols_results_string_split):
        posicao = 0
        posicoes = []
        for pos in gols_results_string_split:
            if((pos == "aa-icon-PG'") or (pos == "aa-icon-G'") or (pos == "aa-icon-OG'")) :
                posicoes.append(posicao + 4)
            posicao += 1

        for pos in posicoes:
            minuto = gols_results_string_split[pos]
            minuto = minuto.replace("'",'')
            if '+' in minuto:
                minuto = minuto.split('+')
                minuto = int(minuto[0])+ int(minuto[1])
            else:
                minuto = int(minuto)
            minutos_gols.append(minuto)

    return minutos_gols

def verifica_placares_momentaneos(minutos_expulsoes, minutos_gols_time_a, minutos_gols_time_b):
    placar_no_momento_da_expulsao = []
    for minuto_expulsao in minutos_expulsoes:
        gols_time_a = 0
        gols_time_b = 0
        for minuto_gol in minutos_gols_time_a:
            if(minuto_expulsao >= minuto_gol):
                gols_time_a += 1
        for minuto_gol in minutos_gols_time_b:
            if(minuto_expulsao >= minuto_gol):
                gols_time_b += 1
        
        placar_no_momento = str(gols_time_a) + '-' + str(gols_time_b)
        placar_no_momento_da_expulsao.append(placar_no_momento)

    for i in range(8- len(placar_no_momento_da_expulsao)):
        placar_no_momento_da_expulsao.append(None)

    return placar_no_momento_da_expulsao

