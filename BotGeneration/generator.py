'''
credits: https://github.com/gmichaelson/GA_in_python
'''

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

import random, copy, sys

from inst_list import *
from esilEmul import *
from compiler import *
from config import *


def create_new_bot(single_bot_start_size):
    # create a new bot with random instructions

    bot = Bot()
    start_size = single_bot_start_size # random.randint(3, single_bot_start_size)
    for i in range(start_size):
        bot.addInst(createRandomInst(bot))

    return bot


def create_starting_population(size, single_bot_start_size):
    # create random bots with a maximum number of instructions

    population = []
    for i in range(0,size):
        population.append(create_new_bot(single_bot_start_size))

    return population


'''
    design of fitness function for bots
    * + how much write damage
    * + how many successful executed instructions
    * - read/write/execute out of bounds
    * - execute invalid instruction
'''
def fitness(bot):

    # write bot to file and compile with rasm2
    codeasm = compileBot(bot)

    # emulate with ESIL
    executed, write_damage = emulate(codeasm)
    bot.addExDam(executed, write_damage)
    return executed, write_damage


def score_population(population):
    scores = []
    for i in range(0, len(population)):
        scores += [fitness(population[i])]

    return scores

'''
    weight bots
    damage counts more than execution
'''
def getBest(scores):
    score_sums = []
    for sc in scores:
        score_sums.append(sc[1]*damage_mult)
        #score_sums.append(sc[0] + sc[1]*damage_mult)

    return np.argmax(score_sums), score_sums


def crossover(a, b):         
    #print("crossover INP: {} - {}".format(a, b))

    # get length of bots
    len_A = a.len()
    len_B = b.len()
    
    cut_a = random.randint(1, len_A-2)
    cut_b = random.randint(1, len_B-2)
    
    new_a1 = a.getInsts()[:cut_a].copy()
    new_a2 = b.getInsts()[cut_b:].copy()

    new_b1 = b.getInsts()[:cut_b].copy()
    new_b2 = a.getInsts()[cut_a:].copy()
    
    new_a = new_a1 + new_a2
    new_b = new_b1 + new_b2
 
    new_BotA = Bot()
    new_BotA.setInsts(new_a)

    new_BotB = Bot()
    new_BotB.setInsts(new_b)

    #print("crossover OUT: {} - {}".format(new_a, new_b))

    return (new_BotA, new_BotB)


def replaceInsts(bot, probability):
    insts = bot.getInsts().copy()
    mutBot = Bot()

    mut = False
    for i in range(1, bot.len()-1):
        if random.random() < probability:   
            mut = True
          
            # replace from the i-th instruction with a random one
            ri = createRandomInst(mutBot)
            insts[i] = ri
            mutBot.setInsts(insts)

    # return mutated one if mutation happened
    if mut:
        return mutBot
    else:
        return bot


def bigMutation(bot, probability):
    insts = bot.getInsts().copy()
    mutBot = Bot()

    mut = False
    for i in range(1, bot.len()-1):
        if random.random() < probability:   
            mut = True
            # replace from the i-th instruction onwards
            new_insts = random.randint(3, 10)
            mutBot.setInsts(insts[:i])

            for k in range(new_insts):                    
                mutBot.addInst(createRandomInst(mutBot))

    # return mutated one if mutation happened
    if mut:
        return mutBot
    else:
        return bot


def mutate(bot, probability):
    if random.random() < 1:
        return replaceInsts(bot, probability)
    else:
        # is not a good way in my mind
        return bigMutation(bot, probability)


def pick_mate(scores):
    array = np.array(scores)
    temp = array.argsort()
    ranks = np.empty_like(temp)
    ranks[temp] = np.arange(len(array))

    fitness = [len(ranks) - x for x in ranks]
    cum_scores = copy.deepcopy(fitness)
    
    for i in range(1,len(cum_scores)):
        cum_scores[i] = fitness[i] + cum_scores[i-1]
        
    probs = [x / cum_scores[-1] for x in cum_scores]
    rand = random.random()
    
    for i in range(0, len(probs)):
        if rand < probs[i]:
            return i

def pickBest(population, keeps):
    bestbots = []

    for i in range(keeps):
        bestbot = None

        for bot in population:
            
            if bestbot is None:
                if bot in bestbots:
                    continue
                bestbot = bot
        
            if bot.getScore() > bestbot.getScore() and bot not in bestbots:
                bestbot = bot

        bestbots.append(bestbot)

    return bestbots


def main():

    # parameters
    population_size = 20
    single_bot_start_size = 20           # start bots have max x instructions
    number_of_iterations = 100
    number_of_couples = 3
    number_of_winners_to_keep = 5
    mutation_probability = 0.1

    # create the starting population
    population = create_starting_population(population_size, single_bot_start_size)

    last_score = (0,0)
    leading_bot = None

    # for a large number of iterations do:

    for i in range(0,number_of_iterations):
        new_population = []

        # evaluate the fitness of the current population
        scores = score_population(population)
        print("scores:")
        print(scores)

        best_index, sums = getBest(scores)
        best_bot = population[best_index]
        best_score = scores[best_index]

        if (best_score[1]*damage_mult) > (last_score[1]*damage_mult):
        #if (best_score[0] + best_score[1]*damage_mult) > (last_score[0] + last_score[1]*damage_mult):
        #if (best_score[1] > last_score[1]) or best_score[1] > 0 and best_score[0] > last_score[0]:
            print('Iteration %i: Best so far is %i/%i execution/damage' % (i, best_score[0], best_score[1]))
            print("\nBOT:")
            population[best_index].printBot()
            leading_bot = population[best_index]

        # allow members of the population to breed based on their relative score;
        # i.e., if their score is higher they're more likely to breed
        #for j in range(0, number_of_couples):
        #    new_1, new_2 = crossover(population[pick_mate(sums)], population[pick_mate(sums)])
        #    new_population = new_population + [new_1, new_2]

        # pick best and mutate those
        new_population += pickBest(population, number_of_winners_to_keep)

        # mutate
        for j in range(0, len(new_population)):
            new_population[j] = mutate(new_population[j], mutation_probability)


        # keep members of previous generation
        # rethink this, keep the best n bots unmodified
        new_population += pickBest(population, number_of_winners_to_keep)
        
        #new_population += [population[np.argmax(sums)]]
        #for j in range(0, number_of_winners_to_keep):
        #    keeper = pick_mate(sums)
        #    new_population += [population[keeper]]

        # add new random members
        while len(new_population) < population_size:
            new_population += [create_new_bot(single_bot_start_size)]

        #replace the old population with a real copy
        population = new_population.copy()

        last_score = best_score
 

    print("\nBest Evolution:")
    print(leading_bot.printBot())

###############################################################################
main()
