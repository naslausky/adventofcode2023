# Desafio do dia 02/12/2023:
# a) Receba uma lista de jogos em que cada elemento é um conjunto de amostras de uma bolsa.
#    Determinar para dada quantidade de bolinhas quais são os jogos possíveis.
# b) Determinar a menor quantidade possível que permite esses jogos.

with open('input.txt') as file:
	linhas = file.read().splitlines()

limiteCubos = {'red': 12, 'green': 13, 'blue': 14} # Limites para a parte 1.

jogos = {} # Mapa que vai armazenar a entrada.
for linha in linhas:
	jogo, informacoes = linha.split(':')
	numeroJogo = int(''.join(jogo.split()[-1]))
	rodadas = informacoes.strip().split(';')
	listaDesteJogo = []
	for rodada in rodadas:
		cores = rodada.split(', ')
		mapaDestaRodada = {cor.split()[1]: int(cor.split()[0]) for cor in cores}
		listaDesteJogo.append(mapaDestaRodada)
	jogos[numeroJogo] = tuple(listaDesteJogo)

resposta = 0
respostaParte2 = 0
for numeroJogo, rodadas in jogos.items():
	esteJogoEhPossivel = True
	maiorQuantidadeVistaDeCadaCor = {} # Dicionário para a parte 2.
	for rodada in rodadas:
		for cor, quantidade in rodada.items():
			if quantidade > limiteCubos[cor]:
				esteJogoEhPossivel = False
			maiorQuantidadeVistaDeCadaCor[cor] = max(maiorQuantidadeVistaDeCadaCor
															.get(cor, 0), quantidade)
	if esteJogoEhPossivel:
		resposta += numeroJogo
	potenciaDesteJogo = 1
	for quantidade in maiorQuantidadeVistaDeCadaCor.values():
		potenciaDesteJogo *= quantidade
	respostaParte2 += potenciaDesteJogo
print('A soma dos id\'s dos jogos possíveis é:', resposta)
print('A soma das potências para permitir todos os jogos é:', respostaParte2)
