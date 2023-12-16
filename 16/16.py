# Desafio do dia 16/12/2023:
# a) Receber uma matriz de espelhos e um raio laser. Calcular quantas coordenadas serão atingidas.
# b)

mapa = {}
with open('input.txt') as file:
	linhas = file.read().splitlines()
	for indiceLinha, linha in enumerate(linhas):
		for indiceCaracter, caracter in enumerate(linha):
			coordenada = (indiceLinha, indiceCaracter)
			mapa[coordenada] = caracter

coordenadasEnergizadas = set()
sinaisAVerificar = {((0,0), '>')}
sinaisVerificados = set()
coordenadasVistas = set()
while sinaisAVerificar:
	sinal = sinaisAVerificar.pop()
#	print('Analisando sinal:', sinal, len(sinaisAVerificar))
	coordenadaAtual, direcao = sinal
	while coordenadaAtual in mapa:
		if (coordenadaAtual, direcao) in coordenadasVistas:
			break # Entrou em um loop
		coordenadasVistas.add((coordenadaAtual, direcao))
#		print('\t Passou pela coordenada:', coordenadaAtual)
		coordenadasEnergizadas.add(coordenadaAtual)
		caracter = mapa[coordenadaAtual]

		if caracter == '\\':
			if direcao == '>':
				direcao = 'v'

			elif direcao == '<':
				direcao = '^'

			elif direcao == 'v':
				direcao = '>'

			elif direcao == '^':
				direcao = '<'
#			print('\t\tPassou por espelho \\, nova direção:', direcao)

		elif caracter == '/':
			if direcao == '>':
				direcao = '^'

			elif direcao == '<':
				direcao = 'v'

			elif direcao == 'v':
				direcao = '<'

			elif direcao == '^':
				direcao = '>'
#			print('\t\tPassou por espelho /, nova direção:', direcao)

		elif caracter == '|':
#			print('\t\tChegou num espelho |')
			if direcao == '>' or direcao == '<': # Segue por um lado e adiciona mais um sinal no outro.
#				print('\t\t\tVindo da direita ou esquerda.')
				direcao = 'v'
				novoSinal = (coordenadaAtual, '^')
				if novoSinal not in sinaisVerificados:
					sinaisAVerificar.add(novoSinal)
#				print('\t\t\tSinais A verificar:', sinaisAVerificar)

		elif caracter == '-':
#			print('\t\tChegou num espelho -')
			if direcao == 'v' or direcao == '^': 
#				print('\t\t\tVindo de cima ou baixo.')
				direcao = '<'
				novoSinal = (coordenadaAtual, '>')
				if novoSinal not in sinaisVerificados:
					sinaisAVerificar.add(novoSinal)
#				print('\t\t\tSinais A verificar:', sinaisAVerificar)

		if direcao == '>':
			coordenadaAtual = (coordenadaAtual[0], coordenadaAtual[1] + 1)
		elif direcao == '<':
			coordenadaAtual = (coordenadaAtual[0], coordenadaAtual[1] - 1)
		elif direcao == '^':
			coordenadaAtual = (coordenadaAtual[0] - 1, coordenadaAtual[1])
		elif direcao == 'v':
			coordenadaAtual = (coordenadaAtual[0] + 1, coordenadaAtual[1])
	sinaisVerificados.add(sinal)
#	print('Acabou de analisar', sinal)
#	input()

print(len(coordenadasEnergizadas))
	
