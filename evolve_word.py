import random

# ---- Constants/Control Variables ----

SIZE_OF_GENERATION = 20 # number of organisms per generation
MIN_CHAR = 32 # ' '
MAX_CHAR = 126 # '~'
CHAR_RANGE = MAX_CHAR - MIN_CHAR

# ---- Functions -----

# Calculate the fitness of a certain string (the organism) from the target string
def fitness(organism, target):
	fitness = 0 # fitness of the word
	
	# in this version of the algorithm the current organism and target must be same length
	# this could be modified by assigning some weight to missing letters
	if len(organism) != len(target): exit(1)

	# Calculate the fitness by character
	for i in xrange(len(organism)):
		char_fitness = 1.0 - (abs(float(ord(organism[i]))-float(ord(target[i]))) / float(CHAR_RANGE))
		fitness += char_fitness

	# total fitness for the oganism is the average fitness of each character
	fitness = fitness / float(len(organism))

	return fitness

# Generate the initial (seed) generation
def gen_seed_generation(length):
	generation = [""] * SIZE_OF_GENERATION
	for i in xrange(len(generation)):
		generation[i] = gen_rand_org(length)
	return generation
	
# generate a random organism of length
def gen_rand_org(length):
	# We create an array the length of the target word which will then be
	# modified in order to avoid the overhead of creating a new array/string
	# for every iteration of the loop (which .append() would do)
	organism = [''] * length
	for i in xrange(length):
		organism[i] = chr(random.randint(MIN_CHAR, MAX_CHAR))
	return ''.join(organism)

# return a dictionary of scored organisms
def score_generation(generation, target):
	scored_generation = {}
	for i in generation:
		scored_generation[i] = fitness(i, target)
	return scored_generation

# generate the next generation of the algorithm
def gen_next_generation(generation, target):
	if len(generation) is 0:
		return gen_seed_generation(len(target))
	else:
		# score
		scored_generation = score_generation(generation, target)
		# breed
		return gen_seed_generation(len(target))

# Use a genetic algorithm to generate the target word
def run_genetic_word_finder(target):
	num_generations = 0
	generation = []
	found = False
	while not found:
		generation = gen_next_generation(generation, target)
		num_generations += 1

		# print the current status of the algorithm
		print "\nCurrent generation: " + str(num_generations)
		for i in generation:
			print i

		if target in generation:
			found = True

	print "Target Found"

# ---- Testing Section -----

print fitness("test", "tart")
print fitness("test", "Farm")
print fitness("a", "b") # this should be .98936
print fitness(chr(32), chr(126)) # this should be 0.0 0% the same
print fitness("test", "test") # this should be 1.0 100% the same
print fitness("t", "t") # this should be 1.0 100% the same


#for i in xrange(10):
#	print gen_rand_org(10)

#for i in xrange(10,15):
#	print gen_seed_generation(i)

print run_genetic_word_finder("test")
