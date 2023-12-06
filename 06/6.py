# Desafio do dia 06/12/2023:
# a) Receber uma lista de corridas. Qualquer quantas formas diferentes podemos segurar o acelerador e ainda bater o recorde.
# b) Idem, porém para apenas uma corrida bem grande. 
import math
with open('input.txt') as file:
	linhas = file.read().splitlines()

tempos = linhas[0].split()[1:]
tempos = tuple(map(int, tempos))
distancias = linhas[1].split()[1:]
distancias = tuple(map(int, distancias))
corridas = [(tempo, distancia) for tempo, distancia in zip(tempos, distancias)]
resposta = 1
for corrida in corridas:
	formasDeGanharEstaCorrida = 0
	duracao, recorde = corrida
	for tempoSegurandoBotao in range(duracao):
		tempoCorrendo = duracao - tempoSegurandoBotao
		velocidade = tempoSegurandoBotao
		distanciaAlcancada = tempoCorrendo * velocidade
		if distanciaAlcancada > recorde:
			formasDeGanharEstaCorrida += 1
	resposta *= formasDeGanharEstaCorrida
print('O produto da quantidade de formas para ganhar as corridas é:', resposta)

# Parte 2:
duracao = int(''.join(linhas[0].split()[1:]))
recorde = int(''.join(linhas[1].split()[1:]))

# A distancia alcançada é (tempoSegurando) * (duracao - tempoSegurando)
# distancia = - tempoSegurando ** 2 + duracao * tempoSegurando >= recorde
# -tempoSegurando ** 2 + duracao* tempoSegurando - recorde = 0
# A resposta final é a quantidade de inteiros entre as duas raízes.
# Uma solução que testa todas as possibilidades também é possível e não demora muito para rodar (~10segs).
a = -1
b = duracao
c = - recorde
delta = (b ** 2 - 4 * a * c)
delta = delta ** (1/2)
raiz1 = (-b + delta) / (2*a)
raiz2 = (-b - delta) / (2*a)
maior = max(raiz1, raiz2)
menor = min(raiz1, raiz2)
formasDeGanharEstaCorrida = math.floor(maior) - math.ceil(menor) + 1
print('A quantidade de formas para ganhar a corrida gigante é:', formasDeGanharEstaCorrida)
