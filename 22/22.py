import copy
with open('input.txt') as file:
	linhas = file.read().splitlines()


listaPedras = [] # Lista de Conjuntos. cada conjunto é uma pedra.
coordenadasOcupadas = set() # conjunto com todas as coordenadas ocupadas.

for linha in linhas:
	# 6,8,103~7,8,103	
	origem, destino = linha.split('~')
	origem = tuple(map(int, origem.split(',')))
	destino = tuple(map(int, destino.split(',')))
	delta = (min(1, abs(origem[0] - destino[0]),),
			 min(1, abs(origem[1] - destino[1]),),
			 min(1, abs(origem[2] - destino[2]),))
	setDestaPedra = {origem}
	while origem != destino:
		#incrementa um e adiciona no set dessa pedra
		origem = (origem[0] + delta [0], origem[1] + delta[1], origem[2]+delta[2])
		setDestaPedra.add(origem)
	listaPedras.append(setDestaPedra)
	coordenadasOcupadas.update(setDestaPedra)

# Vai, pedra a pedra, vendo se alguma pode cair:

caiuAlguma = True
#[print(x) for x in listaPedras]
#print('----------')
#[print(x) for x in coordenadasOcupadas]
#input()
#print('listaPedras', listaPedras)
#print()
while caiuAlguma:
	caiuAlguma = False
	for conjuntoPedra in listaPedras:
#		print('Fazendo pedra:', conjuntoPedra)
		#input()
		# Para essa pedra, vê se todos os bloquinhos tem algo embaixo:
		temAlgoEmbaixo = False
		conjuntoCaidoUmaUnidade = set()
		for coordenada in conjuntoPedra:
			z = coordenada[2]
			coordenadaInferior = (coordenada[0], coordenada[1], z-1)
#			print('\t coord inferior:', coordenadaInferior)
			conjuntoCaidoUmaUnidade.add(coordenadaInferior)
			if (coordenadaInferior in coordenadasOcupadas 
			and coordenadaInferior not in conjuntoPedra) or (z == 1):
#				print('\tOpa, tem algo embaixo, não pode mais descer.')
				temAlgoEmbaixo = True
				break
		#print('Coordenada dessa após cair:', conjuntoCaidoUmaUnidade)
		if temAlgoEmbaixo: # Não dá pra descer essa pedra, passa pra próxima
			continue
		
		# Se chegou aqui é porque dá pra cair uma:
		caiuAlguma = True

		#Atualizar o coordenadasOcupadas
		coordenadasOcupadas-= conjuntoPedra
		coordenadasOcupadas.update(conjuntoCaidoUmaUnidade)

		#Atualizar o conjuntoPedra:
		conjuntoPedra.clear()
		conjuntoPedra.update(conjuntoCaidoUmaUnidade)
		#print('---------------------------------')
#print('terminou')		
#[print(x) for x in listaPedras]

#print('-------------')
#[print(x) for x in sorted(coordenadasOcupadas)]
#print(conjuntoPedra)

#print('------------')
# Agora que todas caíram, ver para cada pedra, quais ela está em cima.
pedrasBaseDeAlguma = set() # Conjunto de conjuntos das pedras que servem de base pra outra.

for conjuntoPedra in listaPedras:
	# Para cada pedra, ver se ela depende só de uma:
	conjuntoCaidoUmaUnidade = set()
	for coordenada in conjuntoPedra:
		z = coordenada[2]
		coordenadaInferior = (coordenada[0], coordenada[1], z-1)
		conjuntoCaidoUmaUnidade.add(coordenadaInferior)
	# Agora tenho o conjunto das coordenadas inferiores. Ver a interseção com cada uma das pedras.
	listaPedrasDeBase = []
	for conjuntoPedra2 in listaPedras:
		if conjuntoPedra == conjuntoPedra2:
			continue
		#print('pedra1:', conjuntoPedra)
		#print('Embaixo dela:', conjuntoCaidoUmaUnidade)
		#print('Pedra2:', conjuntoPedra2)
		#print('Intersecao:', conjuntoPedra2.intersection(conjuntoCaidoUmaUnidade))
		#print('---------------------')
		if len(conjuntoPedra2.intersection(conjuntoCaidoUmaUnidade)):
			#print('appendou!')
			listaPedrasDeBase.append(conjuntoPedra2)
		#input()
	if len(listaPedrasDeBase) == 1: # Só está apoiado em um. Se esse sumir, cai.
		pedrasBaseDeAlguma.add(frozenset(listaPedrasDeBase[0]))

# Eu tenho:
# listaPedras -> Lista com todas as pedras estacionadas [{(x,y), (a,b)} , {...}]

print(len(listaPedras) - len(pedrasBaseDeAlguma))

#parte 2:

for base in pedrasBaseDeAlguma: # Remover essa e ver quantas caem.
	print(base in copy.deepcopy(listaPedras))
