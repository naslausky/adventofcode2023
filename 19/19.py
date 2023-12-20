# Desafio do dia 19/12/2023:
# a) Receber uma lista de regras, e uma lista de valores iniciais. Decidir quais valores quando passados pelas regras chegam no nó "A".
# b) Idem, porém calcular a quantidade de valores possíveis de serem aprovados.

with open('input.txt') as file:
	workflows, pecas = file.read().split('\n\n')
	workflows = workflows.splitlines()
	pecas = pecas.splitlines()

class NoVerificacao: # Classe que representa um nó com uma verificação apenas.
	def __init__(self, regras):
		self.verificacao, caminhos = regras.split(':', 1)  # self.verificação é uma string do tipo 'x<300'
		self.caminhoVerdadeiro, self.caminhoFalso = caminhos.split(',', 1) # Podem ser ou uma string com o nome de outro workflow do tipo 'abc' ou 'A', ou um outro nó de verificação.

		if ':' in self.caminhoVerdadeiro: # Significa que deve apontar para outra verificação.
			self.caminhoVerdadeiro = NoVerificacao(self.caminhoVerdadeiro) # Inicializa o próximo nó com as informações restantes.

		if ':' in self.caminhoFalso:
			self.caminhoFalso = NoVerificacao(self.caminhoFalso)

		self.destinosPossiveis = {} # Dicionário que contém todas as saídas possíveis quando uma peça entra nesta verificação.
		# Suas chaves são strings contendo restrições separadas por ponto e vírgula. Suas chaves são strings com os destinos.
		# Da forma: {'x<2;a>3': 'abc' , 'x<2;a<4':'A' ... }
		self.gerarDestinosPossiveis() # Método que popula o dicionário recursivamente.

	def percorrerPeca(self, peca): # Método que recebe uma peça e retorna uma string com o destino dela.
		verificacaoComValores = self.verificacao 
		for chave, valor in peca.items(): # Substitui os valores das variaveis para utilizar eval().
			verificacaoComValores = verificacaoComValores.replace(chave, valor) # e.g. a string 'S>300' vira '299>300'.
		verificacaoPassou = eval(verificacaoComValores) # O eval deve retornar um booleano indicando qual caminho deve-se seguir.
		proximoNoAAvaliar = self.caminhoVerdadeiro if verificacaoPassou else self.caminhoFalso

		if type(proximoNoAAvaliar) is str: # Caso tenha atingido um destino, retornar seu valor.
			return proximoNoAAvaliar
		return proximoNoAAvaliar.percorrerPeca(peca) # Senão, calcular as verificações seguintes.

	def verificacaoInversa(self,): # Método que inverte a verificação. Utilizado para não precisar se preocupar com verdadeiro/falso.
		# Isto é, se self.verificacao é 'a>300', retorna 'a<301'.
		# 'a > 300' ser falso, é idêntico a verificar que 'a<301' é verdadeiro.
		if '>' in self.verificacao: # Poderia ser refatorado para fazer as duas possibilidades em um loop.
			nome, valor = self.verificacao.split('>')
			valor = str(int(valor) + 1)
			return nome + '<' + valor
		else:
			nome, valor = self.verificacao.split('<')
			valor = str(int(valor) - 1)
			return nome + '>' + valor

	# Eu preciso de um método que retorne uma lista de requisitos e a saída possível.
	# {(a<3000, b>5000, c<2000) : 'bcd', (a>2999) : 'A' }
	def gerarDestinosPossiveis(self,): # Método que popula o dicionário self.destinosPossiveis.
		# Para cada um dos caminhos:
		# Caso ele seja um destino direto, pode popular o dicionário com a verificação relevante.
		# Se é outra verificação, adiciona a própria verificação a todas os destinos possíveis da verificação inferior.
		if type(self.caminhoVerdadeiro) is str:
			self.destinosPossiveis[self.verificacao] = self.caminhoVerdadeiro
		else:
			for verificacaoInferior, destino in self.caminhoVerdadeiro.destinosPossiveis.items():
				self.destinosPossiveis[self.verificacao + ';' + verificacaoInferior] = destino

		if type(self.caminhoFalso) is str: # Ídem que acima, porém para atingir o caminho falso a verificação inversa é utilizada.
			self.destinosPossiveis[self.verificacaoInversa()] = self.caminhoFalso
		else:
			for verificacaoInferior, destino in self.caminhoFalso.destinosPossiveis.items():
				self.destinosPossiveis[self.verificacaoInversa() + ';' + verificacaoInferior] = destino
		
mapaWorkflows = {} # Mapa que relaciona um nome do workflow ao seu nó de verificação inicial, da forma: {'abc': <Nó> , 'def':<Outro Nó>}
for workflow in workflows:
	nome, regras = workflow.split('{')
	regras = regras[:-1]
	verificacaoInicial = NoVerificacao(regras)
	mapaWorkflows[nome] = verificacaoInicial

listaPecas = [] # Lista com as peças a serem passadas pelos workflows. Da forma: [{'x':'300', 'm':'200', 'a':'100', 's':123} , {...}].
for peca in pecas:
	dicionarioDestaPeca = {}
	for variavel in peca[1:-1].split(','):
		nome, valor = variavel.split('=')
		dicionarioDestaPeca[nome] = valor
	listaPecas.append(dicionarioDestaPeca)

resposta = 0 # Resposta da parte 1.
for peca in listaPecas:
	workflowAtual = 'in' # Para cada peça, começar pelo workflow 'in'icial e percorrer os caminhos. 
	# Caso chegue no 'A', somar à resposta final.
	while workflowAtual != 'R' and workflowAtual != 'A': # Percorre os workflows até chegar no 'R' ou 'A'.
		workflow = mapaWorkflows[workflowAtual] 
		workflowAtual = workflow.percorrerPeca(peca)
	if workflowAtual == 'A': # Peça foi aprovada. Somar à resposta final.
		for valor in peca.values():
			resposta += int(valor)
print('A soma das propriedades de todas as peças aprovadas é de:', resposta)

# Parte 2:
requisitosAprovacao = set() # Conjunto de strings de requisitos que se seguidos levam a uma peça ser aprovada. Da forma: {'x<30;m>20;m>50'}.
def percorrerDestinosAteOA(condicoesAteAgora, workflowAtual): 
	# Função que percorre um workflow, verifica seu dicionário de destino, concatena suas restrições e chama ela mesma para cada destino.
	# Caso atinja o destino de aprovação 'A', salva no conjunto acima as restrições concatenadas até chegar lá.
	# Provavelmente poderia ser agregada à classe de verificação acima.
	workflow = mapaWorkflows[workflowAtual]
	for condicoes, destino in workflow.destinosPossiveis.items():
		condicoesParaEsteDestino = condicoesAteAgora + ';' + condicoes # Concatena a sua condição a cada uma das condições dos destinos possíveis.
		if destino == 'A':
			requisitosAprovacao.add(condicoesParaEsteDestino)
		elif destino in mapaWorkflows:
			percorrerDestinosAteOA(condicoesParaEsteDestino, destino)
percorrerDestinosAteOA('', 'in')

respostaParte2 = 0
for requisito in requisitosAprovacao: # Para cada possibilidade de atingir a aprovação, temos uma lista de requisitos.
	condicoes = [x for x in requisito.split(';') if x] # condicoes é da forma ['x>300', 'm'<'200']
	minimo = 'min'
	maximo = 'max'
	mapaDesteRequisito = {chave: {minimo : 1, maximo : 4000} for chave in ('x', 'm', 'a', 's')} # Intervalos inicialmente livres para cada propriedade.
	for condicao in condicoes:
		if '>' in condicao: 
			chave = minimo # Chave do dicionário para ser salvar. Significa que vamos salvar uma restrição de valor mínimo.
			funcao = max # Se houver duas restrições de mesmo tipo e propriedades, armazenar a com maior valor (e.g. x>200 e x>250).
			variavel, valor = condicao.split('>')
			valor = int(valor) + 1 # Salva no dicionário os valores inclusive (e.g. 'x>100' significa que o mínimo de x é 101).
		else:
			chave = maximo
			funcao = min
			variavel, valor = condicao.split('<')
			valor = int(valor) - 1

		mapaDesteRequisito[variavel][chave] = funcao(*(valor, mapaDesteRequisito[variavel][chave]))

	produto = 1 # A quantidade de combinações possíveis dado os intervalos das quatro propriedades.
	for intervalo in mapaDesteRequisito.values():
		produto *= (intervalo[maximo] - intervalo[minimo] + 1) # Quantidade de valores possíveis que uma propriedade pode adotar.
	respostaParte2 += produto

print('A quantidade possível de peças que poderiam ser aprovadas é:', respostaParte2)
