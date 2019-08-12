# Metaheuristic-Local_Search-Iterated_Search
Iterated Search Function for TSP problems. The function returns: 1) A list with the order of the cities to visit, and the total distance for visiting this same list order.

* X = Distance Matrix.

* buid_distance_matrix (HELPER FUNCTION) = Tranforms coordinates in a distance matrix (euclidean distance).

* city_tour = Initial list of visitation.

* seed (HELPER FUNCTION) = Generates a random list of visitation.

* iterations = Total number of iterations. The Default Value is 50.

* max_attempts = Number of attempts to improve solution. The Default Value is 20.

* plot_tour_distance_matrix (HELPER FUNCTION) = A projection is generated based on the distance matrix. The estimated projection may present a plot with path crosses, even for the 2-opt optimal solution (Red Point = Initial city; Orange Point = Second City).

* plot_tour_coordinates (HELPER FUNCTION) = Plots the 2-opt optimal solution (Red Point = Initial city; Orange Point = Second City).
