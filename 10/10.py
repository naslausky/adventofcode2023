# Desafio do dia 10/12/2023:
# a) Receber uma matriz de canos e espaços vazios. Dado um ponto inicial, descobrir o maior caminho fechado que passe por ele e calcular seu comprimento.
# b) Dado o caminho fechado da letra a), calcular sua área interna.

with open('input.txt') as file:
	linhas = file.read().splitlines()

mapa = {} # Dicionário que relaciona cada coordenada a seu conteúdo.
for indiceLinha, linha in enumerate(linhas):
	for indiceCaracter, caracter in enumerate(linha):
		coordenada = (indiceCaracter, indiceLinha)
		mapa[coordenada] = caracter
		if caracter == 'S': # Salva para uso futuro.
			pontoInicial = coordenada

laterais = ((-1, 0), (0, -1), (0, 1), (1, 0)) # Para facilitar a percorrer as quatro laterais.
saidas = { # Dicionário que relaciona cada caracter às suas conexões.
'|': ((0, 1), (0, -1)),
'-': ((-1, 0), (1, 0)),
'L': ((0, -1), (1, 0)),
'J': ((0, -1), (-1, 0)),
'7': ((-1, 0), (0, 1)),
'F': ((0, 1), (1, 0)),
'.': (),
'S': ()
}

for dx, dy in laterais: # Como não sabemos como a coordenada inicial está conectada, percorremos todas até achar o loop correto.
	caminhoPercorrido = {pontoInicial}
	x, y = (pontoInicial[0] + dx, pontoInicial[1] + dy)
	xAnterior, yAnterior = pontoInicial
	quantidadeDePassos = 1
	while (x, y) != pontoInicial: # Caso chegue ao ponto inicial, o loop foi fechado.
		caminhoPercorrido.add((x, y))
		caracter = mapa[(x, y)]
		saidasDestaCoordenada = list(saidas[caracter])
		deltaParaAnterior = (xAnterior - x ,yAnterior - y)
		if deltaParaAnterior not in saidasDestaCoordenada: # Essa coordenada não encaixa na anterior.
			break # Chegamos em um caminho quebrado. Tentar próximo ponto de partida.
		saidasDestaCoordenada.remove(deltaParaAnterior)
		deltaParaProximo = saidasDestaCoordenada[0]
		xProximo, yProximo = (x + deltaParaProximo[0], y + deltaParaProximo[1])
		xAnterior, yAnterior = x, y
		x, y = xProximo, yProximo
		quantidadeDePassos += 1
	else: # Caso o loop tenha sido concluído, sobreescrever o caracter S com o descoberto. Usado na segunda parte.
		anterior = (xAnterior - x , yAnterior - y)
		proximo = (dx, dy)
		adjacencias = [anterior, proximo]
		for letra, saida in saidas.items():
			if set(adjacencias) == set(saida):
				mapa[pontoInicial] = letra
		print('A maior distância percorrida é:', quantidadeDePassos//2)
		break

# Parte 2:
maiorX = max([x for x, _ in mapa]) + 1
maiorY = max([y for _, y in mapa]) + 1

areaTotal = 0
parCurvas = {'F':'7','L':'J'} # Mapa que relaciona cada "esquina" com a sua simétrica horizontalmente.
for indiceLinha in range(0, maiorY):
	estaDentroDaArea = False # Para cada linha vertical que passamos, alternamos se estamos dentro ou fora do circuito.
	ultimoCaracterCurvo = '' # Para saber se um 'J' ou um '7' devem alternar o nosso estado, precisamos saber a curva anterior. 
	for indiceCaracter in range(0, maiorX):
		coordenada = (indiceCaracter, indiceLinha)
		if coordenada in caminhoPercorrido:
			caracter = mapa[coordenada]
			if caracter in ('F', 'L'): # Começou uma linha horizontal. Anotamos para o término dela.
				ultimoCaracterCurvo = mapa[coordenada]
			elif caracter in ('7','J'):
				if parCurvas[ultimoCaracterCurvo] != caracter: # Significa que devemos alternar nosso estado. 
					estaDentroDaArea = not estaDentroDaArea
			elif caracter == '|':
				estaDentroDaArea = not estaDentroDaArea
		elif estaDentroDaArea:
			areaTotal+= 1
print('A área interna do circuito encontrado é:', areaTotal)

