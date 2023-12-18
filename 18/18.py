# Desafio do dia 18/12/2023:
# a) Receber uma lista de movimentos e calcular a área interna deste polígono.
# b) Ídem, porém para os movimentos com coordenadas bem maiores.

with open('input.txt') as file:
	instrucoes = file.read().splitlines()
	
deltaDirecoes = {'R':(0, 1), 'L':(0, -1), 'U': (-1, 0), 'D': (1, 0)}
coordenadaAtual = (0,0)
coordenadaAtualParte2 = coordenadaAtual
listaVertices = [coordenadaAtual]
listaVerticesParte2 = [coordenadaAtual]

areaBorda = 0 # Área inicial cavada.
areaBordaParte2 = 0
for instrucao in instrucoes:
	direcao, quantidade, cor = instrucao.split()
	quantidade = int(quantidade)
	# Parte 2:
	quantidadeParte2 = int(cor[2:-2], 16)
	codigosDirecoes = {'0' : 'R', '1' : 'D', '2' : 'L', '3' : 'U'}
	direcaoParte2 = codigosDirecoes[cor[-2]]

	delta = deltaDirecoes[direcao]
	delta = (delta[0] * quantidade, delta[1] * quantidade)
	areaBorda+=quantidade
	coordenadaAtual = (coordenadaAtual[0] + delta[0], coordenadaAtual[1] + delta[1])
	listaVertices.append(coordenadaAtual)

	delta = deltaDirecoes[direcaoParte2]
	delta = (delta[0] * quantidadeParte2, delta[1] * quantidadeParte2)
	areaBordaParte2+=quantidadeParte2
	coordenadaAtualParte2 = (coordenadaAtualParte2[0] + delta[0], coordenadaAtualParte2[1] + delta[1])
	listaVerticesParte2.append(coordenadaAtualParte2)
	
def areaInterna(vertices): # Função que calcula a area interna de um polígono usando a fórmula do cadarço.
	areaInterna = 0
	for vertice1, vertice2 in zip(vertices[:-1], vertices[1:]):
		x1, y1 = vertice1
		x2, y2 = vertice2
		areaInterna += (x1 * y2) - (x2 * y1)
	return int(abs(areaInterna) / 2)

resposta = int(areaInterna(listaVertices) + areaBorda/2 + 1) # Quantidade de pontos internos pelo teorema de Pick.
respostaParte2 = int(areaInterna(listaVerticesParte2) + areaBordaParte2/2 + 1)
print('A área cavada é de:', resposta)
print('A área cavada usando a segunda interpretação é de:', respostaParte2)
