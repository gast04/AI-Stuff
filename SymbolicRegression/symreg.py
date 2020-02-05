from deap import algorithms
from deap import base
from deap import creator
from deap import tools
from deap import gp

import operator
import math
import random
import logging
import sys

# Define new functions
def safeDiv(left, right):
    try:
        return left / right
    except ZeroDivisionError:
        return 0

pset = gp.PrimitiveSet("MAIN", 1)
pset.addPrimitive(operator.add, 2)
pset.addPrimitive(operator.sub, 2)
pset.addPrimitive(operator.mul, 2)
pset.addPrimitive(safeDiv, 2)
pset.addPrimitive(operator.neg, 1)
pset.addPrimitive(math.cos, 1)
pset.addPrimitive(math.sin, 1)
pset.addEphemeralConstant("name2",lambda: random.randint(-1,1))
#pset.renameArguments({"ARG0" : "x"}) # rename function input argument

creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", gp.PrimitiveTree, fitness=creator.FitnessMin, pset=pset)

# register parameters specific for evolution process
toolbox = base.Toolbox()
toolbox.register("expr", gp.genHalfAndHalf, pset=pset, min_=1, max_=2)
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
#toolbox.register("lambdify", gp.lambdify, pset=pset)

def evalSymbReg(individual):
    # Transform the tree expression in a callable function
    func = toolbox.lambdify(expr=individual)
    # Evaluate the sum of squared difference between the expression
    # and the real function : x**4 + x**3 + x**2 + x
    values = (x/10. for x in xrange(-10,10))
    diff_func = lambda x: (func(x)-(x**4 + x**3 + x**2 + x))**2
    diff = sum(map(diff_func, values))
    return diff,

toolbox.register("compile", gp.compile, pset=pset)
toolbox.register("evaluate", evalSymbReg)
toolbox.register("select", tools.selTournament, tournsize=3)
#toolbox.register("mate", gp.cxUniformOnePoint)
toolbox.register("expr_mut", gp.genFull, min_=0, max_=2)
toolbox.register('mutate', gp.mutUniform, expr=toolbox.expr_mut)

#def main():
random.seed(318)

logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)

pop = toolbox.population(n=300)
hof = tools.HallOfFame(1)
stats = tools.Statistics(lambda ind: ind.fitness.values)
#stats.register("Avg", tools.mean)
#stats.register("Std", tools.std)
stats.register("Min", min)
stats.register("Max", max)

print(hof)

#algorithms.eaSimple(toolbox, pop, 0.5, 0.1, 40, stats, halloffame=hof)
logging.info("Best individual is %s, %s", hof[0], hof[0].fitness)

#return pop, stats, hof

#if __name__ == "__main__":
#    main()

