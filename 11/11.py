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

colunasEstrelas = [y for _, y in coordenadasEstrelas]
colunasEstrelas.sort()
linhasEstrelas = [x for x, _ in coordenadasEstrelas]
linhasEstrelas.sort()

resposta = 0
respostaParte2 = 0
for indiceEstrela1, coordenadaEstrela1 in enumerate(coordenadasEstrelas):
	for coordenadaEstrela2 in coordenadasEstrelas[indiceEstrela1 + 1:]:
		x1, y1 = coordenadaEstrela1
		x2, y2 = coordenadaEstrela2
		x1, x2 = sorted((x1, x2))
		y1, y2 = sorted((y1, y2))
		distanciaBase = x2 - x1 + y2 - y1
		
		quantidadeLinhasDuplicadas = len([1 for x in range(x1, x2) if x not in linhasEstrelas])
		quantidadeColunasDuplicadas = len([1 for y in range(y1, y2) if y not in colunasEstrelas])
		quantidadeDuplicadas = quantidadeLinhasDuplicadas + quantidadeColunasDuplicadas

		distanciaFinal = distanciaBase + quantidadeDuplicadas
		distanciaFinalParte2 = distanciaBase + (1000000 - 1) * quantidadeDuplicadas
		resposta += distanciaFinal
		respostaParte2 += distanciaFinalParte2

print(resposta)
print(respostaParte2)
