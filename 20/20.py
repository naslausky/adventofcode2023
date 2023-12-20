import copy

kEntradas = 'entradas'
kDestinos = 'destinos'
kTipo = 'tipo'
kEstadoAtual = 'estadoAtual'

modulos = {}
with open('input.txt') as file:
	linhas = file.read().splitlines()
	for linha in linhas:
		nome, destinos = linha.split(' -> ')
		tipo = ''
		if nome[0] in '%&':
			tipo, nome = nome[:1], nome[1:]
		destinos = destinos.split(', ')
		modulos[nome] = { kDestinos:tuple(destinos), 
							kTipo: tipo, 
							kEstadoAtual: False, #True if tipo == '&' else False,
							kEntradas: set()}
	for modulo, informacoes in modulos.items():
		for destino in informacoes[kDestinos]:
			if destino not in modulos: # Para o exemplo com output
				continue
			modulos[destino][kEntradas].add(modulo)

#[print(x, y) for x, y in modulos.items()]


impulsosBaixosEnviados = 0
impulsosAltosEnviados = 0

def apertarBotao(pulso = False):
	global impulsosBaixosEnviados, impulsosAltosEnviados
	modulosAVerificar = [] # Idealmente era pra ser uma fila.
	broadcaster = modulos['broadcaster']

	impulsosBaixosEnviados += 1
	broadcaster[kEstadoAtual] = pulso

	modulosAVerificar.extend(('broadcaster', destino) for destino in broadcaster[kDestinos])
	impulsosBaixosEnviados += len(broadcaster[kDestinos])
	
	while modulosAVerificar:
		origemDoPulso, nomeModuloAVerificar = modulosAVerificar.pop(0)
		if nomeModuloAVerificar not in modulos:
			continue
		modulo = modulos[nomeModuloAVerificar]
#		print('Fazendo modulo', nomeModuloAVerificar, 'do sinal vindo do:', origemDoPulso)
		tipoModuloAVerificar = modulo[kTipo]
		if tipoModuloAVerificar == '%':
#			print('\tÉ um Flip Flop.')
			pulsoRecebido = modulos[origemDoPulso][kEstadoAtual]
			if not pulsoRecebido: # Só faz algo se recebeu um pulso low.
#				print('\tPulso negativo recebido! Invertendo e comunicando os destinos.')
				#Inverte o estado atual:
				modulo[kEstadoAtual] = not modulo[kEstadoAtual]
				# Comunica os próximos.
				for destino in modulo[kDestinos]:
					modulosAVerificar.append((nomeModuloAVerificar, destino))

					if modulo[kEstadoAtual]:
						impulsosAltosEnviados += 1
					else:
						impulsosBaixosEnviados += 1

#				print('\tFila:', modulosAVerificar)
		elif tipoModuloAVerificar == '&':
#			print('\tÉ uma porta NAND.')
			# percorre todas as entradas fazendo o AND
			saidaDoNAND = False # if it remembers high pulses for all inputs, it sends a low pulse;
			
			for entrada in modulo[kEntradas]:
				if not modulos[entrada][kEstadoAtual]: # Basta ter um low para enviar high.
#					print('\tA entrada', entrada, 'estava low. Emitiu um High.')
					saidaDoNAND = True

			modulo[kEstadoAtual] = saidaDoNAND
				
			for destino in modulo[kDestinos]:
				modulosAVerificar.append((nomeModuloAVerificar, destino))
				if modulo[kEstadoAtual]:
					impulsosAltosEnviados += 1
				else:
					impulsosBaixosEnviados += 1
#			print('\tFila:', modulosAVerificar)
			
for _ in range(1000):
	apertarBotao()
print(impulsosBaixosEnviados * impulsosAltosEnviados)
