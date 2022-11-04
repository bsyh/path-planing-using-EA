import evo_algo
import environment
import random
import numpy as np

def main():
    # random.seed(0)

    # read map
    maze = np.load('map_table.npy')
    maze = maze.tolist()
    for i in range(len(maze)):
        for j in range(len(maze[i])):
            maze[i][j] = int(maze[i][j])

    # read start and destination position
    start_state = np.load('start_state.npy')
    start_state = start_state.tolist()
    destination_state = np.load('destination_state.npy')
    destination_state = destination_state.tolist()



    dimension = [len(maze),len(maze[0])]

    # if reach iteration upper limit, EA terminates
    max_generation = 20000
    #tournament size
    nts = 4
    path_length_limit = dimension[0]*dimension[1]+1

    #append-mutation step size upper limit
    step_size_bound = 30

    #population size
    population_size = 500
    # initialzed length of solution path
    initial_length = 5

    population = [evo_algo.Path(initial_length) for i in range(population_size)]

    index_list = range(0, population_size)


    [population[0].appendMutation() for i in range(10)]
    # environment.display(maze)

    generation_count = 0
    max_fitness = 0
    while generation_count < max_generation and max_fitness<999:
        # max_fitness<999 will let EA terminates when a path is found for the first time
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

        # probability of 0.66 will hold tournament selection
        # probability of 0.66 will hold uniform-random selection
        if random.randint(0,6)>=2:
            # get winner and loser individual index
            random_tournament_1 = False
            tournament_1_winner_index = tournament_1_index[tournament_1_fitness.index(max(tournament_1_fitness))]
            tournament_1_loser_index = tournament_1_index[tournament_1_fitness.index(min(tournament_1_fitness))]
        else:
            random_tournament_1 = True
            tournament_1_winner_index = tournament_1_index[random.randint(0, nts-1)]
            tournament_1_loser_index = tournament_1_index[random.randint(0,nts-1)]

        # probability of 0.66 will hold tournament selection
        # probability of 0.66 will hold uniform-random selection
        if random.randint(0,6)>=2:
            # get winner and loser individual index
            random_tournament_2 = False
            tournament_2_winner_index = tournament_2_index[tournament_1_fitness.index(max(tournament_1_fitness))]
            tournament_2_loser_index = tournament_2_index[tournament_2_fitness.index(min(tournament_2_fitness))]
        else:
            random_tournament_2 = True
            tournament_2_winner_index = tournament_2_index[random.randint(0,nts-1)]
            tournament_2_loser_index = tournament_2_index[random.randint(0,nts-1)]

        # copy two parents' genotype
        offspring_1_path = population[tournament_1_winner_index].getPath()
        offspring_2_path = population[tournament_2_winner_index].getPath()

        # 0.8 of probability a crossover happens
        if random.randint(1, 10) <= 8:

            offspring_1_path, offspring_2_path = evo_algo.onePointCrossover(
                offspring_1_path, offspring_2_path, length_limit=path_length_limit)

            population[tournament_1_loser_index].setPath(offspring_1_path)
            population[tournament_2_loser_index].setPath(offspring_2_path)



            # 0.5 of probability a append-mutation happens to offspring_1
            # 0.5 of probability a delete-mutation happens to offspring_1
            if random.randint(1, 2) == 1:
                population[tournament_1_loser_index].deleteMutation()
            else:
                population[tournament_1_loser_index].appendMutation(1,step_size_bound)
                if random_tournament_1:
                    for i in range(5):
                        population[tournament_1_loser_index].appendMutation(1, step_size_bound)

            # 0.5 of probability a append-mutation happens to offspring_2
            # 0.5 of probability a delete-mutation happens to offspring_2
            if random.randint(1, 2) == 1:
                population[tournament_2_loser_index].deleteMutation()
            else:
                population[tournament_2_loser_index].appendMutation(1,step_size_bound)
                if random_tournament_2:
                    for i in range(5):
                        population[tournament_2_loser_index].appendMutation(1, step_size_bound)


            population[tournament_1_loser_index].updateFitness(start_state, destination_state, maze)
            population[tournament_2_loser_index].updateFitness(start_state, destination_state, maze)

        max_fitness = max(fitness_list)

    fitness_list = evo_algo.getFitness_list(population)
    max_fitness = max(fitness_list)
    best_individual_index_list = [i for i, x in enumerate(fitness_list) if x == max_fitness]

    best_individual_length_list = [len(population[index].getPath()) for index in best_individual_index_list]
    min_length_index = best_individual_length_list.index(min(best_individual_length_list))
    best_shortest_individual = population[best_individual_index_list[min_length_index]]


    print("Path found with length:", len(best_shortest_individual.path),'\n',best_shortest_individual.path)
    environment.display_path(best_shortest_individual.path, maze, start_state, destination_state)
    return best_shortest_individual, max_fitness


if __name__ == "__main__":
    main()
