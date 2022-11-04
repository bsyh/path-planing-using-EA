import random
import environment

class Path:
    '''
    individual of solution
    '''

    def __init__(self):
        self.path = []
        self.fitness = 0

    def __init__(self, init_length):
        self.path = []
        self.fitness = 0

        for i in range(init_length):
            direction = random.randint(0,3)
            self.path.append(direction)



    def setPath(self, new_path):
        self.path = new_path

    def getPath(self):
        return self.path

    def appendMutation(self,lower=1, upper=5):
        '''
        randomly append moves at random index with random step size in the range of (lower, upper)
        :param lower: lower bound of step size
        :param upper: upper lower of step size
        :return:
        '''
        if len(self.path)==0:
            index_insert = 0
        else:
            index_insert = random.randint(0, len(self.path))
        direction = random.randint(0,3)

        for i in range(random.randint(lower,upper)):
            self.path.insert(index_insert, direction)

    def deleteMutation(self):
        '''
        randomly delete a move at random index
        :return:
        '''
        if len(self.path)==0:
            return
        else:
            index_pop = random.randint(0, len(self.path)-1)
        self.path.pop(index_pop)

    def updateFitness(self, start_state, destination_state, maze):
        '''
        update the fitness of this individual
        :param start_state: start position
        :param destination_state: destination position
        :param maze: grid world
        :return:
        '''
        self.removeRedundancy(start_state, destination_state, maze)

        current_position = start_state
        for step in range(len(self.path)):
            current_position = environment.move(current_position,maze,self.path[step])

        self.fitness = environment.get_reward(current_position, destination_state)

    def getFitness(self):
        return self.fitness

    def removeRedundancy(self,start_state,destination_state,maze):
        '''
        this function remove illegal moves.
        if hitting a wall, the move is illegal.

        :param start_state: start position
        :param destination_state:  destination position
        :param maze: grid world
        :return:
        '''
        current_position = start_state
        path_length = len(self.path)
        step = 0
        while step < path_length:
            next_position = environment.move(current_position, maze, self.path[step])
            if current_position == next_position:
                path_length -= 1
                self.path.pop(step)
            if destination_state == current_position:
                self.path = self.path[:step]
                return
            step += 1

    def removeloop(self,start_state,maze):
        '''
        remove loops in path, such as [0,1,2,3] is a loop
        :param start_state: start position
        :param maze:grid world
        :return:
        '''

        position_1 = start_state
        pointer_1 = 0
        while pointer_1 < len(self.path):
            # position_1 points to a location
            pointer_2 = pointer_1
            position_2 = environment.move(position_1, maze, self.path[pointer_2])
            position_copy = position_1

            while pointer_2 < len(self.path)-1:
                # keep going
                if position_1==position_2:
                    # if position_2 goes to position_1, we consider there is a loop
                    # remove the loop
                    self.path = self.path[:pointer_1] + self.path[pointer_2+1:]
                    break
                pointer_2 += 1
                position_2 = environment.move(position_2, maze, self.path[pointer_2])

            else:
                pointer_1 += 1
            # position_1 moves next
            position_1 = position_copy





def onePointCrossover(parent_1, parent_2, max_distance=4, length_limit=100):
    '''

    :param parent_1: individual 1
    :param parent_2: individual 1
    :param max_distance:  the distance between the crossover points on two individuals
    :param length_limit: the maximum length of path
    :return:
    '''

    # get length of parents
    length_1 = len(parent_1)
    length_2 = len(parent_2)
    shorter_length = min(length_1,length_2)


    if random.randint(0,1):
        # 0.5 of probability the distance is positive
        distance = random.randint(0,max_distance)
    else:
        # 0.5 of probability the distance is positive
        distance = -1 * random.randint(0,max_distance)

    # the crossover point of parent 1
    point_1 = random.randint(0, shorter_length)
    # the crossover point of parent 2
    point_2 = point_1 + distance
    point_2 = max(min(length_2,point_2),0)

    # get segments of parents cut by the crossover point
    segmentation_1_1 = parent_1[:point_1]
    segmentation_1_2 = parent_1[point_1:]

    segmentation_2_1 = parent_2[:point_2]
    segmentation_2_2 = parent_2[point_2:]

    offspring_1 = segmentation_1_1+segmentation_2_2
    offspring_2 = segmentation_2_1+segmentation_1_2

    # recombine to get new offspring, with maximum length limit length_limit
    offspring_1 = offspring_1[:length_limit]
    offspring_2 = offspring_2[:length_limit]

    return offspring_1, offspring_2

def getFitness_list(population):
    '''
    calculate the fitness of population
    :param population: the list of individuals
    :return: a list of fitness in order
    '''
    fitness_list = []
    for individual in population:
        fitness_list.append(individual.getFitness())
    return fitness_list