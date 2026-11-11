import time as t
import random as rand
from pipes import *
import copy as cp

# this was from a previous assignment
'''
what this GA needs to do:

1: shuffle rotation on all pipes lists
2: score them by counting leaks and islands, more is worse
3: have groups of pipes compete for each value in popsize, taking only the best of them
4: combine the best pipe combos
5: occassionally rotate one random pipe in a winning child (mutation)
6: replace parent pipes with newly created children pipes
7: repeat
8: stop if we find a board w 0 cost

create new board -> shuffle board -> crossover -> mutate
'''
class GeneticAlgo:
    def __init__(self, grid, popSize=100, mutationRate=0.1, generations=5000): # base case constructor but overridable
        self.popSize = popSize # how many tours exist at once
        self.mutationRate = mutationRate #chance that a child is mutated
        self.generations = generations # how many rounds to run
        self.grid = grid
        self.size = len(grid.pipes)
    def randomBoard(self):
        board = cp.deepcopy(self.grid) # new pipes, dont want one board changing another
        for row in board.pipes:
            for pipe in row:
                for _ in range(rand.randint(0,3)):
                    pipe.rotate_pipe()
        return board
    def boardCost(self, board):
        leaksForAllPipes, islands = board.check_grid()
        totalLeaks = sum(leaks for tile, leaks in leaksForAllPipes) 
        return totalLeaks + 3 * (islands - 1) # islands are worth 3x the cost of leaks, 1 island is goal so it doesnt add anything if there's only one island
    def crossover(self, p1, p2):
        # take a random chunk of p1, then fill in the rest w p2s pipes in p2s order
        a, b = sorted(rand.sample(range(len(p1.pipes)), 2)) 
        # picks two random positions sorted makes sure a is the smaller one si a<b always
        chunk = p1.pipes[a:b]
        #copies the pipes from position a up to b out of parent 1
        return cp.deepcopy(Grid(p2.pipes[:a] + chunk +p2.pipes[b:]))
        #the child is build as the first a of cities of rest then the chunk, then the remaining rest putting the chunk in the same pos it had in parent 1
    def mutate(self, board):
        # rotates one random pipe
        row = rand.choice(board.pipes)
        rand.choice(row).rotate_pipe()
    def run(self):
        startTime = t.time() # starts timer
        population = [self.randomBoard() for _ in range(self.popSize)] 
        # random tours, basically shuffles eeverything
        self.bestHistory = [] # best cost every generation for tracking
        for gen in range(self.generations):
            # repeats for every generation
            population.sort(key=self.boardCost) # shortest first
            self.bestHistory.append(self.boardCost(population[0]))
            if self.bestHistory[-1] == 0: # this would mean it's been solved
                break
            newPopulation = population[:2] # keep the best 2 and it remains unchanged so it can never get worse 
            while len(newPopulation) < self.popSize:
                p1 = rand.choice(population[:self.popSize//2]) # parents only come from the best half
                p2 = rand.choice(population[:self.popSize//2])
                #basically this just keeps making babies until the gen is full
                child = self.crossover(p1, p2)
                if rand.random() < self.mutationRate: # if random num is generated and it hits the mutation rate then the mutation happens
                    self.mutate(child)
                newPopulation.append(child)
            population = newPopulation
        population.sort(key=self.boardCost)
        self.bestBoard = population[0]
        self.bestCost = self.boardCost(self.bestBoard)
        
        self.runTime = (t.time() - startTime) * 1000
        #sorts one last time, saves the tour and its ccost
        print(f"{self.runTime:.4f} ms, best cost {self.bestCost:.4f}")
        return self.bestBoard