# Desafio do dia 01/12/2023:
# a) Receber uma lista de strings, e para cada uma concatenar o primeiro e último dígito.
# b) Ídem, porém cada dígito pode aparecer por extenso.

with open('input.txt') as file:
	linhas = file.read().splitlines()
	
mapa = {'one':'1', 
		'two':'2', 
		'three':'3', 
		'four':'4', 
		'five':'5', 
		'six':'6', 
		'seven':'7', 
		'eight':'8', 
		'nine':'9'}

resposta = 0
respostaParte2 = 0
for linha in linhas:
	numerosDaLinha = [caracter for caracter in linha if caracter.isnumeric()]
	if numerosDaLinha: # Apenas necessário para o input de teste.
		valorDaLinha = int(numerosDaLinha[0] + numerosDaLinha[-1])
	resposta += valorDaLinha

	# Parte 2:
	# Substituir o primeiro, e depois o último número por extenso de cada linha.
	# Depois seguir como na parte 1.

	linhaSubstituida = linha
	for indiceCaracter in range(len(linhaSubstituida)):
		if linhaSubstituida[indiceCaracter].isnumeric():
			break # O primeiro número não é por extenso. Não precisa substituir.
		for numeroPorExtenso, numero in mapa.items():
			if linhaSubstituida[indiceCaracter:].startswith(numeroPorExtenso):
				linhaSubstituida = linhaSubstituida.replace(numeroPorExtenso, numero, 1)
				break
		else: # Significa que neste índice não começa um número por extenso.
			continue
		break # Se chegou até aqui, já foi feita uma substituição e pode-se parar.
	# Idem porém começando pelo final da linha:
	for indiceCaracter in reversed(range(len(linhaSubstituida))):
		if linhaSubstituida[indiceCaracter].isnumeric():
			break
		for numeroPorExtenso, numero in mapa.items():
			if linhaSubstituida[indiceCaracter:].startswith(numeroPorExtenso):
				linhaSubstituida = linhaSubstituida[:indiceCaracter] + numero
				break
		else:
			continue
		break
	numerosDaLinha = [caracter for caracter in linhaSubstituida if caracter.isnumeric()]
	valorDaLinha = int(numerosDaLinha[0] + numerosDaLinha[-1])
	respostaParte2 += valorDaLinha

print('A soma dos valores de calibração é:', resposta)
print('A soma dos valores de calibração com os números por extenso é:', respostaParte2)
