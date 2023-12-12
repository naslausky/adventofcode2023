with open('input.txt') as file:
	linhas = file.read().splitlines()

gabarito = {}
def quantidadeDePossibilidades(configuracao, quantidades):
	chave = (configuracao, quantidades)
#	if chave in gabarito:
#		return gabarito[chave]

	if '?' in configuracao:
		opcao1 = configuracao.replace('?', '.', 1)
		opcao2 = configuracao.replace('?', '#', 1)
		resposta = quantidadeDePossibilidades(opcao1, quantidades) + quantidadeDePossibilidades(opcao2, quantidades)

	else: # Verifica se essa configuração é valida:
		conjuntosDanificados = configuracao.split('.')
		conjuntosDanificados = [conjunto for conjunto in conjuntosDanificados if conjunto]
		conjuntosDanificados = [len(conjunto) for conjunto in conjuntosDanificados]
		resposta = 0
		if tuple(conjuntosDanificados) == quantidades:
			resposta = 1
#	gabarito[chave] = resposta
	return resposta

#print(quantidadeDePossibilidades('?###????????', (3,2,1)))
resposta = 0
for linha in linhas:
	configuracao, quantidades = linha.split()
	quantidades = quantidades.split(',')
	quantidades = tuple(map(int, quantidades))
#	resposta += quantidadeDePossibilidades(configuracao, quantidades)
	configuracao = [configuracao for _ in range(5)]
	configuracao = '?'.join(configuracao)
	quantidades = 5 * quantidades
	resposta += quantidadeDePossibilidades(configuracao, quantidades)
	print('terminado uma linha')
print(resposta)
