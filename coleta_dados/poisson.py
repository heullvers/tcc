from math import e
import math

##formula
def poisson(forca, provavel):
    poisson = ((forca**provavel) * (e**(-1.0 * forca)))/ (math.factorial(provavel))
    return round(poisson,2)

def resultado_final(matriz):
    probabilidades = [0,0,0] #empate, mandante, visitante

    for i in range(len(matriz)):
        for j in range(len(matriz[i])):
            if(i == j): #empate
                probabilidades[0] += matriz[i][j]
            elif(i > j): #mandante ganhar
                probabilidades[1] += matriz[i][j]
            else: #visitante ganhar
                probabilidades[2] += matriz[i][j]

    maior = max(probabilidades)
    maior_pos = probabilidades.index(maior)

    if(maior_pos == 0):
        return 'Empate'
    elif(maior_pos == 1):
        return 'Mandante'
    else:
        return 'Visitante'

def qnt_gols_exatos(matriz):
    probabilidades = [0,0,0,0,0,0] #gols exatos, 0, 1, 2, 3, 4, mais que 4 gols

    for i in range(len(matriz)):
        for j in range(len(matriz[i])):
            if((i + j) == 0):
                probabilidades[0] += matriz[i][j] 
            elif((i + j) == 1):
                probabilidades[1] += matriz[i][j]
            elif((i + j) == 2):
                probabilidades[2] += matriz[i][j]
            elif((i + j) == 3):
                probabilidades[3] += matriz[i][j]
            elif((i + j) == 4):
                probabilidades[4] += matriz[i][j]
            else:
                probabilidades[5] += matriz[i][j]

    maior = max(probabilidades)
    maior_pos = probabilidades.index(maior)

    if(maior_pos == 5):
        return '4 ou mais'
    else:
        return maior_pos

def ambas_marcam(matriz):
    ambas_marcam = 0
    for i in range(len(matriz)):
        for j in range(len(matriz[i])):
            if((i != 0) and (j != 0)):
                ambas_marcam += matriz[i][j]
    return round(ambas_marcam,2)

def imprimirMatriz(matriz):
    for linha in matriz:
        for elemento in linha:
            print(elemento, end=' ')
        print('\n')

    

total_gols_feitos_mandante_liga = 525
total_gols_feitos_visitante_liga = 302
qnt_jogos = 380

#inicio do calculo para a capacidade ofensiva
media_gols_feitos_mandante_liga = total_gols_feitos_mandante_liga/qnt_jogos
media_gols_feitos_visitante_liga = total_gols_feitos_visitante_liga/qnt_jogos

#inicio do calculo para a capacidade defensiva
media_gols_sofridos_mandante_liga = media_gols_feitos_visitante_liga
media_gols_sofridos_visitante_liga = media_gols_feitos_mandante_liga

###partida analisada
lista1 = [1.44, 0.72, 1.33, 1.33, 2.22, 1.06, 1, 0.56, 1.56, 0.89] #media gols feitos em casa pelo mandante
lista2 = [1.33, 1.06, 1.28, 1.67, 0.83, 1.61, 1.44, 1.17, 1, 0.94] #media gols sofridos fora pelo visitante
lista3 = [0.89, 1.06, 1.06, 1, 1.67, 0.78, 0.67, 1.39, 1.33, 0.78] #media gols feitos fora visitante
lista4 = [0.78, 0.83, 0.89, 0.61, 0.83, 1.17, 0.89, 1.33, 1.17, 1.22] #media gols sofridos em casa pelo mandante

resultados = []
gols_exatos = []
ambas_equipes_marcam = []

for i in range(10):
    
    media_gols_feitos_mandante =  lista1[i] #0.72 #media gols feitos em casa pelo mandante
    #capacidade ofensiva do mandante
    capacidade_ofensiva_mandante = media_gols_feitos_mandante/media_gols_feitos_mandante_liga

    media_gols_sofridos_visitante = lista2[i] #1.06 #media gols sofridos fora pelo visitante
    ##capacidade defensiva do visitante
    capacidade_defensiva_visitante = media_gols_sofridos_visitante/media_gols_sofridos_visitante_liga


    #capacidade ofensiva do visitante
    media_gols_feitos_visitante = lista3[i] #1.06 #media gols feitos fora visitante
    capacidade_ofensiva_visitante = media_gols_feitos_visitante/media_gols_feitos_visitante_liga

    media_gols_sofridos_mandante = lista4[i] #0.83 #media gols sofridos em casa pelo mandante
    #capacidade defensiva do mandante
    capacidade_defensiva_mandante = media_gols_sofridos_mandante/media_gols_sofridos_mandante_liga

    ##Gols feitos pelo mandante
    qnt_gols_predita_mandante = capacidade_ofensiva_mandante * capacidade_defensiva_visitante * media_gols_feitos_mandante_liga

    ##Gols feitos pelo visitante
    qnt_gols_predita_visitante = capacidade_ofensiva_visitante * capacidade_defensiva_mandante * media_gols_feitos_visitante_liga

    ##POISSON
    range_de_gols = 6 #(0 a 5)

    possibilidades_mandante = []
    possibilidades_visitante = []

    for i in range(range_de_gols):
        resultado_mandante = poisson(qnt_gols_predita_mandante, i)
        resultado_visitante = poisson(qnt_gols_predita_visitante, i)
        possibilidades_mandante.append(resultado_mandante)
        possibilidades_visitante.append(resultado_visitante)

    ##DISTRIBUIÇÃO DE POISSON
    matriz = []
    for prob_mandante in possibilidades_mandante:
        linha = []
        for prob_visitante in possibilidades_visitante:
            probabilidade = round(prob_mandante * prob_visitante,2)
            linha.append(probabilidade)
        matriz.append(linha)

    



    





    resultado = resultado_final(matriz)
    gol_exato = qnt_gols_exatos(matriz)
    ambas_mar = ambas_marcam(matriz)
    resultados.append(resultado)
    gols_exatos.append(gol_exato)
    ambas_equipes_marcam.append(ambas_mar)

#print(resultados)
#print(gols_exatos)
print(ambas_equipes_marcam)


        










