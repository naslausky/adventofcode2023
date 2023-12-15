# Desafio do dia 15/12/2023:
# a) Receber uma lista de strings e uma função hash. Calcular a soma da hash de todas as strings.
# b) Criar um hash map para armazenar todas as instruções passadas, e calcular o estado final dele.

with open('input.txt') as file:
	linha = file.read().splitlines()[0]

instrucoes = linha.split(',')
def hashDaString(string): # Função que calcula a hash de uma dada string conforme as regras descritas.
	valorAtual = 0
	for caracter in string:
		valorAtual += ord(caracter)
		valorAtual *= 17
		valorAtual = valorAtual % 256
	return valorAtual

resposta = 0
hashMap = [[] for _ in range(256)] # Lista de listas representando as caixas de lentes.

for instrucao in instrucoes:
	resposta += hashDaString(instrucao) # Resposta da parte 1.
	divisor = '=' if '=' in instrucao else '-'
	etiqueta = instrucao.split(divisor)[0]
	indiceCaixaDestaEtiqueta = hashDaString(etiqueta)
	caixaDestaEtiqueta = hashMap[indiceCaixaDestaEtiqueta]
	if divisor == '-':
		hashMap[indiceCaixaDestaEtiqueta] = [lente for lente in caixaDestaEtiqueta if lente[0] != etiqueta]
	else:
		comprimentoFocal = int(instrucao.split(divisor)[1])
		lentesComEssaEtiqueta = [lente for lente in caixaDestaEtiqueta if lente[0] == etiqueta]
		if lentesComEssaEtiqueta:
			lente = lentesComEssaEtiqueta[0]
			indiceDestaLente = caixaDestaEtiqueta.index(lente)
			caixaDestaEtiqueta[indiceDestaLente] = (etiqueta, comprimentoFocal)
		else:
			caixaDestaEtiqueta.append((etiqueta, comprimentoFocal))

potenciaDeFoco = 0 # Resposta da parte 2.
for indiceCaixa, caixa in enumerate(hashMap):
	for indiceLente, infoLentes in enumerate(caixa):
		_, comprimentoFocal = infoLentes
		potenciaDeFoco += (indiceCaixa + 1) * (indiceLente + 1) * comprimentoFocal

print('A soma da hash de todas as instruções é:', resposta)
print('A soma da potência de foco de todas as lentes é:', potenciaDeFoco)
