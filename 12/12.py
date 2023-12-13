with open('input.txt') as file:
	linhas = file.read().splitlines()

gabarito = {}
def quantidadeDePossibilidades(configuracao, quantidades):
	chave = (configuracao, quantidades)
	if chave in gabarito:
		return gabarito[chave]
	ultimoElemento = len(quantidades) == 1
	tamanhoMinimo = sum(quantidades) + len(quantidades) - 1
	maiorIndiceAPercorrer = len(configuracao) - tamanhoMinimo + 1
	
	indicePrimeiroDanificado = configuracao.find('#')
	if indicePrimeiroDanificado != -1:
		maiorIndiceAPercorrer = min(maiorIndiceAPercorrer, indicePrimeiroDanificado + 1)
#		print(configuracao, quantidades, indicePrimeiroDanificado, len(configuracao)-tamanhoMinimo )
#		input()
	if len(configuracao) < tamanhoMinimo:
		#print('Tamanho insuficiente')
		return 0
	blocoDaVez = quantidades[0]
	resposta = 0
	for indice in range(maiorIndiceAPercorrer):
		#print('\t Começando pelo indice:', indice, 'da string', configuracao)
		candidato = configuracao[indice : indice + blocoDaVez]
		if '.' in candidato:
			#print('\t Indice não encaixa:', candidato)
			continue
		if ultimoElemento: # É uma possibilidade e só falta ele. Adicionar uma possibilidade à resposta.
#			print('\t é o último elemento')
#			print(configuracao)
#			print(candidato)
			if indice+blocoDaVez < len(configuracao) and '#' in configuracao[indice+blocoDaVez:]:
				continue
			resposta += 1
		else: 
			if configuracao[indice + blocoDaVez] == '#': # Se não é o último, tem que ter o separador. Pode ser ? ou .
				#print('\t Não tem o . após pra ter espaco.')
				continue
			if indice-1 > 0 and configuracao[indice - 1] == '#':
				#significa que não tem o espaço anterior.
				#print('\t não tem o . antes pra ter espaço.')
				continue
			#print('\t Chamando com', configuracao[indice+blocoDaVez+1:], quantidades[1:])
			resposta += quantidadeDePossibilidades(configuracao[indice+blocoDaVez+1:], quantidades[1:])
			#print('\t Voltou da chamada')
	gabarito[chave] = resposta
	return resposta

#print(quantidadeDePossibilidades('?###????????', (3,2,1)))

#exit()
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
	#print(linha, resposta)
	#input()
print(resposta)
print(respostaParte2)
