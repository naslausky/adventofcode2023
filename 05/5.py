# Desafio do dia 05/12/2023:
# a) Receber uma lista de funções lineares e seus intervalos, e um conjunto de números iniciais. Calcular o valor quando todos os números são passados por todas as funções.
# b) O conjunto de números iniciais na verdade são intervalos e portanto bem maior. Calcular o mesmo valor.

with open('input.txt') as file:
	linhas = file.read().split('\n\n')
	sementes = linhas[0].split(': ')[1].split()
	sementes = list(map(int, sementes))

mapaConversoes = {} # Mapa que associa cada nível a suas conversões da forma: {('agua', 'solo'): ((12,34,56),...)}
for informacoesConversao in linhas[1:]:
	linhasConversao = informacoesConversao.splitlines()
	origem, destino = linhasConversao[0].split()[0].split('-to-')
	caminho = (origem, destino)
	conversoesDesteCaminho = []
	for linhaNumeros in linhasConversao[1:]:
		valores = tuple(map(int, linhaNumeros.split()))
		conversoesDesteCaminho.append(valores)
	mapaConversoes[caminho] = tuple(conversoesDesteCaminho)

def percorrerConversoes(semente): # Função da parte 1 que passa uma semente por todas as etapas e retorna a posição final.
	estadoAtual = 'seed'
	localAtual = semente 
	while (estadoAtual != 'location'): # Cada iteração deve avançar uma etapa.
		destino = [caminho[1] for caminho in mapaConversoes if caminho[0] == estadoAtual][0] # Presume que só existe uma conversão disponivel para cada etapa.
		conversoes = mapaConversoes[(estadoAtual, destino)]
		for conversao in conversoes: # Para cada conversão, verificar se esta semente se encaixa nela.
			comecoDestino, comecoOrigem, comprimento = conversao
			if localAtual >= comecoOrigem and localAtual < comecoOrigem + comprimento: # Poderia ser usado in range(a, b).
				localAtual = comecoDestino + (localAtual - comecoOrigem)
				break # Cada número só deve passar por uma conversão por etapa.
		estadoAtual = destino # Avança uma etapa.
	return localAtual

locaisSementes = []
for semente in sementes:
	localAtual = percorrerConversoes(semente)
	locaisSementes.append(localAtual)
print('A menor localização possível referente às sementes iniciais é:', min(locaisSementes))

# Parte 2:
intervalosATestar = set() # Lista com os intervalos a se testar. Deve ser atualizada a cada etapa.
for indiceInformacoesSementes in range(int(len(sementes)/2)): # Reinterpreta a linha inicial para montar os intervalos de sementes.
	indice = indiceInformacoesSementes * 2
	inicioIntervalo = sementes[indice]
	comprimentoIntervalo = sementes[indice + 1]
	intervalosATestar.add((inicioIntervalo, inicioIntervalo+comprimentoIntervalo-1))

estadoAtual = 'seed'
while estadoAtual != 'location': # Para cada etapa:
	destino = [caminho[1] for caminho in mapaConversoes if caminho[0] == estadoAtual][0] # Obtem o nome da próxima etapa e suas conversões.
	conversoes = mapaConversoes[(estadoAtual, destino)]

	# 1) Um intervalo pode sobrepor em parte com uma linha conversão.
	# Neste caso, quebrar os intervalos a se testar afetados:
	for conversao in conversoes:
		comecoDestino, comecoOrigem, comprimento = conversao
		fimOrigem = comecoOrigem + comprimento - 1
		for intervalo in intervalosATestar.copy(): # Copiar para não alterar o que se está iterando.
			quebrouComeco = False # Variaveis que definem se houve uma quebra de intervalo para o começo ou fim de uma conversão.
			quebrouFim = False
			# O lado da conversão faz diferença na hora da quebra para saber em qual lado vai ficar o número central.
			if comecoOrigem > intervalo[0] and comecoOrigem <= intervalo[1]: # O começo da conversão cai dentro de um intervalo.
				quebrouComeco = True # Quebra o intervalo em 2:
				intervalosATestar.add((intervalo[0], comecoOrigem - 1)) # Do começo até o começo da conversão,
				intervalosATestar.add((comecoOrigem, intervalo[1])) # E do começo da conversão até o final.
			# Idem para o final da conversão:
			if fimOrigem >= intervalo[0] and fimOrigem < intervalo[1]: # O fim da conversão cai dentro de um intervalo.
				quebrouFim = True
				if quebrouComeco: # Neste caso, os dois lados da conversão estão contidos dentro do intervalo. Deve ser quebrado em 3.
					intervalosATestar.remove((comecoOrigem, intervalo[1])) # Remove o intervalo criado acima, e adiciona:
					intervalosATestar.add((comecoOrigem, fimOrigem)) # Do começo da quebra anterior até o fim da conversão,
					intervalosATestar.add((fimOrigem + 1, intervalo[1])) # E do fim da conversão até o fim do intervalo.
				else: # Significa que apenas o final da conversão cai dentro de um intervalo. Adicionar:
					intervalosATestar.add((intervalo[0], fimOrigem)) # Do começo do intervalo até o final da conversão,
					intervalosATestar.add((fimOrigem + 1, intervalo[1])) # E do final da conversão até o final do intervalo.

			if quebrouComeco or quebrouFim: # Se houve alguma quebra, o intervalo antigo não deve ser considerado.
				intervalosATestar.remove(intervalo)

	# 2) Com os intervalos quebrados corretamente, tenho a certeza que cada um usa apenas uma conversão.
	# Pra cada intervalo a ser testado, passar ele pela sua conversão e anotar a nova faixa de intervalos, que vai ser o começo da próxima etapa.
	novosIntervalos = set() 
	for comecoIntervalo, fimIntervalo in intervalosATestar: # Como cada intervalo só usa uma conversão, apenas as extremidades precisam ser convertidas.
		novoComeco = comecoIntervalo # Novas extremidades. Devem ficar iguais caso não estejam no escopo de nenhuma conversão.
		novoFim = fimIntervalo
		for conversao in conversoes: 
			comecoDestino, comecoOrigem, comprimento = conversao
			if comecoIntervalo >= comecoOrigem and comecoIntervalo < comecoOrigem + comprimento: # Converte o começo do intervalo.
				novoComeco = comecoDestino + (comecoIntervalo - comecoOrigem)
				break

		for conversao in conversoes: # Poderia ser feito junto com o for acima, mas precisaria de um controle para não converter o mesmo lado múltiplas vezes. 
			comecoDestino, comecoOrigem, comprimento = conversao
			if fimIntervalo >= comecoOrigem and fimIntervalo < comecoOrigem + comprimento: # Converte o fim do intervalo.
				novoFim = comecoDestino + (fimIntervalo - comecoOrigem)
				break
		novosIntervalos.add((novoComeco, novoFim))
	intervalosATestar = novosIntervalos # Sobrescreve os intervalos a testar para a próxima etapa.
	estadoAtual = destino # Atualiza a etapa.

print('Com os intervalos de sementes, a menor localização possível é:', min(intervalosATestar)[0])
