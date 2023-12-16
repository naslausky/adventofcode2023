# Desafio do dia 16/12/2023:
# a) Receber uma matriz de espelhos e um raio laser. Calcular quantas coordenadas serão atingidas.
# b) Calcular o maior número de coordenadas atingidas para qualquer laser entrando pela borda.

mapa = {}
with open('input.txt') as file:
	linhas = file.read().splitlines()
	for indiceLinha, linha in enumerate(linhas):
		for indiceCaracter, caracter in enumerate(linha):
			coordenada = (indiceLinha, indiceCaracter)
			mapa[coordenada] = caracter

def percorrerMapa(inicio): # Função que percorre um mapa a partir de um início e calcula quantas coordenadas serão energizadas.
	sinaisAVerificar = {inicio} # Conjunto de sinais que faltam verificar. Aumenta conforme bifurca (| ou -).

	# Provavelmente os três conjuntos abaixos poderiam ser unidos em um só. Porém preferi separar para cada caso:
	coordenadasEnergizadas = set() # Conjunto de coordenadas que contém um laser. Usado para obter a resposta.
	sinaisVerificados = set() # Conjunto dos sinais que já foram verificados. Usado para quando bifurcar, não adicionar um sinal já visto.
	coordenadasVistas = set() # Conjunto dos pares (coordenada, direcao) já vistos. Usado para detectar loops em que não sejam gerados novos sinais.

	while sinaisAVerificar: # Começa a verificar o próximo sinal.
		sinal = sinaisAVerificar.pop()
		coordenadaAtual, direcao = sinal

		while coordenadaAtual in mapa:
			if (coordenadaAtual, direcao) in coordenadasVistas: # Entrou em um loop.
				break
			coordenadasVistas.add((coordenadaAtual, direcao))

			coordenadasEnergizadas.add(coordenadaAtual) # Armazena a coordenada atual para a resposta.
			caracter = mapa[coordenadaAtual] # Obtém o caracter do mapa para decidir próxima direção.
			if caracter == '\\':
				if direcao == '>': # Poderia ser substituido por um dicionário de constantes.
					direcao = 'v'
				elif direcao == '<':
					direcao = '^'
				elif direcao == 'v':
					direcao = '>'
				elif direcao == '^':
					direcao = '<'

			elif caracter == '/':
				if direcao == '>':
					direcao = '^'
				elif direcao == '<':
					direcao = 'v'
				elif direcao == 'v':
					direcao = '<'
				elif direcao == '^':
					direcao = '>'

			elif caracter == '|':
				if direcao == '>' or direcao == '<': # Seguir por um lado e adicionar mais um sinal a verificar pelo outro.
					direcao = 'v' # Arbitrei o sinal a seguir.
					novoSinal = (coordenadaAtual, '^') # A outra direção fica como um novo sinal a verificar.
					if novoSinal not in sinaisVerificados: # Apenas os que já não tenham sido verificados antes.
						sinaisAVerificar.add(novoSinal)

			elif caracter == '-':
				if direcao == 'v' or direcao == '^': 
					direcao = '<'
					novoSinal = (coordenadaAtual, '>')
					if novoSinal not in sinaisVerificados:
						sinaisAVerificar.add(novoSinal)

			if direcao == '>': # Move a coordenada atual baseado na direção.
				coordenadaAtual = (coordenadaAtual[0], coordenadaAtual[1] + 1)
			elif direcao == '<':
				coordenadaAtual = (coordenadaAtual[0], coordenadaAtual[1] - 1)
			elif direcao == '^':
				coordenadaAtual = (coordenadaAtual[0] - 1, coordenadaAtual[1])
			elif direcao == 'v':
				coordenadaAtual = (coordenadaAtual[0] + 1, coordenadaAtual[1])

		sinaisVerificados.add(sinal) # Salva para não precisar reolhar este sinal no futuro.
	return len(coordenadasEnergizadas)
print('Começando do canto superior esquerdo, o número de coordenadas energizadas é:', percorrerMapa(((0,0), '>')))

# Parte 2:
numeroDeLinhas = len(linhas)
numeroDeColunas = len(linhas[0])
maiorEnergizacao = 0
candidatosInicios = [] # Possíveis começos.
for indiceLinha in range(numeroDeLinhas): # Para cada linha, o início pode ser da esquerda indo pra direita, e da direita indo pra esquerda:
	candidatosInicios.extend((((indiceLinha, 0), '>'), ((indiceLinha, numeroDeColunas - 1), '<')))
	
for indiceColuna in range(numeroDeColunas): # Para cada coluna, o início pode ser de cima indo pra baixo, e de baixo indo pra cima:
	candidatosInicios.extend((((0, indiceColuna), 'v'), ((numeroDeLinhas - 1, indiceColuna), '^')))

for candidato in candidatosInicios:
	maiorEnergizacao = max(maiorEnergizacao, percorrerMapa(candidato))
print('O maior número de coordenadas energizadas a partir de qualquer borda é:', maiorEnergizacao)
