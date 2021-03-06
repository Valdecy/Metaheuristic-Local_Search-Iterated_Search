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
import numpy  as np
import math
import copy
from matplotlib import pyplot as plt 

# Function: Tour Distance
def distance_calc(Xdata, city_tour):
    distance = 0
    for k in range(0, len(city_tour[0])-1):
        m = k + 1
        distance = distance + Xdata[city_tour[0][k]-1, city_tour[0][m]-1]            
    return distance

# Function: Euclidean Distance 
def euclidean_distance(x, y):       
    distance = 0
    for j in range(0, len(x)):
        distance = (x[j] - y[j])**2 + distance   
    return distance**(1/2) 

# Function: Initial Seed
def seed_function(Xdata):
    seed = [[],float("inf")]
    sequence = random.sample(list(range(1,Xdata.shape[0]+1)), Xdata.shape[0])
    sequence.append(sequence[0])
    seed[0] = sequence
    seed[1] = distance_calc(Xdata, seed)
    return seed

# Function: Build Distance Matrix
def build_distance_matrix(coordinates):
   a = coordinates
   b = a.reshape(np.prod(a.shape[:-1]), 1, a.shape[-1])
   return np.sqrt(np.einsum('ijk,ijk->ij',  b - a,  b - a)).squeeze()

# Function: Tour Plot
def plot_tour_distance_matrix (Xdata, city_tour):
    m = np.copy(Xdata)
    for i in range(0, Xdata.shape[0]):
        for j in range(0, Xdata.shape[1]):
            m[i,j] = (1/2)*(Xdata[0,j]**2 + Xdata[i,0]**2 - Xdata[i,j]**2)    
    w, u = np.linalg.eig(np.matmul(m.T, m))
    s = (np.diag(np.sort(w)[::-1]))**(1/2) 
    coordinates = np.matmul(u, s**(1/2))
    coordinates = coordinates.real[:,0:2]
    xy = np.zeros((len(city_tour[0]), 2))
    for i in range(0, len(city_tour[0])):
        if (i < len(city_tour[0])):
            xy[i, 0] = coordinates[city_tour[0][i]-1, 0]
            xy[i, 1] = coordinates[city_tour[0][i]-1, 1]
        else:
            xy[i, 0] = coordinates[city_tour[0][0]-1, 0]
            xy[i, 1] = coordinates[city_tour[0][0]-1, 1]
    plt.plot(xy[:,0], xy[:,1], marker = 's', alpha = 1, markersize = 7, color = 'black')
    plt.plot(xy[0,0], xy[0,1], marker = 's', alpha = 1, markersize = 7, color = 'red')
    plt.plot(xy[1,0], xy[1,1], marker = 's', alpha = 1, markersize = 7, color = 'orange')
    return

# Function: Tour Plot
def plot_tour_coordinates (coordinates, city_tour):
    xy = np.zeros((len(city_tour[0]), 2))
    for i in range(0, len(city_tour[0])):
        if (i < len(city_tour[0])):
            xy[i, 0] = coordinates[city_tour[0][i]-1, 0]
            xy[i, 1] = coordinates[city_tour[0][i]-1, 1]
        else:
            xy[i, 0] = coordinates[city_tour[0][0]-1, 0]
            xy[i, 1] = coordinates[city_tour[0][0]-1, 1]
    plt.plot(xy[:,0], xy[:,1], marker = 's', alpha = 1, markersize = 7, color = 'black')
    plt.plot(xy[0,0], xy[0,1], marker = 's', alpha = 1, markersize = 7, color = 'red')
    plt.plot(xy[1,0], xy[1,1], marker = 's', alpha = 1, markersize = 7, color = 'orange')
    return

# Function: Stochastic 2_opt
def stochastic_2_opt(Xdata, city_tour):
    best_route = copy.deepcopy(city_tour)      
    i, j  = random.sample(range(0, len(city_tour[0])-1), 2)
    if (i > j):
        i, j = j, i
    best_route[0][i:j+1] = list(reversed(best_route[0][i:j+1]))           
    best_route[0][-1]  = best_route[0][0]              
    best_route[1] = distance_calc(Xdata, best_route)                     
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
        print("Iteration = ", count, " Distance = ", best_solution[1])
    return best_solution

######################## Part 1 - Usage ####################################

# Load File - A Distance Matrix (17 cities,  optimal = 1922.33)
X = pd.read_csv('Python-MH-Local Search-Iterated Search-Dataset-01.txt', sep = '\t') 
X = X.values

# Start a Random Seed
seed = seed_function(X)

# Call the Function
lsis = iterated_search(X, city_tour = seed, max_attempts = 25, iterations = 1000)

# Plot Solution. Red Point = Initial city; Orange Point = Second City # The generated coordinates (2D projection) are aproximated, depending on the data, the optimum tour may present crosses
plot_tour_distance_matrix(X, lsis)

######################## Part 2 - Usage ####################################

# Load File - Coordinates (Berlin 52,  optimal = 7544.37)
Y = pd.read_csv('Python-MH-Local Search-Iterated Search-Dataset-02.txt', sep = '\t') 
Y = Y.values

# Build the Distance Matrix
X = build_distance_matrix(Y)

# Start a Random Seed
seed = seed_function(X)

# Call the Function
lsis = iterated_search(X, city_tour = seed, max_attempts = 50, iterations = 5000)

# Plot Solution. Red Point = Initial city; Orange Point = Second City
plot_tour_coordinates(Y, lsis)
