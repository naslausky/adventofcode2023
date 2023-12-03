# Desafio do dia 03/12/2023:
# a) Receber uma matriz de caracteres. Somar todos os números que é adjancente a um caracter especial.
# b) Multiplicar os números que estão adjacentes a um mesmo asterisco e somá-los.

with open('input.txt') as file:
	linhas = file.read().splitlines()

resposta = 0
engrenagens = {} # Dicionário que associa uma engrenagem a um conjunto de números em contato.
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
							if caracterAVerificar == '*': # Salva para a segunda parte.
								chave = (idy, idx)
								coordenadasDestaEngrenagem = engrenagens.get(chave, set())
								coordenadasDestaEngrenagem.add(int(numero))
								engrenagens[chave] = coordenadasDestaEngrenagem
				if contemCaracterAoRedor:
					resposta += int(numero)
			numero = ''
# Parte 2:
respostaParte2 = 0
for conjuntoNumeros in engrenagens.values(): # Realiza a multiplicação das engrenagens em contato com dois números.
	if len(conjuntoNumeros) == 2:
		multiplicacao = 1
		for numero in conjuntoNumeros:
			multiplicacao *= numero
		respostaParte2 += multiplicacao
print('A soma do número das partes é:', resposta)
print('A soma das razões das engrenagens é:', respostaParte2)
