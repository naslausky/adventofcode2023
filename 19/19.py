
with open('input.txt') as file:
	workflows, pecas = file.read().split('\n\n')
	workflows = workflows.splitlines()
	pecas = pecas.splitlines()

class NoVerificacao:
	def __init__(self, regras):
		# regras = a<2006:qkq,m>2090:A,rfg
		self.destinosPossiveis = {}
		self.verificacao, caminhos = regras.split(':', 1) # a<2006
		self.caminhoVerdadeiro, self.caminhoFalso = caminhos.split(',', 1)

		if ':' in self.caminhoVerdadeiro:
			self.caminhoVerdadeiro = NoVerificacao(self.caminhoVerdadeiro)

		if ':' in self.caminhoFalso:
			self.caminhoFalso = NoVerificacao(self.caminhoFalso)
		# Cada caminho pode ser uma string ou um Nó para outra verificação.	

		self.gerarDestinosPossiveis()

	def percorrerPeca(self, peca):
		verificacaoComValores = self.verificacao
		for chave, valor in peca.items():
			verificacaoComValores = verificacaoComValores.replace(chave, valor)
		verificacaoPassou = eval(verificacaoComValores)
		proximoNoAAvaliar = self.caminhoVerdadeiro if verificacaoPassou else self.caminhoFalso
		if type(proximoNoAAvaliar) is str:
			return proximoNoAAvaliar

		return proximoNoAAvaliar.percorrerPeca(peca)

	def verificacaoInversa(self,):
		if '>' in self.verificacao:
			nome, valor = self.verificacao.split('>')
			valor = str(int(valor) + 1)
			return nome + '<' + valor
			# a > 3000 o contrario é a <= 3000, ou seja a < 3001
		else:
			nome, valor = self.verificacao.split('<')
			valor = str(int(valor) - 1)
			return nome + '>' + valor

	# Eu preciso de um método que retorne uma lista de requisitos e a saída possível.
	# {(a<3000, b>5000, c<2000) : 'bcd', (a>2999) : 'A' }
	def gerarDestinosPossiveis(self,):
		# 
		if type(self.caminhoVerdadeiro) is str:
			self.destinosPossiveis[self.verificacao] = self.caminhoVerdadeiro
		else:
			for chave, valor in self.caminhoVerdadeiro.destinosPossiveis.items():
				self.destinosPossiveis[self.verificacao + ';' + chave] = valor

		if type(self.caminhoFalso) is str:
			self.destinosPossiveis[self.verificacaoInversa()] = self.caminhoFalso
		else:
			for chave, valor in self.caminhoFalso.destinosPossiveis.items():
				self.destinosPossiveis[self.verificacaoInversa() + ';' + chave] = valor
		

mapaWorkflows = {}
for workflow in workflows:
	nome, regras = workflow.split('{')
	regras = regras[:-1]
#	print('Fazendo verificação:', regras)
	verificacao = NoVerificacao(regras)
#	print('Dicionário:', verificacao.destinosPossiveis)
#	input()
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
	workflowAtual = 'in'
	while workflowAtual != 'R' and workflowAtual != 'A':
		workflow = mapaWorkflows[workflowAtual]
		workflowAtual = workflow.percorrerPeca(peca)
	if workflowAtual == 'A':
		for valor in peca.values():
			resposta += int(valor)
print(resposta)
# Parte 2:

requisitosAprovacao = set()
def percorrerDestinosAteOA(condicoesAteAgora, workflowAtual):
	workflow = mapaWorkflows[workflowAtual]
	for condicoes, destino in workflow.destinosPossiveis.items():
	#{'m<1450': 'R', 'm>1449;a>2836;a>2927': 'A', 'm>1449;a>2836;a<2928': 'R', 'm>1449;a<2837': 'R'}	
		condicoesParaEsteDestino = condicoesAteAgora + ';' + condicoes
		if destino == 'A':
			requisitosAprovacao.add(condicoesParaEsteDestino)
		elif destino in mapaWorkflows:
			percorrerDestinosAteOA(condicoesParaEsteDestino, destino)

percorrerDestinosAteOA('', 'in')
respostaParte2 = 0
for requisito in requisitosAprovacao:
	condicoes = [x for x in requisito.split(';') if x]
	minimo = 'min'
	maximo = 'max'
	mapaDesteRequisito = {chave:{minimo:1, maximo:4000} for chave in ('x','m','a','s')}
	for condicao in condicoes:
		if '>' in condicao: 
			# A> 300 significa que o minimo que A pode ser é 301
			# se vier um A>302 depois, significa que o minimo que A pode ser é 303, ou seja é max()
			chave = minimo
			funcao = max
			variavel, valor = condicao.split('>')
			valor = int(valor) + 1
		else:
			chave = maximo
			funcao = min
			variavel, valor = condicao.split('<')
			valor = int(valor) - 1

#		if variavel not in mapaDesteRequisito:
#			mapaDesteRequisito[variavel] = {minimo:0, maximo:5000}
		mapaDesteRequisito[variavel][chave] = funcao(*(valor, mapaDesteRequisito[variavel][chave]))
	#print(condicoes)
	#['m<10', 'm>3'] # 4,5,6,7,8,9 = 6 
	#'m': {'min': 3, 'max': 10}
	# 
	#print(mapaDesteRequisito)
	produto = 1
	for intervalo in mapaDesteRequisito.values():
		produto *= (intervalo[maximo] - intervalo[minimo] + 1)
	respostaParte2 += produto

print(respostaParte2)
exit()
def maneirasParaAprovar(requisitosAteAqui, workflowAtual):
	workflow = mapaWorkflows[workflowAtual]

	print('Fazendo workflow', workflowAtual)
	if type(workflow.caminhoVerdadeiro) is str:
		if workflow.caminhoVerdadeiro == 'A':
			requisitosAprovacao.add(requisitosAteAqui + workflow.verificacao)
	else:
		maneirasParaAprovar(requisitosAteAqui + workflow.verificacao, workflow.caminhoVerdadeiro)

	if type(workflow.caminhoFalso) is str:
		if workflow.caminhoFalso == 'A':
			requisitosAprovacao.add(requisitosAteAqui + workflow.verificacaoInversa())
	else:
		maneirasParaAprovar(requisitosAteAqui + workflow.verificacaoInversa(), workflow.caminhoFalso)

