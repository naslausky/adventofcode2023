with open('input.txt') as file:
	linhas = file.read().splitlines()

paredes = set()
esferas = set()
for indiceLinha, linha in enumerate(linhas):
	for indiceCaracter, caracter in enumerate(linha):
		coordenada = (indiceLinha, indiceCaracter)
		if caracter == '#':
			paredes.add(coordenada)
		elif caracter == 'O':
			esferas.add(coordenada)

def imprimirMapa():
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

numeroDeLinhas = len(linhas)
numeroDeColunas = len(linhas[0])
norte = (-1, 0)
sul = (1, 0)
oeste = (0, -1)
leste = (0, 1)
direcoes = (norte, oeste, sul, leste) # Na ordem certa do ciclo.
esferasParte2 = esferas.copy() # Salva para a parte 2.
algumaEsferaMoveu = True
while algumaEsferaMoveu:
	algumaEsferaMoveu = False
	coordenadasARemover = set()
	coordenadasAAdicionar = set()
	for esfera in esferas:
		coordenadaNorte = (esfera[0] + norte[0], esfera[1] + norte[1])
		if coordenadaNorte[0] < 0:
			continue
		if coordenadaNorte not in esferas and coordenadaNorte not in paredes: # Pode mover.
			coordenadasARemover.add(esfera)
			coordenadasAAdicionar.add(coordenadaNorte)
			algumaEsferaMoveu = True
	esferas-= coordenadasARemover
	esferas.update(coordenadasAAdicionar)

pesoTotal = 0
for esfera in sorted(esferas):
	pesoTotal+= numeroDeLinhas - esfera[0]
print(pesoTotal)

# Parte 2:
numeroDeCiclos = 1000000000
indiceCiclo = 0
esferas = esferasParte2
ciclos= {}
while indiceCiclo < numeroDeCiclos:

	chave = frozenset(esferas)
	if chave in ciclos: # repetiu
		periodo = indiceCiclo - ciclos[chave]
		passosAPular = (numeroDeCiclos - indiceCiclo) // periodo
		indiceCiclo += (passosAPular * periodo)
	ciclos[chave] = indiceCiclo

	for direcao in direcoes:
#		print('Direcao', direcao)
		# Dá uma rolada full nessa direção.
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
#					print('moveu', esfera, proximaCoordenada)
					algumaEsferaMoveu = True
			esferas-= coordenadasARemover
			esferas.update(coordenadasAAdicionar)
	indiceCiclo+= 1
pesoTotal = 0
for esfera in sorted(esferas):
	pesoTotal+= numeroDeLinhas - esfera[0]
print(pesoTotal)
