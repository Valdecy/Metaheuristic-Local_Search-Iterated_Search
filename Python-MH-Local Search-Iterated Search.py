############################################################################

# Created by: Prof. Valdecy Pereira, D.Sc.
# UFF - Universidade Federal Fluminense (Brazil)
# email:  valdecy.pereira@gmail.com
# Course: Metaheuristics
# Lesson: Iterated Search

# Citation: 
# PEREIRA, V. (2018). Project: Metaheuristic-Local_Search-Iterated_Search, File: Python-MH-Local Search-Iterated Search.py, GitHub repository: <https://github.com/Valdecy/Metaheuristic-Local_Search-Iterated_Search>

############################################################################

# Required Libraries
import pandas as pd
import random
import math
import copy

# Function: Distance
def distance_calc(Xdata, route):
    distance = 0
    for k in range(0, len(route[0])-1):
        m = k + 1
        distance = distance + Xdata.iloc[route[0][k]-1, route[0][m]-1]            
    return distance

# Function: Stochastic 2_opt
def stochastic_2_opt(Xdata, city_tour):
    best_route = copy.deepcopy(city_tour)      
    i, j  = random.sample(range(0, len(city_tour[0])-1), 2)
    if (i > j):
        i, j = j, i
    best_route[0][i:j+1] = list(reversed(best_route[0][i:j+1]))           
    best_route[0][-1]  = best_route[0][0]              
    best_route[1] = distance_calc(Xdata, route = best_route)                     
    return best_route

# Function: Local Search
def local_search(Xdata, city_tour, max_attempts = 50):
    count = 0
    solution = copy.deepcopy(city_tour) 
    while (count < max_attempts):
        candidate = stochastic_2_opt(Xdata, city_tour = solution)      
        if candidate[1] < solution[1]:
            solution  = copy.deepcopy(candidate)
            count = 0
        else:
            count = count + 1                             
    return solution 

# Function: Double Bridge
def double_bridge_4_opt(Xdata, city_tour):
    point_1 =           1 + random.randint(0, math.floor(len(city_tour[0]) / 4))
    point_2 = point_1 + 1 + random.randint(0, math.floor(len(city_tour[0]) / 4))
    point_3 = point_2 + 1 + random.randint(0, math.floor(len(city_tour[0]) / 4))
   
    segment_1 = city_tour[0][0:point_1] + city_tour[0][point_3:len(city_tour[0])-1]
    segment_2 = city_tour[0][point_2:point_3] + city_tour[0][point_1:point_2]   
    city_tour[0] = segment_1 + segment_2 + [segment_1[0]]
    city_tour[1] = distance_calc(Xdata, city_tour)
    return city_tour

# Function: Iterated Search
def iterated_search(Xdata, city_tour, max_attempts = 20, iterations = 50):
    count = 0
    solution = copy.deepcopy(city_tour)
    best_solution = [[],float("inf")]
    while (count < iterations):
        solution = double_bridge_4_opt(Xdata, solution)
        solution = local_search(Xdata, city_tour = solution, max_attempts = max_attempts)
        if (solution[1] < best_solution[1]):
            best_solution = copy.deepcopy(solution) 
        count = count + 1
        if (count > 0):
            print("Iteration = ", count, "->", best_solution)
    return best_solution

######################## Part 1 - Usage ####################################

X = pd.read_csv('Python-MH-Local Search-Iterated Search-Dataset-01.txt', sep = '\t') #17 cities = 2085

cities = [[   1,  2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,   1   ], 4722]
lsis = iterated_search(X, city_tour = cities, max_attempts = 25, iterations = 1000)
