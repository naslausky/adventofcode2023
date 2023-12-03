# Desafio do dia 03/12/2023:
# a) Receber uma matriz de caracteres. Somar todos os números que é adjancente a um caracter especial.
# b) Multiplicar os números que estão adjacentes a um mesmo asterisco e somá-los.

with open('input.txt') as file:
	linhas = file.read().splitlines()

resposta = 0
coordenadasNumeros = {} # Mapa utilizado para a segunda parte.
for indiceLinha, linha in enumerate(linhas):
	numero = ''
	menorIndiceComNumero = 0
	for indiceCaracter, caracter in enumerate(linha + '.'): # O ponto é para caso a linha termine com um número.
		if caracter.isdigit():
			if not numero:
				menorIndiceComNumero = indiceCaracter
			numero += caracter
		else:
			if numero:
				coordenadasNumeros[(indiceLinha, menorIndiceComNumero)] = int(numero)
				contemCaracterAoRedor = False 
				# Verificar as coordenadas adjacentes:
				for idx in range(menorIndiceComNumero - 1, indiceCaracter + 1):
					if idx < 0 or idx >= len(linha):
						continue
					for idy in range(indiceLinha - 1, indiceLinha + 2):
						if idy < 0 or idy >= len(linhas):
							continue
						caracterAVerificar = linhas[idy][idx]
						if (not caracterAVerificar.isdigit()) and caracterAVerificar != '.':
							contemCaracterAoRedor = True
				if contemCaracterAoRedor:
					resposta += int(numero)
			numero = ''
# Parte 2:
respostaParte2 = 0
for indiceLinha, linha in enumerate(linhas):
	for indiceCaracter, caracter in enumerate(linha):
		if caracter == '*':
			multiplicacao = 1
			quantidadeDeNumerosConectados = 0
			for coordenadasDoNumero, numero in coordenadasNumeros.items():
				rangeLinhasDesteNumero = (coordenadasDoNumero[0] - 1, coordenadasDoNumero[0] + 2)
				rangeCaracteresDesteNumero = (coordenadasDoNumero[1] - 1, 
								coordenadasDoNumero[1] + len(str(numero)) + 1)
				if (indiceLinha in range(*rangeLinhasDesteNumero) and
					indiceCaracter in range(*rangeCaracteresDesteNumero)):
					multiplicacao *= numero
					quantidadeDeNumerosConectados += 1
			if quantidadeDeNumerosConectados == 2:
				respostaParte2+= multiplicacao
print('A soma do número das partes é:', resposta)
print('A soma das razões das engrenagens é:', respostaParte2)
