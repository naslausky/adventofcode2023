with open('input.txt') as file:
	instrucoes = file.read().splitlines()
	
deltaDirecoes = {'R':(0, 1), 'L':(0, -1), 'U': (-1, 0), 'D': (1, 0)}

coordenadaAtual = (0,0)
mapa = {coordenadaAtual}
for instrucao in instrucoes:
	direcao, quantidade, cor = instrucao.split()
	quantidade = int(quantidade)
	#Parte 2:
	#quantidade = int(cor[2:-2], 16)
	#codigosDirecoes = {'0' : 'R', '1' : 'D', '2' : 'L', '3' : 'U'}
	#direcao = codigosDirecoes[cor[-2]]
	for _ in range(quantidade):
		delta = deltaDirecoes[direcao]
		coordenadaAtual = (coordenadaAtual[0] + delta[0], coordenadaAtual[1] + delta[1])
		mapa.add(coordenadaAtual)

# Achar uma coordenada que esteja dentro:
coordenadaInterna = (None, None)
menorLinha = min(mapa, key=lambda x:x[0])[0]
maiorLinha = max(mapa, key=lambda x:x[0])[0]
menorColuna = min(mapa, key=lambda x:x[1])[1]
maiorColuna = max(mapa, key=lambda x:x[1])[1]
for indiceLinha in range(menorLinha, maiorLinha + 1):
	for indiceColuna in range(menorColuna, maiorColuna + 1):
		coordenada = (indiceLinha, indiceColuna)
		coordenadaNorte = (indiceLinha - 1, indiceColuna)
		coordenadaSul = (indiceLinha + 1, indiceColuna)
		if coordenada in mapa and coordenadaNorte in mapa and coordenadaSul in mapa:
			coordenadaInterna = (indiceLinha, indiceColuna + 1)
			break
	else:
		continue
	break

def imprimirMapa():
	for indiceLinha in range(menorLinha, maiorLinha + 1):
		linha = ''.join('#' if (indiceLinha, indiceColuna) in mapa else ' ' 
						for indiceColuna in range(menorColuna, maiorColuna + 1))

def percorrerInterior(coordenadaInterna):
	coordenadasAlcancaveis = {coordenadaInterna}
	coordenadasVistas = set()
	while coordenadasAlcancaveis:
		coordenadaAtual = coordenadasAlcancaveis.pop()
		for delta in deltaDirecoes.values():
			proximaCoordenada =  (coordenadaAtual[0] + delta[0], coordenadaAtual[1] + delta[1])
			if proximaCoordenada not in mapa and proximaCoordenada not in coordenadasVistas:
				coordenadasAlcancaveis.add(proximaCoordenada)
		coordenadasVistas.add(coordenadaAtual)
	for novaCoordenada in coordenadasVistas:
		mapa.add(novaCoordenada)
percorrerInterior(coordenadaInterna)
print(len(mapa))
