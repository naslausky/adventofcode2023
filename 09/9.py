# Desafio do dia 09/12/2023:
# a) Receber uma lista de sequências discretas. Sendo as sequências geradas por polinomios, extrapolar a cada sequência para descobrir o próximo elemento e somar todos.
# b) Ídem porém para os números anteriores.

with open('input.txt') as file:
	linhas = file.read().splitlines()

resposta = 0
respostaParte2 = 0
for linha in linhas:
	numeros = linha.split()
	numeros = tuple(map(int, numeros))
	maioresNumerosDessaLinha = [] # A resposta da parte 1 é a soma de todos os elementos dessa lista.
	menoresNumerosDessaLinha = [] # A da parte 2 é a redução dessa lista com a subtração.
	while (any(numeros)):
		maioresNumerosDessaLinha.append(numeros[-1])
		menoresNumerosDessaLinha.append(numeros[0])
		numeros = [b-a for a, b in zip(numeros[:-1],numeros[1:])]
	resposta += sum(maioresNumerosDessaLinha)
	
	# Parte 2:
	valorAtual = 0
	menoresNumerosDessaLinha.reverse()
	for numero in menoresNumerosDessaLinha:
		valorAtual = numero - valorAtual
	respostaParte2 += valorAtual

print('A soma do próximo elemento de todas as sequências é:', resposta)
print('A soma do elemento anterior de todas as sequências é:', respostaParte2)
