# Desafio do dia 05/12/2023:
# a) Receber uma lista de funções lineares e seus intervalos, e um conjunto de números iniciais. Calcular o valor quando todos os números são passados por todas as funções.
# b)

with open('input.txt') as file:
	linhas = file.read().split('\n\n')
	sementes = linhas[0].split(': ')[1].split()
	sementes = list(map(int, sementes))
mapaConversoes = {}
for informacoesConversao in linhas[1:]:
	linhasConversao = informacoesConversao.splitlines()
	origem, destino = linhasConversao[0].split()[0].split('-to-')
	caminho = (origem, destino)
	conversoesDesteCaminho = []
	for linhaNumeros in linhasConversao[1:]:
		valores = tuple(map(int, linhaNumeros.split()))
		conversoesDesteCaminho.append(valores)
	mapaConversoes[caminho] = tuple(conversoesDesteCaminho)

def percorrerConversoes(semente):
	estadoAtual = 'seed'
	localAtual = semente 
	while (estadoAtual != 'location'):
		destino = [caminho[1] for caminho in mapaConversoes if caminho[0] == estadoAtual][0]
		conversoes = mapaConversoes[(estadoAtual, destino)]
		for conversao in conversoes:
			comecoDestino, comecoOrigem, comprimento = conversao
			#if localAtual in range(comecoOrigem, comecoOrigem + comprimento):
			if localAtual >= comecoOrigem and localAtual <comecoOrigem + comprimento:
				localAtual = comecoDestino + (localAtual - comecoOrigem)
				break
		estadoAtual = destino
	return localAtual

locaisSementes = []
for semente in sementes:
	localAtual = percorrerConversoes(semente)
	locaisSementes.append(localAtual)
print(min(locaisSementes))

# Parte 2:
intervalosATestar = []

for indiceInformacoesSementes in range(int(len(sementes)/2)):
	indice = indiceInformacoesSementes * 2
	inicioIntervalo = sementes[indice]
	comprimentoIntervalo = sementes[indice + 1]
	intervalosATestar.append((inicioIntervalo, inicioIntervalo+comprimentoIntervalo))
	
estadoAtual = 'seed'
while estadoAtual != 'location':
	#Preciso quebrar os intervalos a testar:
	destino = [caminho[1] for caminho in mapaConversoes if caminho[0] == estadoAtual][0]
	conversoes = mapaConversoes[(estadoAtual, destino)]
	for conversao in conversoes: # Para cada conversão, quebrar os intervalos a testar que são afetados por ela:
		comecoDestino, comecoOrigem, comprimento = conversao
		fimOrigem = comecoOrigem + comprimento
#		print('Fazendo conversao:', comecoOrigem, fimOrigem)
		for intervalo in intervalosATestar.copy():
			quebrouComeco = False
			quebrouFim = False
			if comecoOrigem >= intervalo[0] and comecoOrigem <= intervalo[1]:
#				print('Quebrou Comeco!')
				quebrouComeco = True
				intervalosATestar.append((intervalo[0], comecoOrigem - 1))
				intervalosATestar.append((comecoOrigem, intervalo[1]))
			if fimOrigem >= intervalo[0] and fimOrigem <= intervalo[1]:
				
#				print('Quebrou fim!')
				quebrouFim = True
				if quebrouComeco:
					intervalosATestar.remove((comecoOrigem, intervalo[1]))
					intervalosATestar.append((comecoOrigem, fimOrigem))
					intervalosATestar.append((fimOrigem + 1, intervalo[1]))
				else:
					intervalosATestar.append((intervalo[0], fimOrigem))
					intervalosATestar.append((fimOrigem + 1, intervalo[1]))
			if quebrouComeco or quebrouFim:
				intervalosATestar.remove(intervalo)
#	print(intervalosATestar) #Ainda preciso testar isso?
#	input()
	novosIntervalos = [] # No final vou substituir esse antes de passar para o próximo nivel.

	for comecoIntervalo, fimIntervalo in intervalosATestar: #Pega cada 
		novoComeco = novoFim = None
		for conversao in conversoes:
			comecoDestino, comecoOrigem, comprimento = conversao
			if comecoIntervalo >= comecoOrigem and comecoIntervalo <= comecoOrigem + comprimento:
				novoComeco = comecoDestino + (comecoIntervalo - comecoOrigem)
				break

		for conversao in conversoes:
			comecoDestino, comecoOrigem, comprimento = conversao
			if fimIntervalo >= comecoOrigem and fimIntervalo <= comecoOrigem + comprimento:
				novoFim = comecoDestino + (fimIntervalo - comecoOrigem)
				break
		novosIntervalos.append((novoComeco if novoComeco else comecoIntervalo, novoFim if novoFim else fimIntervalo))
#	print('Acabou, novosIntervalos,', novosIntervalos)
#	print(destino)
#	input()
	intervalosATestar = novosIntervalos
	estadoAtual = destino

print(min(intervalosATestar)[0])	
#	sementesATestar.append(inicioIntervalo + comprimentoIntervalo)
#	print(sementesATestar)

#Tentativa: Testar só as seeds de cada intervalo.
#sementesATestar = []
#estadoAtual = 'seed'
#for indiceInformacoesSementes in range(int(len(sementes)/2)):
#	indice = indiceInformacoesSementes * 2
#	inicioIntervalo = sementes[indice]
#	comprimentoIntervalo = sementes[indice + 1]
#	sementesATestar.append(inicioIntervalo)
#	sementesATestar.append(inicioIntervalo + comprimentoIntervalo)
#	print(sementesATestar)













#extremidades = set()
#for caminho, conversoes in mapaConversoes.items():
#	for comecoDestino, comecoOrigem, comprimento in conversoes:
#		extremidades.add(comecoDestino)
#		extremidades.add(comecoOrigem)
#		extremidades.add(comecoDestino + comprimento)
#		extremidades.add(comecoDestino + comprimento)
#for indiceInformacoesSementes in range(int(len(sementes)/2)):
#	indice = indiceInformacoesSementes * 2
#	inicioIntervalo = sementes[indice]
#	comprimentoIntervalo = sementes[indice + 1]
#	extremidades.add(inicioIntervalo)
#	extremidades.add(inicioIntervalo + comprimentoIntervalo)
#extremidades = list(extremidades)
#extremidades.sort()
#dicionarioExtremidades = {extremidade: indice for indice, extremidade in enumerate(extremidades)}
#
#print(dicionarioExtremidades)
#
#locaisSementes = []
#for indiceInformacoesSementes in range(int(len(sementes)/2)):
#	indice = indiceInformacoesSementes * 2
#	inicioIntervalo = dicionarioExtremidades[sementes[indice]]
#	fimIntervalo = sementes[indice] + sementes[indice+1]
#	fimIntervalo = dicionarioExtremidades[fimIntervalo]
#	print(inicioIntervalo, fimIntervalo)
#	for semente in range(inicioIntervalo, fimIntervalo + 1):
#		estadoAtual = 'seed'
#		localAtual = semente 
#		while (estadoAtual != 'location'):
#			destino = [caminho[1] for caminho in mapaConversoes if caminho[0] == estadoAtual][0]
#			conversoes = mapaConversoes[(estadoAtual, destino)]
#			for conversao in conversoes:
#				comecoDestino, comecoOrigem, comprimento = conversao
#				fimDestino = comecoDestino + comprimento
#				fimOrigem = comecoOrigem + comprimento
#
#				comecoDestino = dicionarioExtremidades[comecoDestino]
#				fimDestino = dicionarioExtremidades[fimDestino]
#
#				comecoOrigem = dicionarioExtremidades[comecoOrigem]
#				fimOrigem = dicionarioExtremidades[fimOrigem]
#
#				if localAtual in range(comecoOrigem, fimOrigem + 1):
#					print(localAtual)
#					localAtual = comecoDestino + (localAtual - comecoOrigem)
#					print(localAtual)
#					print(extremidades[localAtual])
#					input()
#					break
#			estadoAtual = destino
#		locaisSementes.append(localAtual)
#print(min(locaisSementes))
#
