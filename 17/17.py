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

direcoesOpostas = {norte : sul, sul : norte, leste : oeste, oeste : leste} # Dicionário que relaciona cada direção ao seu oposto. Usado para não deixar voltar por onde veio.
coordenadaFinal = (len(linhas) - 1, len(linhas[-1]) - 1) # Objetivo é chegar aqui.

def menorCaminho(parte2 = False): # Função que aplica o Dijkstra e calcula o menor custo para atingir a coordenada final.
	# Uma chave é definida como a coordenada, de qual direção chegou e por quantas vezes consecutivas.
	vistos = set() # Quais coordenadas já foram visitadas e tem seu valor de distância correto.
	alcancaveis = {((0,0), None, 0): 0} # Dicionário que relaciona uma chave a sua distância mínima até agora.
	pq = queue.PriorityQueue() # Fila de prioridade para pegar sempre a menor próxima chave. Provavelmente poderia ser condensado com o dicionário acima.
	pq.put((0, ((0,0), None, 0))) # Adiciona o primeiro elemento à fila de prioridade.

	coordenadasFinais = set((coordenadaFinal, direcao, n+1) for n in range(3 if not parte2 else 10) for direcao in (sul, leste))  # Conjunto de chaves para determinar que nosso algoritmo terminou de rodar.
	while not coordenadasFinais.issubset(vistos) and len(vistos) != len(alcancaveis): # Acaba quando viu todas as possibilidades ou quando já calculou a distância para todas as formas de atingir as coordenadasFinais.
		chave = pq.get()[1] # Obtém o alcançável com menor distância.
		distanciaAteAqui = alcancaveis[chave] 
		coordenada, origem, quantidade = chave 
		proximasDirecoesPossiveis = [direcao for direcao in direcoesOpostas if direcao != direcoesOpostas.get(origem, None)] # Pode ir para qualquer canto, exceto de onde veio.

		if parte2:
			if quantidade < 4 and origem: # Só pode seguir na mesma direção caso esteja andando por menos de quatro vezes seguidas.
				proximasDirecoesPossiveis = [origem]

		if quantidade == (3 if not parte2 else 10): # Não pode andar mais de 3 (ou 10 na parte 2) vezes na mesma direção.
			proximasDirecoesPossiveis.remove(origem) # Nesse caso só sobra virar para os lados.

		for proximaDirecao in proximasDirecoesPossiveis: # Para cada uma das próximas coordenadas possíveis, calcula a próxima chave e a distância, e armazena.
			proximaCoordenada = (coordenada[0] + proximaDirecao[0], coordenada[1] + proximaDirecao[1])
			proximaChave = (	proximaCoordenada, 
								proximaDirecao,
								quantidade + 1 if proximaDirecao == origem else 1) # Se fez curva, começa a contar de 1 novamente.

			if proximaCoordenada in mapa: # Para evitar coordenadas fora do mapa.
				distanciaNoProximo = distanciaAteAqui + mapa[proximaCoordenada]
				if proximaChave in alcancaveis:
					if alcancaveis[proximaChave] > distanciaNoProximo: # Apenas salva a nova distância mínima se for menor do que a conhecida previamente.
						alcancaveis[proximaChave] = distanciaNoProximo
						pq.put((distanciaNoProximo, proximaChave))
				else:
					alcancaveis[proximaChave] = distanciaNoProximo
					pq.put((distanciaNoProximo, proximaChave))
		vistos.add(chave)
	return min(alcancaveis[final] for final in coordenadasFinais if final in alcancaveis) # A resposta é o menor valor dentre todas as formas de chegar à coordenada final.

print('A menor perda de calor com os cadinhos é:', menorCaminho())
print('A menor perda de calor com os ultra-cadinhos é:', menorCaminho(parte2 = True))
