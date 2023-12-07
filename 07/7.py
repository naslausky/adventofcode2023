# Desafio do dia 07/12/2023:
# a) Receber uma lista de mãos de poker, com sua respectiva aposta. Ordenar todas e calcular a pontuação total.
# b) Idem porém agora interpretando a carta 'J' como coringa.

maos = []
with open('input.txt') as file:
	linhas = file.read().splitlines()
for linha in linhas:
	mao, aposta = linha.split()
	aposta = int(aposta)
	maos.append((mao, aposta))

def posicaoDaMao(mao, considerarCoringas = False): # Função que recebe uma mão e converte para um objeto comparável.
	coringa = 'J'
	if considerarCoringas: # Configura a ordem de valor das cartas.
		cartas = ['A', 'K', 'Q', 'T', '9', '8', '7', '6', '5', '4', '3', '2', coringa]
	else:
		cartas = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']

	contagemCartas = {carta: mao.count(carta) for carta in mao 
						if (carta != coringa or not considerarCoringas)} # Necessário para a parte 2.
	quantidadeDeCoringas = mao.count(coringa)
	contagemCartas = list(sorted(contagemCartas.values(), reverse = True))
	if not contagemCartas:
		contagemCartas = [0]
	if considerarCoringas:
		contagemCartas[0] += quantidadeDeCoringas
	contagemCartas = tuple(contagemCartas) # Passo desnecessário.

	resposta = []
	if contagemCartas[0] == 5: # Tem uma quina.
		resposta.append(0)
	elif contagemCartas[0] == 4: # Tem uma quadra.
		resposta.append(1)
	elif contagemCartas[0] == 3 and contagemCartas[1] == 2: # Tem um full house.
		resposta.append(2)
	elif contagemCartas[0] == 3 and contagemCartas[1] == 1: # Tem uma trinca. (Nem precisaria da segunda comparação).
		resposta.append(3)
	elif contagemCartas[0] == 2 and contagemCartas[1] == 2: # Tem dois pares.
		resposta.append(4)
	elif contagemCartas[0] == 2 and contagemCartas[1] == 1: # Tem um par. (Nem precisaria da segunda comparação).
		resposta.append(5)
	else: # Não tem nada.
		resposta.append(6)
	
	for carta in mao: # Adiciona o índice de "força" de cada carta, como critério de desempate.
		resposta.append(cartas.index(carta))

	return tuple(resposta)

def calcularGanhos(maos): # Função que calcula os ganhos para um conjunto de mãos.
	# Ou, mais sucintamente:
	# return sum([(indice+1) * mao[1] for indice, mao in enumerate(maos)])
	ganhoTotal = 0
	for indice, mao in enumerate(maos):
		ranque = indice + 1
		aposta = mao[1]
		ganhoTotal += ranque * aposta
	return ganhoTotal	

maos.sort(key= lambda mao:posicaoDaMao(mao[0]), reverse = True)
ganhoTotal = calcularGanhos(maos)
print('O ganho total das mãos é:', ganhoTotal)

# Parte 2:
maos.sort(key= lambda mao:posicaoDaMao(mao[0], considerarCoringas = True), reverse = True)
ganhoTotal = calcularGanhos(maos)
print('O ganho total das mãos levando em consideração os coringas é:', ganhoTotal)
