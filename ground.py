import evo_algo
import environment
import random

def ground_test():
    # parameter setting

    # dimention of map
    dimension = [7,10]

    # start and destination position
    start_state = [3,0]
    destination_state = [3,7]

    # when generation reach this limit, terminates
    max_generation = 5000
    # tournament size
    nts = 3

    path_length_limit = dimension[0]*dimension[1]+1

    # population size
    population_size = 500

    initial_length = dimension[0]+dimension[1]
    population = [evo_algo.Path(initial_length) for i in range(population_size)]

    index_list = range(0, population_size)

    # generate flat ground map
    maze = environment.generate_grid(dimension[0], dimension[1], 1)

    [population[0].appendMutation() for i in range(10)]
    # environment.display(maze)

    generation_count = 0
    max_fitness = 0
    while generation_count < max_generation:

        generation_count += 1

        # calculate fitness list
        fitness_list = evo_algo.getFitness_list(population)

        # tournaments
        parent_pool_index = random.sample(index_list, k=2 * nts)

        tournament_1_index = parent_pool_index[:nts]
        tournament_2_index = parent_pool_index[nts:]
        tournament_1_fitness = []
        tournament_2_fitness = []
        for i in range(nts):
            tournament_1_fitness.append(fitness_list[tournament_1_index[i]])
            tournament_2_fitness.append(fitness_list[tournament_2_index[i]])

        # get winner and loser individual index
        tournament_1_winner_index = tournament_1_index[tournament_1_fitness.index(max(tournament_1_fitness))]
        tournament_1_loser_index = tournament_1_index[tournament_1_fitness.index(min(tournament_1_fitness))]

        tournament_2_winner_index = tournament_2_index[tournament_2_fitness.index(max(tournament_2_fitness))]
        tournament_2_loser_index = tournament_2_index[tournament_2_fitness.index(min(tournament_2_fitness))]

        # copy two parents' genotype
        offspring_1_path = population[tournament_1_winner_index].getPath()
        offspring_2_path = population[tournament_2_winner_index].getPath()

        # 0.7 of probability a crossover happens
        if random.randint(1, 10) <= 7:

            offspring_1_path, offspring_2_path = evo_algo.onePointCrossover(
                offspring_1_path, offspring_2_path, length_limit=path_length_limit)

            population[tournament_1_loser_index].setPath(offspring_1_path)
            population[tournament_2_loser_index].setPath(offspring_2_path)



            # 0.33 of probability a micro mutation happens to offspring_1
            # 0.66 of probability a macro mutation happens to offspring_1
            if random.randint(1, 3) == 1:
                population[tournament_1_loser_index].deleteMutation()
            else:
                population[tournament_1_loser_index].appendMutation()

            # 0.33 of probability a micro mutation happens to offspring_2
            # 0.66 of probability a macro mutation happens to offspring_2
            if random.randint(1, 3) == 1:
                population[tournament_2_loser_index].deleteMutation()
            else:
                population[tournament_2_loser_index].appendMutation()

            population[tournament_2_loser_index].updateFitness(start_state, destination_state, maze)
            population[tournament_1_loser_index].updateFitness(start_state, destination_state, maze)

            # print(fitness_list)

        max_fitness = max(fitness_list)

    fitness_list = evo_algo.getFitness_list(population)
    max_fitness = max(fitness_list)
    best_individual_index_list = [i for i, x in enumerate(fitness_list) if x == max_fitness]

    best_individual_length_list = [len(population[index].getPath()) for index in best_individual_index_list]
    min_length_index = best_individual_length_list.index(min(best_individual_length_list))
    best_shortest_individual = population[best_individual_index_list[min_length_index]]

    best_shortest_individual.removeloop(start_state,maze)
    print("Path found:",best_shortest_individual.path)
    environment.display_path(best_shortest_individual.path, maze, start_state,destination_state)
    return best_shortest_individual, max_fitness




ground_test()
