from bs4 import BeautifulSoup
import requests

from functions import * 

'''
campeonatos = getCampeonatos()
'''
#Campeonato (FAZER UM FOR PARA PERCORRER OS CAMPEONATOS)
'''
temporadas = identificar_temporadas(campeonatos[1]) ##recebe um array com o link para cada temporada do campeonato
'''
#fazer fatiamento das temporadas
#Temporada (FAZER UM FOR PARA PERCORRER AS TEMPORADAS)
'''
jogos = identificar_jogos(temporadas[0]) ##recebe um array com o link para cada jogo da temporada
'''
#jogo = jogos[253] #segundo amarelo
#jogo = jogos[360] #dois vermelhos

jogo = 'https://www.academiadasapostasbrasil.com/stats/match/inglaterra/barclays-premier-league/norwich-city/burnley/3029438/live'
#jogo_segundo_amarelo = 'https://www.academiadasapostasbrasil.com/stats/match/inglaterra/barclays-premier-league/wolverhampton/leicester-city/3029332/live'
#jogo_3 = 'https://www.academiadasapostasbrasil.com/stats/match/alemanha/bundesliga/borussia-dortmund/hoffenheim/3047317/live'

r = requests.get(jogo)
soup = BeautifulSoup(r.content, 'html.parser')

##VARIÁVEL
#--------------------
#nome do campeonato disputado
nome_campeonato = soup.find('td', class_="stats-game-head-date").find_all('li')[4].text.strip()
#--------------------

time_a = soup.find('div', id="team_A_")
time_b = soup.find('div', id="team_B_")

expulsoes_time_mandante = identificar_minuto_expulsoes(time_a)
expulsoes_time_visitante = identificar_minuto_expulsoes(time_b)

##VARIÁVEIS
#--------------------
#minuto das expulsoes
expulsao_mandante_um = expulsoes_time_mandante[0][0]
expulsao_mandante_dois = expulsoes_time_mandante[0][1]
expulsao_mandante_tres = expulsoes_time_mandante[0][2]
expulsao_mandante_quatro = expulsoes_time_mandante[0][3]

expulsao_visitante_um = expulsoes_time_visitante[0][0]
expulsao_visitante_dois = expulsoes_time_visitante[0][1]
expulsao_visitante_tres = expulsoes_time_visitante[0][2]
expulsao_visitante_quatro = expulsoes_time_visitante[0][3]
#--------------------

minuto_gols_time_mandante = verifica_tempo_gols(time_a)
minuto_gols_time_visitante = verifica_tempo_gols(time_b)
minutos_expulsoes = sorted(expulsoes_time_mandante[1] + expulsoes_time_visitante[1])
placares_no_momento_da_expulsao = verifica_placares_momentaneos(minutos_expulsoes, minuto_gols_time_mandante, minuto_gols_time_visitante)


expulsoes = []
for minuto in expulsoes_time_mandante[1]:
    expulsoes.append([minuto, 'Mandante'])
for minuto in expulsoes_time_visitante[1]:
    expulsoes.append([minuto, 'Visitante'])

expulsoes_verificar_cartao = sorted(expulsoes, key=lambda x:x[0])

for i in range(8 - len(expulsoes_verificar_cartao)):
    expulsoes_verificar_cartao.append([None, None])


#VARIÁVEL
#--------------------
#número de expulsões durante o jogo
quantidade_expulsoes = len(minutos_expulsoes)
#--------------------

##VARIÁVEIS
#--------------------
#quem tomou o cartão (mandante ou visitante)
expulsao_um_m_v = expulsoes_verificar_cartao[0][1]
expulsao_dois_m_v = expulsoes_verificar_cartao[1][1]
expulsao_tres_m_v = expulsoes_verificar_cartao[2][1]
expulsao_quatro_m_v = expulsoes_verificar_cartao[3][1]
expulsao_cinco_m_v = expulsoes_verificar_cartao[4][1]
expulsao_seis_m_v = expulsoes_verificar_cartao[5][1]
expulsao_sete_m_v = expulsoes_verificar_cartao[6][1]
expulsao_oito_m_v = expulsoes_verificar_cartao[7][1]
#--------------------

##VARIÁVEIS
#--------------------
#placares no momento da expulsão
placar_expulsao_um = placares_no_momento_da_expulsao[0]
placar_expulsao_dois = placares_no_momento_da_expulsao[1]
placar_expulsao_tres = placares_no_momento_da_expulsao[2]
placar_expulsao_quatro = placares_no_momento_da_expulsao[3]
placar_expulsao_cinco = placares_no_momento_da_expulsao[4]
placar_expulsao_seis = placares_no_momento_da_expulsao[5]
placar_expulsao_sete = placares_no_momento_da_expulsao[6]
placar_expulsao_oito = placares_no_momento_da_expulsao[7]
#--------------------
##ESTATISTICAS
jogo = jogo[:-5]
r = requests.get(jogo)
soup = BeautifulSoup(r.content, 'html.parser')

classificacao = soup.find('table', class_="results")

##VARIÁVEIS
#--------------------
#posicao dos times no campeonato
posicao_atual_time_mandante = classificacao.find("tr", {"style":"background-color: #CDDFF0"}).find('td').get_text().strip()
posicao_atual_time_visitante = classificacao.find("tr", {"style":"background-color: #FFE0A6"}).find('td').get_text().strip()
#--------------------
print(posicao_atual_time_mandante)
print(posicao_atual_time_visitante)














