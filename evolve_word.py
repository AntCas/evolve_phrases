import random

# ---- Constants/Control Variables ----

TARGET_PHRASE = "To be or not to be."
SIZE_OF_GENERATION = 200 # number of organisms per generation
MUTATION_RATE = .01 # Chance of a character randomly mutating
MIN_CHAR = 63 # ' '
MAX_CHAR = 122 # '~'
CHAR_RANGE = MAX_CHAR - MIN_CHAR

# ---- Functions -----

# fitness is the percentage of correct characters of an organism vs the target
def fitness(organism):
    total_correct = 0
    for i in xrange(len(organism)):
        if organism[i] == TARGET_PHRASE[i]:
            total_correct += 1
    return total_correct / float(len(organism))

# Generate the initial (seed) generation
def gen_seed_generation(length):
    generation = [""] * SIZE_OF_GENERATION
    for i in xrange(len(generation)):
        generation[i] = gen_rand_org(length)
    return generation
    
# returns a random character within the range (w/ addition of ' ', and '.')
def rand_char():
    c = random.randint(MIN_CHAR, MAX_CHAR)
    if c == 63:
        c = 32
    elif c == 64:
        c = 46
    return chr(c)

# generate a random organism length characters long
def gen_rand_org(length):
    organism = [''] * length
    for i in xrange(length):
        organism[i] = rand_char()
    return ''.join(organism)

# return a list of tuples mapping organisms to their score
def score_generation(generation):
    return [(organism, fitness(organism)) for organism in generation]

# randomly mutates a character some percentage of the time
def mutate(character, rate):
    if random.random() < rate:
        return rand_char()
    else:
        return character

# breeds two organisms
def breed(mother, father):
    if len(mother) != len(father):
        print "LENGTH ERROR"
        exit(1)

    # A child randomly inherits each character from either the mother or the father
    child = [""] * len(mother)
    for i in xrange(len(mother)):
        # This line would always give the child the strongest attribute (unfair)
        # child[i] = mother[i] if fitness(mother) >= fitness(father) else father[i]
        child[i] = mother[i] if random.random() < .5 else father[i]
        child[i] = mutate(child[i], MUTATION_RATE)

    return ''.join(child)

# assigns each organism a breeding potential based on its relative score
def gen_gene_pool(scored_generation):
    # each organism gets exactly the share of the gene pool it contributes
    total_fitness = sum(w for c,w in scored_generation)
    gene_pool = [(c, w / float(total_fitness)) for c,w in scored_generation]
    return gene_pool

# selects an organism to be a father based on its relative fitness
# source: http://stackoverflow.com/questions/3679694/a-weighted-version-of-random-choice
def select_father(gene_pool, mother):
    total = sum(w for c, w in gene_pool)
    r = random.uniform(0, total)
    upto = 0
    for c, w in gene_pool:
        if upto + w >= r:
            return c
        upto += w
    print gene_pool
    assert False, "Shouldn't get here" # No more diversity left in the gene pool

# generate the next generation of the algorithm
def gen_next_generation(generation):
    if len(generation) is 0:
        return gen_seed_generation(len(TARGET_PHRASE))
    else:
        next_generation = [""] * SIZE_OF_GENERATION

        # score each organism based on its fitness
        scored_generation = score_generation(generation)

        # create the gene pool (roulette wheel)
        gene_pool = gen_gene_pool(scored_generation)

        # breed each organism with a father in the gene pool
        for i in xrange(len(generation)):
            father = select_father(gene_pool, generation[i])
            next_generation[i] = breed(generation[i], father)

        return next_generation

# generates a status report
def gen_status(generation, num_generations):
    avg_fitness = sum(w for c,w in score_generation(generation)) / float(len(generation))
    return ("\nCurrent generation: %s | average fitness: %s | population size: %s" %
            (str(num_generations),
            str(avg_fitness),
            str(SIZE_OF_GENERATION)))

# Use a genetic algorithm to generate the target phrase
def run_genetic_word_finder():
    num_generations = 0
    generation = []
    found = False
    while not found:
        generation = gen_next_generation(generation)
        num_generations += 1

        for i in generation:
            print i

        print gen_status(generation, num_generations)

        if TARGET_PHRASE in generation:
            found = True

    print "Target Found"

# ---- Testing Section -----

# print fitness("test", "tart")
# print fitness("test", "Farm")
# print fitness("a", "b") # this should be .98936
# print fitness(chr(32), chr(126)) # this should be 0.0 0% the same
# print fitness("test", "test") # this should be 1.0 100% the same
# print fitness("t", "t") # this should be 1.0 100% the same


#for i in xrange(10):
#   print gen_rand_org(10)

#for i in xrange(10,15):
#   print gen_seed_generation(i)

# ---- Execute the program ----

run_genetic_word_finder()
