# Desafio do dia 07/12/2023:
# a) Receber uma lista de mãos de poker, com sua respectiva aposta. Ordenar todas e calcular a pontuação total.
# b) Idem porém agora interpretando J como coringa.

maos = []
with open('input.txt') as file:
	linhas = file.read().splitlines()
for linha in linhas:
	mao, aposta = linha.split()
	aposta = int(aposta)
	maos.append((mao, aposta))

cartas = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']
def posicaoDaMao(mao): # Função que recebe uma mão e converte para um objeto comparável.
	contagemCartas = {carta: mao.count(carta) for carta in mao}
	contagemCartas = tuple(sorted(contagemCartas.values(), reverse = True))

	resposta = []
	if contagemCartas[0] == 5: # Tem uma quina.
		resposta.append(0)
	elif contagemCartas[0] == 4: # Tem uma quadra.
		resposta.append(1)
	elif contagemCartas[0] == 3 and contagemCartas[1] == 2: # Tem um full house.
		resposta.append(2)
	elif contagemCartas[0] == 3 and contagemCartas[1] == 1: # Tem uma trinca. (Nem precisaria da segunda comparação)
		resposta.append(3)
	elif contagemCartas[0] == 2 and contagemCartas[1] == 2: # Tem dois pares.
		resposta.append(4)
	elif contagemCartas[0] == 2 and contagemCartas[1] == 1: # Tem um par. (Nem precisaria da segunda comparação)
		resposta.append(5)
	else: # Não tem nada.
		resposta.append(6)
	
	for carta in mao:
		resposta.append(cartas.index(carta))

	return tuple(resposta)

maos.sort(key= lambda mao:posicaoDaMao(mao[0]), reverse = True)
ganhoTotal = 0
for indice, mao in enumerate(maos):
	ranque = indice + 1
	aposta = mao[1]
	ganhoTotal += ranque * aposta
print('O ganho total das mãos é:', ganhoTotal)

# Parte 2:
coringa = 'J'
cartas = ['A', 'K', 'Q', 'T', '9', '8', '7', '6', '5', '4', '3', '2', coringa]
def posicaoDaMaoComCoringas(mao): # Função que recebe uma mão e converte para um objeto comparável.
	contagemCartas = {carta: mao.count(carta) for carta in mao if carta != coringa}
	quantidadeDeCoringas = mao.count(coringa)
	contagemCartas = list(sorted(contagemCartas.values(), reverse = True))
	if not contagemCartas:
		contagemCartas = [0]
	contagemCartas[0] += quantidadeDeCoringas # Os coringas devem adicionar à maior quantidade que você já tem.
	contagemCartas = tuple(contagemCartas)
	resposta = []
	if contagemCartas[0] == 5: # Tem uma quina.
		resposta.append(0)
	elif contagemCartas[0] == 4: # Tem uma quadra.
		resposta.append(1)
	elif contagemCartas[0] == 3 and contagemCartas[1] == 2: # Tem um full house.
		resposta.append(2)
	elif contagemCartas[0] == 3 and contagemCartas[1] == 1: # Tem uma trinca. (Nem precisaria da segunda comparação)
		resposta.append(3)
	elif contagemCartas[0] == 2 and contagemCartas[1] == 2: # Tem dois pares.
		resposta.append(4)
	elif contagemCartas[0] == 2 and contagemCartas[1] == 1: # Tem um par. (Nem precisaria da segunda comparação)
		resposta.append(5)
	else: # Não tem nada.
		resposta.append(6)
	
	for carta in mao:
		resposta.append(cartas.index(carta))

	return tuple(resposta)

maos.sort(key= lambda mao:posicaoDaMaoComCoringas(mao[0]), reverse = True)
ganhoTotal = 0
for indice, mao in enumerate(maos):
	ranque = indice + 1
	aposta = mao[1]
	ganhoTotal += ranque * aposta
print('O ganho total das mãos levando em consideração os coringas é:', ganhoTotal)
