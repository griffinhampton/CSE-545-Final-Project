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
    def __init__(self, grid, popSize=500, mutationRate=0.1, generations=5000, visualize = False, vis_interval = 100, locked=None, stallLimit=150): # base case constructor but overridable
        self.popSize = popSize # how many tours exist at once
        self.mutationRate = mutationRate #chance that a child is mutated
        self.generations = generations # how many rounds to run
        self.grid = grid
        self.size = len(grid.pipes)
        self.visualize = visualize
        self.locked = locked
        self.stallLimit = stallLimit
        self.vis_interval = vis_interval
    def isLocked(self, pipe):
        return self.locked is not None and self.locked[pipe.row][pipe.col]
    def copyBoard(self,board):
        return Grid([[Pipe(p.pipe, p.row, p.col) for p in row] for row in board.pipes])
    def randomBoard(self):
        board = self.copyBoard(self.grid) # new pipes, dont want one board changing another
        for row in board.pipes:
            for pipe in row:
                for _ in range(rand.randint(0,3)):
                    pipe.rotate_pipe()
        return board
    def boardCost(self, board):
        leaksForAllPipes, islands = board.check_grid()
        totalLeaks = sum(leaks for tile, leaks in leaksForAllPipes) 
        return totalLeaks + 2 * (islands - 1) # islands are worth 3x the cost of leaks, 1 island is goal so it doesnt add anything if there's only one island
    def crossover(self, p1, p2):
        # take a random chunk of p1, then fill in the rest w p2s pipes in p2s order
        rows, cols = len(p1.pipes), len(p1.pipes[0])
        r1, r2 = sorted(rand.sample(range(rows + 1), 2)) # +1 so the last row/col can be picked too
        c1, c2 = sorted(rand.sample(range(cols + 1), 2))
        child = []
        for r in range(rows):
            row = []
            for c in range(cols):
                parent = p1 if (r1 <= r < r2 and c1 <= c < c2) else p2
                row.append(Pipe(parent.pipes[r][c].pipe, r, c))
            child.append(row)
        return Grid(child)
    def localLeaks(self, board, pipe):
        # leaks on this tile plus the 4 tiles around it
        total = pipe.check_leaks(board.pipes)
        for n in pipe.check_neighbors(board.pipes):
            if n is not None:
                total += n.check_leaks(board.pipes)
        return total
    def mutate(self, board):
        # rotates one random pipe
        row = rand.choice(board.pipes)
        rand.choice(row).rotate_pipe()
    def run(self):
        startTime = t.time() # starts timer
        population = [self.randomBoard() for _ in range(self.popSize)]
        self.bestHistory = [] # best cost every generation for tracking
        best_so_far = float("inf") # has to be set before the loop or visualize crashes
        lastImprove = 0
        for gen in range(self.generations):
            population.sort(key=self.boardCost) # lowest cost first
            current_best = self.boardCost(population[0])
            self.bestHistory.append(current_best)

            improved = current_best < best_so_far
            if improved:
                best_so_far = current_best
                lastImprove = gen
            if self.visualize and (improved or gen % self.vis_interval == 0):
                show_grid(population[0], pause_time=0.01, title=f"Gen {gen} | Cost: {current_best}")

            if current_best == 0: # solved
                break
            if gen - lastImprove >= self.stallLimit: # stuck, more gens wont help
                break

            newPopulation = population[:2] # keep the best 2 so it can never get worse
            parents = population[:max(2, self.popSize // 2)] # parents only come from the best half
            while len(newPopulation) < self.popSize:
                p1 = rand.choice(parents)
                p2 = rand.choice(parents)
                child = self.crossover(p1, p2)
                if rand.random() < self.mutationRate:
                    self.mutate(child)
                newPopulation.append(child)
            population = newPopulation

        population.sort(key=self.boardCost)
        self.bestBoard = population[0]
        self.bestCost = self.boardCost(self.bestBoard)

        self.runTime = (t.time() - startTime) * 1000
        print(f"{self.runTime:.0f} ms, {len(self.bestHistory)} gens, best cost {self.bestCost}")
        return self.bestBoard