# Desafio do dia 08/12/2023:
# a) Receber uma matriz de conexões e um caminho. Calcular o número de passos necessários entre dois nós.
# b) Idem, porém calcular o número de passos necessários que todas os nós terminando em 'A' cheguem nos 'Z' ao mesmo tempo.

# import math # A função de máximo divisor comum foi para a biblioteca math na versão mais nova do Python.
import fractions
with open('input.txt') as file:
	linhas = file.read()
	instrucoes, mapas = linhas.split('\n\n')
	mapas = mapas.splitlines()
	caminhos = {} # Dicionário que relaciona cada nó a seus sucessores: {'AAA':{'L':'BBB','R':'CCC'} ...}
	for mapa in mapas:
		origem, destino = mapa.split(' = (')
		destino = destino[:-1]
		destino = destino.split(', ')
		destino = {'L': destino[0], 'R': destino[1]}	
		caminhos[origem] = destino

salaAtual = 'AAA'
indiceInstrucaoAtual = 0 # O índice atual poderia ser obtido através da quantidade de passos.
quantidadeDePassos = 0
while salaAtual != 'ZZZ':
	instrucao = instrucoes[indiceInstrucaoAtual]
	proximaSala = caminhos[salaAtual][instrucao]
	salaAtual = proximaSala
	indiceInstrucaoAtual = (indiceInstrucaoAtual + 1) % len(instrucoes)
	quantidadeDePassos += 1 
print('A quantidade de passos necessária para chegar ao fim é:', quantidadeDePassos)

# Parte 2:
salasIniciais = [sala for sala in caminhos if sala.endswith('A')]
conjuntosCaminhos = {sala: set() for sala in salasIniciais} # Conjunto para detectar repetição, i.e. se uma mesma sala foi atingida com o mesmo índice de instrução.
intervalos = [] # Lista para calcular o MMC.
for sala, conjunto in conjuntosCaminhos.items():
	salaAtual = sala
	indiceInstrucaoAtual = 0
	quantidadeDePassos = 0
	while (salaAtual, indiceInstrucaoAtual) not in conjunto:
	# Se uma mesma sala foi atingida com o mesmo índice de instrução, é um ciclo e não precisa percorrer mais.
		conjunto.add((salaAtual, indiceInstrucaoAtual))
		instrucao = instrucoes[indiceInstrucaoAtual]
		proximaSala = caminhos[salaAtual][instrucao]
		salaAtual = proximaSala
		indiceInstrucaoAtual = (indiceInstrucaoAtual + 1) % len(instrucoes)
		quantidadeDePassos += 1
		# Essa solução presume duas coisas, que não são necessariamente verdade em um input genérico:
		# 1) Que cada sala terminando em 'A', vê, ao percorrer seu caminho, apenas uma sala de final 'Z'.
		# 2) Que não exista um intervalo inicial antes de entrar no ciclo: 
		# i.e. A sala "ABZ" ocorre nos passos 100, 200, 300... (ao invés de 50,150,250...)
		# Se fosse o caso, seria necessário aplicar aritmética modular.
		if salaAtual.endswith('Z'): 
			intervalos.append(quantidadeDePassos)

resposta = 1
for numero in intervalos: # Calcula o MMC para todas os ciclos encontrados.
	produto = resposta * numero
	#resposta = produto // math.gcd(numero, resposta) # Para versões mais novas do Python.
	resposta = produto // fractions.gcd(numero, resposta)
print('O menor número de passos para chegar ao fim em todas as salas ao mesmo tempo é:', resposta)
