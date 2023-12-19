
with open('input.txt') as file:
	workflows, pecas = file.read().split('\n\n')
	workflows = workflows.splitlines()
	pecas = pecas.splitlines()

class NoVerificacao:
	def __init__(self, regras):
		# regras = a<2006:qkq,m>2090:A,rfg

		self.verificacao, caminhos = regras.split(':', 1) # a<2006
		self.caminhoVerdadeiro, self.caminhoFalso = caminhos.split(',', 1)

		if ':' in self.caminhoVerdadeiro:
			self.caminhoVerdadeiro = NoVerificacao(self.caminhoVerdadeiro)

		if ':' in self.caminhoFalso:
			self.caminhoFalso = NoVerificacao(self.caminhoFalso)
		# Cada caminho pode ser uma string ou um Nó para outra verificação.	

	def percorrerPeca(self, peca):
		verificacaoComValores = self.verificacao
		for chave, valor in peca.items():
			verificacaoComValores = verificacaoComValores.replace(chave, valor)
		verificacaoPassou = eval(verificacaoComValores)
		proximoNoAAvaliar = self.caminhoVerdadeiro if verificacaoPassou else self.caminhoFalso
		if type(proximoNoAAvaliar) is str:
			return proximoNoAAvaliar

		return proximoNoAAvaliar.percorrerPeca(peca)

mapaWorkflows = {}
for workflow in workflows:
	nome, regras = workflow.split('{')
	regras = regras[:-1]
	verificacao = NoVerificacao(regras)
	mapaWorkflows[nome] = verificacao

listaPecas = []
for peca in pecas:
	dicionarioDestaPeca = {}
	for variavel in peca[1:-1].split(','):
		nome, valor = variavel.split('=')
		#valor = int(valor)
		dicionarioDestaPeca[nome] = valor
	listaPecas.append(dicionarioDestaPeca)
resposta = 0
for peca in listaPecas:
	# peca = {a = 123, b = 345, x=789, s=12557}
#	print('Fazendo peca:', peca)
	workflowAtual = 'in'
	while workflowAtual != 'R' and workflowAtual != 'A':
		workflow = mapaWorkflows[workflowAtual]
		workflowAtual = workflow.percorrerPeca(peca)
#		print(workflowAtual)

	if workflowAtual == 'A':
		for valor in peca.values():
			resposta += int(valor)
print(resposta)
