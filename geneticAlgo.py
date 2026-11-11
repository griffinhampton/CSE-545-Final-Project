from splitAlgo import *
from tspDict import *
import time
import random

# this was from a previous assignment
'''
what i need to do:

1:create a random batch of a ton of tours
2: score them by measuring total tour length
3: have groups of tours compete to empty the population a tad, keeping only the best
4: combine good tours
5: occasionally swap a few cities to mutate
6: replace tours with the newly created children tours
7: repeat a bunch of times
'''
class GeneticAlgo:
    def __init__(self, coords, popSize=100, mutationRate=0.1, generations=5000): # base case constructor but overridable
        self.coords = coords 
        self.popSize = popSize # how many tours exist at once
        self.mutationRate = mutationRate #chance that a child is mutated
        self.generations = generations # how many rounds to run

    def distanceBetweenNodes(self, x1, y1, x2, y2):
            # distance formula:
            # d = sqrt((x[1]-x[0])^2+(y[1]-y[0])^2)
            return sqrt((x2-x1)**2+(y2-y1)**2)
    def tourCost(self, tour):
        total = 0.0
        for i in range(len(tour)):
            a = tour[i]
            b = tour[(i+1) % len(tour)] # % so the last city connects back to the first
            total += self.distanceBetweenNodes(a[0], a[1], b[0], b[1]) # adds up the cost + total distance is the cost
        return total
    def crossover(self, p1, p2):
        # take a random chunk of p1, then fill in the rest w p2s cities in p2s order
        a, b = sorted(random.sample(range(len(p1)), 2)) 
        # picks two random positions sorted makes sure a is the smaller one si a<b always
        chunk = p1[a:b]
        #copies the cities from position a up to b out of parent 1
        rest = [city for city in p2 if city not in chunk]
        #iterates thru parent 2 in order and keeps every city that isnt alr in the chunk so the child has no dups and missing cities
        return rest[:a] + chunk + rest[a:]
        #the child is build as the first a of cities of rest then the chunk, then the remaining rest putting the chunk in the same pos it had in parent 1
    def mutate(self, tour):
        # reverse a random chunk of the tour
        a, b = sorted(random.sample(range(len(tour)), 2))
        tour[a:b] = tour[a:b][::-1]
        # ::-1 means reversed here (i'm learning more with python and data structures)

    def run(self):
        startTime = time.time() # starts timer
        population = [random.sample(self.coords, len(self.coords)) for _ in range(self.popSize)] 
        # random tours, basically shuffles eeverything
        self.bestHistory = [] # best cost every generation for tracking
        for gen in range(self.generations):
            # repeats for every generation
            population.sort(key=self.tourCost) # shortest first
            self.bestHistory.append(self.tourCost(population[0]))
            newPopulation = population[:2] # keep the best 2 and it remains unchanged so it can never get worse 
            while len(newPopulation) < self.popSize:
                p1 = random.choice(population[:self.popSize//2]) # parents only come from the best half
                p2 = random.choice(population[:self.popSize//2])
                #basically this just keeps making babies until the gen is full
                child = self.crossover(p1, p2)
                if random.random() < self.mutationRate: # if random num is generated and it hits the mutation rate then the mutation happens
                    self.mutate(child)
                newPopulation.append(child)
            population = newPopulation
        population.sort(key=self.tourCost)
        self.bestTour = population[0]
        self.bestCost = self.tourCost(self.bestTour)
        
        self.runTime = (time.time() - startTime) * 1000
        #sorts one last time, saves the tour and its ccost
        print(f"{self.runTime:.4f} ms, best cost {self.bestCost:.4f}")
        return self.bestTour