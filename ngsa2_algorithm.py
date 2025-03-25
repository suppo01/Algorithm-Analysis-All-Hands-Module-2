import numpy as np
from pymoo.algorithms.soo.nonconvex.ga import GA
from pymoo.operators.selection.tournament import TournamentSelection
from pymoo.optimize import minimize
from pymoo.algorithms.moo.nsga2 import binary_tournament
from data import simplified_test_metrics

# P is the permutations of things to be compared between competitors
"""
def binary_tournament(pop, P, _, **kwargs):
    # The P input defines the tournaments and competitors
    n_tournaments, n_competitors = P.shape

    if n_competitors != 2:
        raise Exception("Only pressure=2 allowed for binary tournament!")

    # the result this function returns
    S = np.full(n_tournaments, -1, dtype=np.int)

    # now do all the tournaments
    for i in range(n_tournaments):
        a, b = P[i]

        # if the first individual is better, choose it
        if pop[a].F < pop[b].F:
            S[i] = a

        # otherwise take the other individual
        else:
            S[i] = b

    return S
"""

selection = TournamentSelection(pressure=2, func_comp=binary_tournament)
problem = np.array(dict[simplified_test_metrics])
algorithm = GA(pop_size=len(problem), eliminate_duplicates=True)
res = minimize(problem, algorithm, termination=('n_gen', (2.5 * pow(10, 164))), verbose=False)
print(res)
