import math
import random
import numpy
import matplotlib.pyplot
 
def cost_calculate(x, function_choice):
    if function_choice == 1:
        return -(x[1]+47)*math.sin(math.sqrt(math.fabs(x[1]+x[0]/2+47)))-x[0]*math.sin(math.sqrt(math.fabs(x[0]-(x[1]+47))))
    else:
        return -abs(math.sin(x[0]) * math.cos(x[1]) * math.exp(abs(1 - ((x[0]**2 + x[1]**2)**(1/2))/math.pi)))
 
def differential_evolution(population_size, boundary_conditions, iter, K, F, cr, function_choice):
    bounds_diff = boundary_conditions[:, 1] - boundary_conditions[:, 0]
    population = boundary_conditions[:, 0] + (numpy.random.rand(population_size, len(boundary_conditions)) * bounds_diff)
    cost = [cost_calculate(candidate, function_choice) for candidate in population]

    best_vector = population[numpy.argmin(cost)]
    best_cost = min(cost)
    prev_cost = best_cost
    generation_best_cost = list()
    generation_avg_cost = list()
    for i in range(iter):
        for j in range(population_size):
            candidates = [candidate for candidate in range(population_size) if candidate != j]
            x, x_r1, x_r2, x_r3 = population[numpy.random.choice(candidates, 4, replace=False)]

            # mutation
            mutant_vector = x + K * (x_r1 - x) + F * (x_r2 - x_r3)
            mutant_vector = [numpy.clip(mutant_vector[i], boundary_conditions[i, 0], boundary_conditions[i, 1]) for i in range(len(boundary_conditions))]

            # crossover
            random_crossover_point = numpy.random.rand(len(boundary_conditions))
            trial_vector = [mutant_vector[i] if random_crossover_point[i] < cr else population[j][i] for i in range(len(boundary_conditions))]
            
            target_vector_cost = cost_calculate(population[j], function_choice)
            trial_vector_cost = cost_calculate(trial_vector, function_choice)
            # selection
            if trial_vector_cost < target_vector_cost:
                population[j] = trial_vector
                cost[j] = trial_vector_cost
        best_cost = min(cost)
        avg_cost = sum(cost) / len(cost)
        generation_best_cost.append(best_cost)
        generation_avg_cost.append(avg_cost)
        if best_cost < prev_cost:
            best_vector = population[numpy.argmin(cost)]
            prev_cost = best_cost
    return [best_vector, best_cost, generation_best_cost, generation_avg_cost]
 
function_choice = int(input("Enter the name of desired function: egg holder(1) or holder table(2): "))

# population size
pop_size = 20

# boundary conditions
if function_choice == 1:
    boundary_conditions = numpy.asarray([(-512, 512), (-512, 512)])
else:
    boundary_conditions = numpy.asarray([(-10, 10), (-10, 10)])

# define number of iterations
generation_count = 50

# hyper parameters
K = 0.5
F = random.uniform(-2, 2)
cr = 0.8
 
result_arr = differential_evolution(pop_size, boundary_conditions, generation_count, F, K, cr, function_choice)
print("Solution:")
print(result_arr[0])
print("Cost of the solution: %f" % result_arr[1])
 
matplotlib.pyplot.plot(result_arr[2], '.-')
matplotlib.pyplot.legend(["minimum cost and avg cost"])
matplotlib.pyplot.plot(result_arr[3], '.-')
matplotlib.pyplot.xlabel("Iteration")
matplotlib.pyplot.ylabel("Cost")
matplotlib.pyplot.show()