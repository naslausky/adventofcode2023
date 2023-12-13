# Desafio do dia 13/12/2023:
# a) Receber uma lista de matrizes retangulares de caracteres. Descobrir em qual linha ou coluna cada matriz pode ser considerada como linha de simetria.
# b) Idem porém aceitando um erro na simetria.

with open('input.txt') as file:
	mapas = file.read().split('\n\n')

somaIndicesLinhas = 0
somaIndicesColunas = 0
somaIndicesColunasParte2 = 0
somaIndicesLinhasParte2 = 0
for mapa in mapas:
	linhasDesteMapa = mapa.splitlines()
	for indiceLinha in range(1, len(linhasDesteMapa)):
		quantidadeDeErrosDestaLinha = 0 # Quantidade de erros tomando esta linha como espelho.
		for linha1, linha2 in zip(linhasDesteMapa[indiceLinha:],
						reversed(linhasDesteMapa[:indiceLinha])):
			for caracter1, caracter2 in zip(linha1, linha2):
				if caracter1 != caracter2:
					quantidadeDeErrosDestaLinha += 1
		if quantidadeDeErrosDestaLinha == 0:
			somaIndicesLinhas += indiceLinha
		if quantidadeDeErrosDestaLinha == 1:
			somaIndicesLinhasParte2 += indiceLinha

	# Idem para as colunas:
	colunasDesteMapa = [''.join([linha[indiceColuna] for linha in linhasDesteMapa]) 
					for indiceColuna in range(len(linhasDesteMapa[0]))]
	for indiceColuna in range(1, len(colunasDesteMapa)):
		quantidadeDeErrosDestaColuna = 0 # Quantidade de erros tomando esta coluna como espelho.
		for coluna1, coluna2 in zip(colunasDesteMapa[indiceColuna:],
						reversed(colunasDesteMapa[:indiceColuna])):
			for caracter1, caracter2 in zip(coluna1, coluna2):
				if caracter1 != caracter2:
					quantidadeDeErrosDestaColuna += 1
		if quantidadeDeErrosDestaColuna == 0:
			somaIndicesColunas += indiceColuna
		if quantidadeDeErrosDestaColuna == 1:
			somaIndicesColunasParte2 += indiceColuna

resposta = somaIndicesLinhas* 100 + somaIndicesColunas
respostaParte2 = somaIndicesLinhasParte2 * 100 + somaIndicesColunasParte2
print('O resumo das anotações sobre os espelhos é de:', resposta)
print('O resumo das anotações considerando uma mancha é de:', respostaParte2)
