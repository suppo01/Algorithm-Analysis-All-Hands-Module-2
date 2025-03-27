"""Run an NSGA-II Algorithm using a binary tournament method."""

import json
import numpy as np
from pymoo.operators.selection.tournament import TournamentSelection
from pymoo.core.population import Population
from pymoo.core.individual import Individual

# P is the permutations of things to be compared between competitors
def binary_tournament(pop, P, **kwargs):
    """Run a series of binary tournaments to determine the best fit individual(s)."""
    # The P input defines the tournaments and competitors
    n_tournaments, n_competitors = P.shape

    if n_competitors != 2:
        raise Exception("Only pressure=2 allowed for binary tournament!")

    # the result this function returns
    S = np.full(n_tournaments, -1, dtype=int)

    # define lists to keep track of test names
    winner_list = []
    loser_list = []

    # now do all the tournaments
    for i in range(n_tournaments):
        a, b = P[i]

        # if the first individual is better, choose it
        if pop[a].F < pop[b].F:
            S[i] = a
            loser = pop[b].name
            winner = pop[a].name
        # otherwise take the other individual
        else:
            S[i] = b
            loser = pop[a].name
            winner = pop[b].name
   
        # update lists with name records
        if winner not in winner_list:
            if winner not in loser_list:
                winner_list.append(winner)
            else:
                winner_list.remove(loser)
        if loser not in loser_list:
            loser_list.append(loser)

    # return the names of the ideal tests
    print(f"\nThe Ideal Tests Are: {winner_list}\n")
    return S

def main():
    """Performs an experiment for a multi objective sorting algorithm."""
    with open('data/nsga.json', 'r') as json_data:
        data = json.load(json_data)
    data_array = np.array(data["data"])

    # Create an empty Individuals List
    individuals = []

    # Populate the List with individuals using the 2D array
    for row in data_array:
        ind = Individual(X=[row[1], row[2]])  # Set decision variables (X)
        ind.name = row[0]
        individuals.append(ind)

    # Set fitness values
    for ind in individuals:
        ind.F = float(ind.X[1]) / float(ind.X[0])  # Assign fitness values as the sum of X

    # Create a population object with the individuals
    pop = Population(individuals)

    # Generation of Pairing Array
    a = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32,
        33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63,
        64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91]
    res = []

    for i in range(len(a)):
        for j in range(i + 1, len(a)):
            res.append([a[i], a[j]])

    # Pairing Array
    P = np.array(res)

    # run the binary tournament selection
    selection = TournamentSelection(func_comp=binary_tournament)
    selected = selection.do(P, pop, n_select=1, n_parents=2)


if __name__ == "__main__":
   main()
