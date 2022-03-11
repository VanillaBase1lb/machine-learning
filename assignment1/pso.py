import random
import numpy
from random import SystemRandom
import matplotlib.pyplot

class Generation(object):
    def __init__(self, pbest, fbest, gbest):
        self.pbest = pbest
        self.fbest = fbest
        self.gbest = gbest

class limits(object):
    def __init__(self, x_min, x_max, y_min, y_max):
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max

def eggholder(Parameter):
    x=Parameter[0]
    y=Parameter[1]
    return -(y+47)*numpy.sin(numpy.sqrt(abs(x/2 + (y+47)))) - x*numpy.sin(numpy.sqrt(abs(x-(y+47))))

def holdertable(Parameter):
    x=Parameter[0]
    y=Parameter[1]
    return -abs(numpy.sin(x)*numpy.cos(y)*numpy.exp(abs(1-(numpy.sqrt(x**2+y**2)/numpy.pi))))


population_size = [20, 50, 100, 200]
num_of_gens = [50, 100, 200]
egg_limits = limits(-512, 512, -512, 512)
holder_limits = limits(-10, 10,-10, 10)
c1 = 2
c2 = 2
egg_max_vel = numpy.array([100,100])
holder_max_vel = numpy.array([2,2])
graph_store = {}

def graph(particle, pbest, gbest, pop_size, gen, func):
    fig = matplotlib.pyplot.figure()

    x1 = [particle[i][0] for i in range(0,pop_size)]
    y1 = [particle[i][1] for i in range(0,pop_size)]
    x2 = [gbest[0] for i in range(0,pop_size)]
    y2 = [gbest[1] for i in range(0,pop_size)]

    print("x1",x1,"y1",y1)
    print("\n")
    print("x2",x2,"y2",y2)
    matplotlib.pyplot.scatter(x1,y1)
    matplotlib.pyplot.scatter(x2,y2,c="red",s=800)
    title = "Function: " + func + ", Population: " + str(pop_size) + ", Generation: " + str(gen)
    matplotlib.pyplot.title(title)
    matplotlib.pyplot.show()


def constraints(z, limits):
    for particle in z:
        x = particle[0]
        y = particle[1]
        if limits.x_min <= x <= limits.x_max and limits.y_min <= y <= limits.y_max:
            continue
        else:
            return False
    return True

def initialize_candidates(n, limits):
    position_vectors = []
    for i in range(0,n):
        Random_X = SystemRandom().uniform(limits.x_min, limits.x_max)
        Random_Y = SystemRandom().uniform(limits.y_min, limits.y_max)
        position_vectors.append(numpy.array([Random_X,Random_Y]))
    return position_vectors

def initialize(population_size, limits):
    particles=initialize_candidates(population_size, limits)
    if(constraints(particles, limits) and c1+c2==4):
        return particles
    else:
        initialize(population_size, limits)

def fitness(function,particles,pop_size):
    return [function(particles[i]) for i in range(0, pop_size)]

def new_vel(velocity,particles,pop_size,gen,pbest,gbest, max_vel):
    r1=random.random()
    r2=random.random()
    for i in range(0, pop_size):
        velocity[i] = velocity[i] + c1*r1*(pbest[i] - particles[i]) + c2*r2*(gbest-particles[i])
    for i in range(0, pop_size):
        if velocity[i].any() > max_vel.any():
            new_vel(velocity,particles,pop_size,gen,pbest,gbest, max_vel)

def generate_position(particles, velocity, i):
       particles[i]=particles[i]+velocity[i]

def new_pos(velocity,particles,pop_size,gen,limits):
    old_positions = [x for x in particles]
    for i in range(0,pop_size):
        if limits.x_min <= particles[i][0] <= limits.x_max and limits.y_min <= particles[i][1] <= limits.y_max:
            continue
        else:
            new_pos(velocity,particles,pop_size,gen,limits)
        generate_position(particles, velocity, i)

def PSO(function, limits, pop_size, gens_count, velocity, particles, pbest, gbest, fbest, max_vel):
    new_vel(velocity,particles,pop_size,gens_count,pbest,gbest, max_vel)
    
    new_pos(velocity,particles,pop_size,gens_count,limits)

    current_fitness=fitness(function,particles,pop_size)

    for i in range(0,pop_size):
        if(current_fitness[i]<fbest[i]):
            fbest[i]=current_fitness[i]
            pbest[i]=particles[i]

    for i in range(0,pop_size):
        if(fbest[i]==min(fbest)):
            gbest=pbest[i]
            break
    return pbest,gbest,fbest

if __name__ == "__main__":
    function_choice = int(input("Enter the name of desired function: egg holder(1) or holder table(2): "))
    if function_choice==1:
        func = {'function': eggholder, 'limits': egg_limits, 'max_vel': egg_max_vel}
    else:
        func = {'function': holdertable, 'limits': holder_limits, 'max_vel': holder_max_vel}
    print('\nFunction: ', func['function'].__name__, '\n')
    for pop_size in population_size:
        print('\nPopulation size:', pop_size)
        velocity=[[0,0]]*pop_size
        particles = initialize(pop_size, func['limits'])

        pbest=particles
        fbest = fitness(func['function'], pbest, pop_size)

        for i in range(0, pop_size):
            if(fbest[i]==min(fbest)):
                gbest=pbest[i]
                break

        for gen in range(1, 201):
            pbest, gbest, fbest = PSO(func['function'], func['limits'], pop_size, gen, velocity, particles, pbest, gbest, fbest, func['max_vel'])

            if gen in num_of_gens:
                print('\n   Generations: ', gen)
                print('   Optimum: ', gbest)
                graph(particles, pbest,gbest,pop_size, gen, func['function'].__name__)