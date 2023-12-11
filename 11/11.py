# Desafio do dia 11/12/2023:
# a) Receber um mapa de estrelas. Calcular a distância entre cada par de estrelas, considerando que linhas e colunas que não contenham nenhuma estrela valem como 2.
# b) Idem, porém linhas e colunas vazias valem como 1000000.

with open('input.txt') as file:
	linhas = file.read().splitlines()

coordenadasEstrelas = []
for indiceLinha, linha in enumerate(linhas):
	for indiceCaracter, caracter in enumerate(linha):
		if caracter == '#':
			coordenadasEstrelas.append((indiceLinha, indiceCaracter))

colunasEstrelas = list({y for _, y in coordenadasEstrelas}) # Lista que contém as colunas que contém estrelas, ordenada e sem duplicatas.
colunasEstrelas.sort()
indicesColunasEstrelas = {coluna: indice for indice, coluna in enumerate(colunasEstrelas)}

linhasEstrelas = list({x for x, _ in coordenadasEstrelas}) # Idem para as linhas.
linhasEstrelas.sort()
indicesLinhasEstrelas = {linha: indice for indice, linha in enumerate(linhasEstrelas)}

resposta = 0
respostaParte2 = 0
for indiceEstrela1, coordenadaEstrela1 in enumerate(coordenadasEstrelas):
	for coordenadaEstrela2 in coordenadasEstrelas[indiceEstrela1 + 1:]: # Calcula apenas para as estrelas seguintes.
		x1, y1 = coordenadaEstrela1
		x2, y2 = coordenadaEstrela2
		x1, x2 = sorted((x1, x2)) # Ordena as duas linhas e colunas utilizadas.
		y1, y2 = sorted((y1, y2))
		distanciaBase = (x2 - x1) + (y2 - y1)
		
		quantidadeLinhasDuplicadas = 0
		indiceX1 = indicesLinhasEstrelas[x1] # Índices para percorrer as listas de linhas/colunas.
		indiceX2 = indicesLinhasEstrelas[x2] # Para cada elemento, a distância para o elemento anterior é a quantidade de linhas/colunas vazias.
		for linha1, linha2 in zip(linhasEstrelas[indiceX1: indiceX2], linhasEstrelas[indiceX1 + 1: indiceX2 + 1]):
			quantidadeLinhasDuplicadas += linha2 - linha1 - 1

		quantidadeColunasDuplicadas = 0
		indiceY1 = indicesColunasEstrelas[y1]
		indiceY2 = indicesColunasEstrelas[y2]
		for coluna1, coluna2 in zip(colunasEstrelas[indiceY1: indiceY2], colunasEstrelas[indiceY1 + 1: indiceY2 + 1]):
			quantidadeColunasDuplicadas += coluna2 - coluna1 - 1

		quantidadeDuplicadas = quantidadeLinhasDuplicadas + quantidadeColunasDuplicadas
		distanciaFinal = distanciaBase + quantidadeDuplicadas
		distanciaFinalParte2 = distanciaBase + (1000000 - 1) * quantidadeDuplicadas
		resposta += distanciaFinal
		respostaParte2 += distanciaFinalParte2

print('A soma da quantidade mínima de passos entre cada par de estrelas é:', resposta)
print('A soma da quantidade mínima de passos entre cada par de estrelas com o universo mais expandido é:', respostaParte2)
