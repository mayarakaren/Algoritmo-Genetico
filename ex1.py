# Minimizar 𝑧 = 837,9658 − ∑ 𝑥𝑖2𝑖=1 ∗ sin(√|𝑥𝑖|) e domínio no intervalo [-500, +500]
import random
import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import sys
import numpy as np

class GeneticAlgorithm:
    def __init__(self):
        self.tamanho_populacao = 60
        self.populacao = []
        self.num_geracoes = 10
        self.num_filhos = 30
        self.filhos = []
        self.mutacao = 1
        self.all_populations = []  

    def avaliar_individuo(self, x1, x2):
        return 837.9658 - (self.avaliar_ponto(x1) + self.avaliar_ponto(x2))

    def avaliar_ponto(self, x):
        return np.sum(x * np.sin(np.sqrt(np.abs(x))))

    def create_population(self):
        for i in range(self.tamanho_populacao):
            x1 = round(random.randint(-500, 500))
            x2 = round(random.randint(-500, 500))

            fitness = self.avaliar_individuo(x1, x2)
            individual = [x1, x2, fitness]
            self.populacao.append(individual)

    def selecionar_pais(self):
        fitness_total = sum(individuo[2] for individuo in self.populacao)
        pesos = [individuo[2] / fitness_total for individuo in self.populacao]
        pai1 = random.choices(range(len(self.populacao)), weights=pesos)[0]
        pai2 = random.choices(range(len(self.populacao)), weights=pesos)[0]
        return pai1, pai2

    def realizar_mutacao(self, filho):
        for i in range(2):
            if random.random() < self.mutacao:
                filho[i] = random.randint(-500, 500)
        return filho

    def realizar_descarte(self):
        self.populacao.sort(key=lambda x: x[2])
        del self.populacao[:-self.num_filhos]
    
    def verificar_melhor_individuo(self, geracao, output_file=None):
        melhor_individuo = min(self.populacao, key=lambda x: x[2])
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
        x = np.linspace(-500, 500, 100)
        y = np.linspace(-500, 500, 100)
        x, y = np.meshgrid(x, y)
        z = np.zeros_like(x)

        for i in range(x.shape[0]):
            for j in range(x.shape[1]):
                z[i, j] = 837.9658 - (self.avaliar_ponto(x[i, j]) + self.avaliar_ponto(y[i, j]))

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_surface(x, y, z, cmap='viridis', alpha=0.8)

        x_coordinate = [individual[0] for individual in self.populacao]
        y_coordinate = [individual[1] for individual in self.populacao]
        costs = [individual[2] for individual in self.populacao]
        #ax.scatter(x_coordinate, y_coordinate, costs, color='red', label='Ótimos pontos')

        best = min(self.populacao, key=lambda x: x[2])
        ax.scatter(best[0], best[1], best[2], color='blue', s=100, label='O melhor indíviduo')

        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Custo')
        ax.set_title('Superfície da função custo')

        plt.legend()
        plt.show()

output_file = "ex1/exercicio1Alg.txt"
sys.stdout = open(output_file, "w")

algorithmInstance = GeneticAlgorithm()
algorithmInstance.init_execution(output_file)
algorithmInstance.plot_fitness()
