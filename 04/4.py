# Desafio do dia 04/12/2023:
# a) Receber uma lista de jogos com os números ganhadores e apostados. Verificar quantos pontos foi feito em cada.
# b) Idem, porém cada ponto rende uma raspadinha seguinte adicional. Calcular a quantidade de raspadinhas obtida.

with open('input.txt') as file:
	linhas = file.read().splitlines()

resposta = 0
quantidadeDeRaspadinhas = {} # Dicionário que relaciona um jogo a quantidade de cópias de dele.
for linha in linhas:
	jogo, numeros = linha.split(': ')
	jogo = int(jogo.split()[1])
	numerosSorteados, numerosApostados = numeros.split(' | ')
	numerosSorteados = numerosSorteados.split()
	numerosApostados = numerosApostados.split()
	numerosSorteados = set(map(int,numerosSorteados))
	numerosApostados = set(map(int,numerosApostados))
	acertos = len(numerosSorteados.intersection(numerosApostados))
	pontuacao = 2 ** (acertos - 1) if acertos else 0
	resposta += pontuacao

	# Parte 2:
	quantidadeDeRaspadinhas[jogo] = quantidadeDeRaspadinhas.get(jogo, 0) + 1 # Adiciona a raspadinha lida à contagem.
	for indice in range(1, acertos + 1): # Incrementa a quantidade dos próximos jogos
		quantidadeDeRaspadinhas[jogo + indice] = (quantidadeDeRaspadinhas.get(jogo + indice, 0) + 
												quantidadeDeRaspadinhas[jogo]) # com a quantidade que temos da raspadinha atual.
	
quantidadeDeRaspadinhas = {chave: valor for chave, valor in quantidadeDeRaspadinhas.items() if chave <= jogo} # Elimina as raspadinhas com número maior do que o último jogo.
respostaParte2 = sum([valor for valor in quantidadeDeRaspadinhas.values()]) # Conta o resultado.
print('A pontuação total das raspadinhas é:', resposta)
print('A quantidade total de raspadinhas obtidas é:', respostaParte2)
