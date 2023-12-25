# Desafio do dia 22/12/2023:
# a) Receber uma lista de tijolos que estão caindo. Terminar de cair todos os tijolos e quando eles formarem uma pilha, calcular quais são seguros de remover sem que outros caiam.
# b) Calcular quantos tijolos cairiam caso cada um deles fosse removido.

import copy
with open('input.txt') as file:
	linhas = file.read().splitlines()

listaTijolos = [] # Lista de conjuntos, em que cada conjunto são as coordenadas ocupadas por um tijolo.
coordenadasOcupadas = set() # Conjunto com todas as coordenadas ocupadas.

for linha in linhas:
	origem, destino = linha.split('~')
	origem = tuple(map(int, origem.split(',')))
	destino = tuple(map(int, destino.split(',')))
	delta = (min(1, abs(origem[0] - destino[0]),),
			 min(1, abs(origem[1] - destino[1]),),
			 min(1, abs(origem[2] - destino[2]),))
	setDestaPedra = {origem}
	while origem != destino: # Adiciona todas as coordenadas intermediárias ao conjunto.
		origem = (origem[0] + delta [0], origem[1] + delta[1], origem[2] + delta[2])
		setDestaPedra.add(origem)
	listaTijolos.append(setDestaPedra)
	coordenadasOcupadas.update(setDestaPedra)

def estacionarTijolos(listaTijolos, coordenadasOcupadas, parte2 = False): # Função que recebe a lista e faz todos caírem até onde dá.  
	caiuAlguma = True
	indicesTijolosQueCairam = set() # Para contabilizar para a parte 2.
	while caiuAlguma:
		caiuAlguma = False
		for indiceTijolo, tijolo in enumerate(listaTijolos): # Para um tijolo, ver se todas as coordenadas inferiores estão livres.
			if parte2 and indiceTijolo in indicesTijolosQueCairam:
				continue # Cada tijolo só precisa cair uma unidade para a parte 2.
			temAlgoEmbaixo = False
			conjuntoCaidoUmaUnidade = set()
			for coordenada in tijolo:
				z = coordenada[2]
				coordenadaInferior = (coordenada[0], coordenada[1], z-1)
				conjuntoCaidoUmaUnidade.add(coordenadaInferior)
				if (coordenadaInferior in coordenadasOcupadas 
				and coordenadaInferior not in tijolo) or (z == 1): # Atentar-se com um tijolo que já esteja na vertical.
					temAlgoEmbaixo = True
					break

			if temAlgoEmbaixo: # Não dá pra descer essa pedra, passa pra próxima.
				continue
			
			# Se chegou aqui é porque dá pra descer este tijolo em uma unidade. Atualizar as informações:
			indicesTijolosQueCairam.add(indiceTijolo) # Adiciona o índice do tijolo caído para a conta da parte 2.
			caiuAlguma = True
			coordenadasOcupadas-= tijolo
			coordenadasOcupadas.update(conjuntoCaidoUmaUnidade)
			tijolo.clear()
			tijolo.update(conjuntoCaidoUmaUnidade)
	return len(indicesTijolosQueCairam)

estacionarTijolos(listaTijolos, coordenadasOcupadas)
# Agora que todos caíram, ver para cada tijolo, quais ele está em cima.
# Se estiver em cima de apenas um, é porque esse é a unica base para ele.
tijolosBaseDeAlgum = set() # Conjunto de conjuntos das pedras que servem de base pra outra.
for tijolo in listaTijolos:
	conjuntoCaidoUmaUnidade = set()
	for coordenada in tijolo:
		z = coordenada[2]
		coordenadaInferior = (coordenada[0], coordenada[1], z-1)
		conjuntoCaidoUmaUnidade.add(coordenadaInferior)
	# Agora tenho o conjunto das coordenadas inferiores. Ver a interseção com cada uma das pedras.
	listaTijolosDeBase = []
	for tijolo2 in listaTijolos:
		if tijolo == tijolo2:
			continue
		if len(tijolo2.intersection(conjuntoCaidoUmaUnidade)):
			listaTijolosDeBase.append(tijolo2)
	if len(listaTijolosDeBase) == 1: # Só está apoiado em um. 
		tijolosBaseDeAlgum.add(frozenset(listaTijolosDeBase[0]))
print('A quantidade de tijolos desintegráveis é:', len(listaTijolos) - len(tijolosBaseDeAlgum))

#parte 2:
resposta = 0
for indiceBase, base in enumerate(tijolosBaseDeAlgum):
	listaSemABase = [pedra for pedra in copy.deepcopy(listaTijolos) if pedra != base]
	coordenadasOcupadasSemABase = copy.deepcopy(coordenadasOcupadas)
	for coordenada in base:
		coordenadasOcupadasSemABase.remove(coordenada)
	resposta+= estacionarTijolos(listaSemABase, coordenadasOcupadasSemABase, True)
print('A soma da quantidade de reações em cadeia é de:', resposta)
