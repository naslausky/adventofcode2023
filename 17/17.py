# Desafio do dia 17/12/2023:
# a) Receber uma matriz de custos para cada coordenada. Calcular o menor custo para ir do topo esquerdo até embaixo a direita.
#    Os caminhos só podem percorrer até no máximo 3 vezes na mesma direção.
# b) Idem, porém os caminhos devem percorrer no mínimo 4 vezes na mesma direção, e no máximo 10.

import queue # Para utilização da fila de prioridade.
with open('input.txt') as file:
	linhas = file.read().splitlines()

mapa = {}
for indiceLinha, linha in enumerate(linhas):
	for indiceCaracter, caracter in enumerate(linha):
		coordenada = (indiceLinha, indiceCaracter)
		mapa[coordenada] = int(caracter)

norte = (-1, 0)
sul = (1, 0)
oeste = (0, -1)
leste = (0, 1)

def h(x):
	return x[0][0]+x[0][1]

direcoesOpostas = {norte : sul, sul : norte, leste : oeste, oeste : leste}
coordenadaFinal = (len(linhas) - 1, len(linhas[-1]) - 1)
def menorCaminho(parte2 = False):
	vistos = set()
	alcancaveis = {((0,0), None, 0): 0} # Dicionário que relaciona uma coordenada a sua distância mínima.
	pq = queue.PriorityQueue()
	pq.put((0, ((0,0), None, 0)))
	coordenadasFinais = set((coordenadaFinal, direcao, n+1) for n in range(3 if not parte2 else 10) for direcao in (sul, leste))  # Mudar o range para a parte 2!

	while not coordenadasFinais.issubset(vistos) and len(vistos) != len(alcancaveis):
		chave = pq.get()[1]
		distanciaAteAqui = alcancaveis[chave] 
		coordenada, origem, quantidade = chave 
		proximasDirecoesPossiveis = [direcao for direcao in direcoesOpostas if direcao != direcoesOpostas.get(origem, None)]

		if parte2:
			if quantidade < 4 and origem: # Só pode seguir na mesma direção
				proximasDirecoesPossiveis = [origem]

		if quantidade == (3 if not parte2 else 10): 
			proximasDirecoesPossiveis.remove(origem) # Não pode andar + de 3 (ou 10 na parte 2) vezes na mesma direção.

		for proximaDirecao in proximasDirecoesPossiveis:
			proximaCoordenada = (coordenada[0] + proximaDirecao[0], coordenada[1] + proximaDirecao[1])
			proximaChave = (	proximaCoordenada, 
						proximaDirecao, 
						quantidade + 1 if proximaDirecao == origem else 1)

			if proximaCoordenada in mapa: # Se estiver dentro do mapa
				distanciaNoProximo = distanciaAteAqui + mapa[proximaCoordenada]
				if proximaChave in alcancaveis:
					if alcancaveis[proximaChave] > distanciaNoProximo: 
						alcancaveis[proximaChave] = distanciaNoProximo
						pq.put((
									distanciaNoProximo + h(proximaChave[0]),
									proximaChave)
								)
				else:
					alcancaveis[proximaChave] = distanciaNoProximo
					pq.put((
								distanciaNoProximo + h(proximaChave),
								proximaChave)
							)
		vistos.add(chave)
	return min(alcancaveis[final] for final in coordenadasFinais if final in alcancaveis)

print(menorCaminho())
print(menorCaminho(parte2 = True))
