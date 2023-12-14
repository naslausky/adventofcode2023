# Desafio do dia 14/12/2023:
# a) Receber um mapa com esferas e paredes. Calcular o estado final após inclinar as esferas para rolarem para norte.
# b) Calcular o estado final após realizar 1000000000 ciclos de inclinações para os quatro lados.

with open('input.txt') as file:
	linhas = file.read().splitlines()

paredes = set() # Conjunto das coordenadas das paredes que as esferas não podem atravessar.
esferas = set() # Conjunto das coordenadas das esferas.
numeroDeLinhas = len(linhas)
numeroDeColunas = len(linhas[0])

for indiceLinha, linha in enumerate(linhas):
	for indiceCaracter, caracter in enumerate(linha):
		coordenada = (indiceLinha, indiceCaracter)
		if caracter == '#':
			paredes.add(coordenada)
		elif caracter == 'O':
			esferas.add(coordenada)

def imprimirMapa(): # Função de depuração que imprime o estado atual das esferas.
	for indiceLinha in range(numeroDeLinhas):
		for indiceCaracter in range(numeroDeColunas):
			chave = (indiceLinha, indiceCaracter)
			caracter = '.'
			if chave in esferas:
				caracter = 'O'
			if chave in paredes:
				caracter = '#'
			print(caracter, end = '')
		print('')

def moverEsferasEmUmaDirecao(esferas, direcao): # Função que recebe um conjunto de esferas e move todas ao máximo para a direção dada.
	algumaEsferaMoveu = True
	while algumaEsferaMoveu:
		algumaEsferaMoveu = False
		coordenadasARemover = set()
		coordenadasAAdicionar = set()
		for esfera in esferas:
			proximaCoordenada = (esfera[0] + direcao[0], esfera[1] + direcao[1])
			if (proximaCoordenada[0] not in range(numeroDeLinhas) 
				or proximaCoordenada[1] not in range(numeroDeColunas)):
				continue
			if proximaCoordenada not in esferas and proximaCoordenada not in paredes: # Pode mover.
				coordenadasARemover.add(esfera)
				coordenadasAAdicionar.add(proximaCoordenada)
				algumaEsferaMoveu = True
		esferas-= coordenadasARemover
		esferas.update(coordenadasAAdicionar)

def calcularPeso(esferas): # Função que calcula o peso final das esferas.
	pesoTotal = 0
	for esfera in esferas:
		pesoTotal+= numeroDeLinhas - esfera[0]
	return pesoTotal

norte = (-1, 0)
sul = (1, 0)
oeste = (0, -1)
leste = (0, 1)
direcoes = (norte, oeste, sul, leste) # Na ordem certa do ciclo.
esferasParte2 = esferas.copy() # Salva para a parte 2.
moverEsferasEmUmaDirecao(esferas, norte)
print('O peso total nas vigas norte após uma movimentação é de:', calcularPeso(esferas))

# Parte 2:
numeroDeCiclos = 1000000000
indiceCiclo = 0
esferas = esferasParte2
ciclos = {} # Mapa para armazenar caso um estado do tabuleiro já tenha ocorrido.
while indiceCiclo < numeroDeCiclos:

	chave = frozenset(esferas) # Chave para salvar os estados.
	if chave in ciclos: # Significa que este estado já aconteceu em um ciclo anterior.
		periodo = indiceCiclo - ciclos[chave]
		passosAPular = (numeroDeCiclos - indiceCiclo) // periodo
		indiceCiclo += (passosAPular * periodo)
	ciclos[chave] = indiceCiclo

	for direcao in direcoes:
		moverEsferasEmUmaDirecao(esferas, direcao)
	indiceCiclo+= 1

print('O peso total nas vigas norte após 1000000000 ciclos é de:', calcularPeso(esferas))
