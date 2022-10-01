import random
import numpy as np
import math
#import pandas
#number of cities
numCities = 5

routeLength = 18

#population to be produced (number of possible solutions)
population_Size = 40

#cites represented as bits
#city A: 000
#city B: 001
#city C: 010
#city E: 011
#city D: 100
genes = ["000","001","010","011","100"]

class chromosome:
    def __init__(self) -> None:
        self.route = [] 
        self.fitness = 0


#population creation
def createRoute():
    route = ["000"]
    while True:
        #route of 5 cities reached
        if len(route) == numCities:
            route.append("000")
            return route
        else:
            #get random city and append it to the existing route, if it isnt already
            cityIndex = random.randint(0,4)
            city = genes[cityIndex]
            if not city in route:
                route.append(city)
        

   





#Fitness calculation for each solution, i.e. the total cost of the route.
def fitnessCalculation(route,costMatrix):
    fitness = 0
    #calculate costs from city i to city i+1 to calculate the total cost of the route, 
    for i in range(len(route)-1):
        cityIndex1 = int(route[i],2)
        cityIndex2 = int(route[i+1],2)
        fitness += costMatrix[cityIndex1][cityIndex2]

    return 1/fitness





#Roulette selection implementation
def rouletteSelection(population):
    #calculate probabilities
    sum = 0
    fitness = [None] * len(population)
    for i in range(population_Size):
        fitness[i] = fitnessCalculation(population[i].route,costMatrix)
        
        sum += fitness[i]

    S = random.uniform(0,sum)
    i=0
    K=0
    while True:
        if fitness[i] + K > S:
            return population[i]
        else:
            K+= fitness[i]
            i+=1

        
    
    
   



#check for illegal routes
def checkCities(child,city):
    if city not in child.route:
        return True
    return False


#function to produce legal routes with no repetitive cites
def produce(child,parent,index):
    if checkCities(child,parent.route[3]):
        child.route[index] = parent.route[3]
        return child
    elif checkCities(child,parent.route[4]):
        child.route[index] = parent.route[4]
        return child
    elif checkCities(child,parent.route[1]):
        child.route[index] = parent.route[1]
        return child
    else:
        for city in genes:
            if city not in child.route:
                child.route[index] = city
                return child





#breed population function
def breed(firstparent,secondparent,costMatrix): 
    #choose two parents according to the roulette wheel
    child = chromosome()
    #perform crossover
    child.route = ["000","",firstparent.route[2],"","","000"]
    #produce  child
    produce(child,secondparent,3)
    produce(child,secondparent,4)
    produce(child,secondparent,1)
    child.fitness = fitnessCalculation(child.route,costMatrix)
    return child







#mutate percentage of population function
#Mutation causes two cities inside the route to be swapped to form a new route
def mutate(route):
    while True:
        #swap the two cities in the route if they are different to produce a legal route
        print("Before mutation:",route)
        firstCity = random.randint(0,4)
        secondCity = random.randint(0,4)
        if (firstCity != secondCity and firstCity !=0  and secondCity !=0):
            temp = route[firstCity]
            route[firstCity] = route[secondCity]
            route[secondCity] = temp
            print("After mutation:",route)
            break
    return route




#solution to TSP problem
def TspSolution(costMatrix):
    print("TSP")
    #create population of 40
    population = []
    for i in range(population_Size):
        solution = chromosome()
        solution.route = createRoute()
        solution.fitness = fitnessCalculation(solution.route,costMatrix)
        population.append(solution)
        
    print("CREATED FIRST POPULATION!")
    
    print("\nInitial population: \nGNOME     FITNESS VALUE\n")
    for i in range(population_Size):
         print(population[i].route, population[i].fitness)
    print()


    newPopulation = [None]*population_Size
    #start of generations
    #25 generations
    for i in range(50):
        #select fittest parents
        children = [] 
        fittest = []
        for pop in population:
            fittest.append(pop.fitness)

        indexes = np.argsort(fittest)
        fittest = []
        indexes = indexes[::-1]
        r = 0
        while (r < population_Size/2):

            fittest.append(population[indexes[r]])
            r+=1

        #perform breeding
        for j in range(10):
            firstParent = rouletteSelection(population)
            while True:
                secondParent = rouletteSelection(population)
                if not(np.array_equal(firstParent,secondParent)):
                    break
            #breeding
            firstChild = chromosome()
            secondChild = chromosome() 
            #produce children based on selected parents  
            firstChild = breed(firstParent,secondParent,costMatrix)
            secondChild = breed(secondParent,firstParent,costMatrix)
            #append children to list
            children.append(firstChild)
            children.append(secondChild)
        
          
        #create new population
        population = fittest + children
        #perform mutation on 10%
        m = 0
        while m < 10/100*population_Size:
            index = random.randint(0,population_Size-1)
            population[index].route = mutate(population[index].route)
            m+=1
        

        print("GENERATION NUMBER:",i)
        print("\nFinal population: \nGNOME     FITNESS VALUE\n")
        for i in range(population_Size):
            print(population[i].route, 1/population[i].fitness)
        print()

    
    bestRoute = max(population, key = lambda pop: pop.fitness)
    print("Route with minimum cost is:",bestRoute.route," with cost ", 1/bestRoute.fitness)

    
    return True



if __name__ == "__main__":
    costMatrix = [
        [0, 4, 4, 3, 7], #routes from city A to others
        [4, 0, 2, 5 ,3], #routes from city B to others
        [4, 2, 0, 3, 2], #routes from city C to others
        [4, 5 ,3, 0, 6], #routes from city D to others
        [7, 3, 2, 6, 0], #routes from city E to others
    ]
    TspSolution(costMatrix)
 
