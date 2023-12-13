# Desafio do dia 12/12/2023:
# a) Receber uma linha de um nonograma, e as quantidades de blocos. Calcular quantas possibilidades de preenchimento existem.
# b) Idem porém para cada informação multiplicada por 5.

with open('input.txt') as file:
	linhas = file.read().splitlines()

gabarito = {} # Caso a função já tenha sido chamada com as mesmas entradas, não precisar calcular novamente.
def quantidadeDePossibilidades(configuracao, quantidades): 
	# Função que recebe como entrada uma string, e a tupla com os blocos a serem analisados,
	# e retorna a quantidade de organizações possíveis.

	chave = (configuracao, quantidades)
	if chave in gabarito: # Verifica se já foi calculado anteriormente.
		return gabarito[chave]

	ultimoElemento = len(quantidades) == 1 # Booleano que informa se estamos no elemento final.
	tamanhoMinimo = sum(quantidades) + len(quantidades) - 1 # O mínimo de caracteres necessários para acomodar todos os blocos.
	if len(configuracao) < tamanhoMinimo:
		return 0

	maiorIndiceAPercorrer = len(configuracao) - tamanhoMinimo + 1 # Ao percorrer as possibilidades para o início do primeiro bloco, só podemos ir até onde ainda sobra espaço suficiente para os próximos.
	
	indicePrimeiroDanificado = configuracao.find('#')
	if indicePrimeiroDanificado != -1: # Se o primeiro bloco começar após um '#', ele não seria o primeiro bloco e portanto este também é um limite superior de busca.
		maiorIndiceAPercorrer = min(maiorIndiceAPercorrer, indicePrimeiroDanificado + 1)

	blocoDaVez = quantidades[0]
	resposta = 0
	for indice in range(maiorIndiceAPercorrer): # Indice para início do primeiro bloco.
		candidato = configuracao[indice : indice + blocoDaVez] # Janela para verificação do bloco em questão.
		if '.' in candidato: # A janela experimentada não serve.
			continue

		if ultimoElemento: # Caso ele seja o último, este índice é uma possibilidade apenas se não existir outro '#' no resto da string (pois neste caso ele não seria verdadeiramente o último).
			if not (indice+blocoDaVez < len(configuracao) and '#' in configuracao[indice+blocoDaVez:]):
				resposta += 1
		else: # Caso esse não seja o último bloco, é necessario ter o separador.
			if configuracao[indice + blocoDaVez] == '#': # O separador pode ser '?' ou '.'.
				continue
			# Para cada candidato não sendo o último elemento, chama a função recursiva com
			# um bloco a menos e o resto da string que sobrou após retirar o candidato e o separador.
			resposta += quantidadeDePossibilidades(configuracao[indice+blocoDaVez+1:], quantidades[1:])
	gabarito[chave] = resposta # Salva para não precisar calcular no futuro.
	return resposta

resposta = 0
respostaParte2 = 0
for linha in linhas:
	configuracao, quantidades = linha.split()
	quantidades = quantidades.split(',')
	quantidades = tuple(map(int, quantidades))
	resposta += quantidadeDePossibilidades(configuracao, quantidades)
	configuracao = [configuracao for _ in range(5)]
	configuracao = '?'.join(configuracao)
	quantidades = 5 * quantidades
	respostaParte2 += quantidadeDePossibilidades(configuracao, quantidades)
print('A soma da quantidade de arranjos diferentes é:', resposta)
print('A soma da quantidade de arranjos diferentes com 5x cada linha é:', respostaParte2)
