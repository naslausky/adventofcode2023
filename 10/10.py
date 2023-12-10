# Desafio do dia 10
with open('input.txt') as file:
	linhas = file.read().splitlines()

mapa = {}
for indiceLinha, linha in enumerate(linhas):
	for indiceCaracter, caracter in enumerate(linha):
		coordenada = (indiceCaracter, indiceLinha)
		mapa[coordenada] = caracter
		if caracter == 'S':
			pontoInicial = coordenada

laterais = ((-1, 0), (0, -1), (0, 1), (1, 0))
saidas = {
'|': ((0, 1), (0, -1)),
'-': ((-1, 0), (1, 0)),
'L': ((0, -1), (1, 0)),
'J': ((0, -1), (-1, 0)),
'7': ((-1, 0), (0, 1)),
'F': ((0, 1), (1, 0)),
'.': (),
'S': ()
}

for dx, dy in laterais:
	#print('Começando pela lateral:', dx,dy)
	# Supondo que saíamos por esse lado do ponto inicial:
	x, y = (pontoInicial[0] + dx, pontoInicial[1] + dy)
	xAnterior, yAnterior = pontoInicial
	quantidadeDePassos = 1
	while (x, y) != pontoInicial:
		caracter = mapa[(x,y)]
		saidasDestaCoordenada = list(saidas[caracter])
		deltaParaAnterior = (xAnterior - x ,yAnterior - y)
		#print('Testando coordenada', (x,y), caracter)
		if deltaParaAnterior not in saidasDestaCoordenada: # Essa coordenada não encaixa na anterior.
			break
		saidasDestaCoordenada.remove(deltaParaAnterior)

		deltaParaProximo = saidasDestaCoordenada[0]
		xProximo, yProximo = (x + deltaParaProximo[0], y + deltaParaProximo[1])
		xAnterior, yAnterior = x, y
		x, y = xProximo, yProximo
		quantidadeDePassos += 1
	else:
		print('A maior distância percorrida é:', quantidadeDePassos//2)
		break




