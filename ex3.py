# Maximizar 𝑧 = 𝑥−(𝑥2+𝑦2) e domínio no intervalo [-2, +2]
import random
import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import sys
import numpy as np

class GeneticAlgorithm:
    def __init__(self):
        self.tamanho_populacao = 40
        self.populacao = []
        self.num_geracoes = 10
        self.num_filhos = 20
        self.filhos = []
        self.mutacao = 1
        self.all_populations = []

    def avaliar_individuo(self, x, y):
        var = x - (x ** 2 + y ** 2)
        return np.exp(var)

    def create_population(self):
        for _ in range(self.tamanho_populacao):
            x = random.uniform(-2, 2)
            y = random.uniform(-2, 2)
            fitness = self.avaliar_individuo(x, y)
            individuo = [x, y, fitness]
            self.populacao.append(individuo)

    def selecionar_pais(self):
        fitness_total = sum(individuo[2].real for individuo in self.populacao)
        if fitness_total == 0:
            print("Todos os valores de fitness são zero. Todos os pesos serão iguais.")
            pesos = [1 / len(self.populacao)] * len(self.populacao)  # Todos os pesos iguais
        else:
            pesos = [individuo[2].real / fitness_total for individuo in self.populacao]
        pai1 = random.choices(range(len(self.populacao)), weights=pesos)[0]
        pai2 = random.choices(range(len(self.populacao)), weights=pesos)[0]
        return pai1, pai2

    def realizar_mutacao(self, filho):
        for i in range(2):
            if random.random() < self.mutacao:
                filho[i] = random.uniform(-2, 2)
        return filho

    def realizar_descarte(self):
        self.populacao.sort(key=lambda x: x[2].real)
        del self.populacao[:-self.num_filhos]

    def verificar_melhor_individuo(self, geracao, output_file=None):
        melhor_individuo = max(self.populacao, key=lambda x: x[2].real)
        output = f"======================================\nGeração: {geracao}\nTamanho da População: {self.num_filhos}\nO melhor indivíduo:\nPopulação: {self.populacao}\nX = {melhor_individuo[0]}\nY = {melhor_individuo[1]}\nFitness = {melhor_individuo[2]}\n\n"

        print(output)

        if output_file:
            with open(output_file, "a") as f:
                f.write(output)

    def reproduzir(self):
        for _ in range(self.num_filhos // 2):
            pai1, pai2 = self.selecionar_pais()
            xf1, yf1 = self.populacao[pai1][:2]
            xf2, yf2 = self.populacao[pai2][:2]

            primeiro_filho_fitness = self.avaliar_individuo(xf1, yf1)
            segundo_filho_fitness = self.avaliar_individuo(xf2, yf2)

            filho1 = [xf1, yf1, primeiro_filho_fitness]
            filho2 = [xf2, yf2, segundo_filho_fitness]

            filho1 = self.realizar_mutacao(filho1)
            filho2 = self.realizar_mutacao(filho2)

            self.filhos.append(filho1)
            self.filhos.append(filho2)

    def init_execution(self, output_file=None):
        self.create_population()
        for contador_geracoes in range(1, self.num_geracoes + 1):
            self.reproduzir()
            self.populacao.extend(self.filhos)
            self.realizar_descarte()
            self.all_populations.append(self.populacao.copy())
            self.verificar_melhor_individuo(contador_geracoes, output_file)

    def plot_fitness(self):
        x = np.linspace(-2, 2, 100)
        y = np.linspace(-2, 2, 100)
        x, y = np.meshgrid(x, y)
        z = self.avaliar_individuo(x, y)

        figure = plt.figure()
        ax = figure.add_subplot(111, projection='3d')
        ax.plot_surface(x, y, z, cmap='viridis', alpha=.8)

        x_coordenada = [individual[0] for individual in self.populacao]
        y_coordenada = [individual[1] for individual in self.populacao]
        costs = [individual[2] for individual in self.populacao]

        ax.scatter(x_coordenada, y_coordenada, costs, color='red', label='Pontos da população')

        best = max(self.populacao, key=lambda x: x[2])
        ax.scatter(best[0], best[1], best[2], color='blue', s=100, label='O melhor indivíduo')

        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Custo')
        ax.set_title('Superfície da função custo')

        plt.legend()
        plt.show()

output_file = "ex3/exercicio3Alg.txt"
sys.stdout = open(output_file, "w")

algorithmInstance = GeneticAlgorithm()
algorithmInstance.init_execution(output_file)
algorithmInstance.plot_fitness()

