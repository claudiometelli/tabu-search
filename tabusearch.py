from typing import List, Tuple
from itertools import combinations

PROCESSING_TIMES = [6, 4, 8, 2, 10, 3] # p_j, j=1,...,6
PENALTIES = [1, 1, 1, 1, 1, 1] # w_j, j=1,...,6
DUE_DATES = [9, 12, 15, 8, 20, 22] # d_j, j=1,...,6
STARTING = [1, 2, 3, 4, 5, 6] # first solution
TABU_TENURE = 3 # length of tabu list (short memory)
ITERATIONS = 10 # iterations of the tabu search algorithm


def tot_value(seq: List[int]) -> int:
    """
    Get objective function value from a sequence.
    params:
    - seq: list of integer numbers from 1 to n with n=len(seq) that represents a sequence of jobs
    return value: value of the objective function with the sequece seq
    """
    result = 0
    for i in range(len(seq)):
        # sum of the processing times [C_j]
        times_sum = sum([PROCESSING_TIMES[seq[j]-1] for j in range(i+1)])
        # objective function
        result += PENALTIES[i] * max(0, times_sum - DUE_DATES[seq[i] - 1])
    return result


def neighborhood(seq: List[int]) -> List[Tuple[List[int], Tuple[int, int]]]:
    """
    Get the neighborhood of a sequence.
    params:
    - seq: list of integer numbers from 1 to n with n=len(seq) that represents a sequence of jobs
    return value: a list of neighbors, which are represented by a tuple:
        the first element of a tuple is a sequence in the same format as seq, neighbor of seq
        the second element is the move that creates the new sequence, which is represented as a tuple with the ids of the jobs swapped
    """
    result = []
    for combo in list(combinations(seq, 2)):
        actual_combo = seq.copy()
        # swapping two jobs
        actual_combo[combo[0]-1], actual_combo[combo[1]-1] = actual_combo[combo[1]-1], actual_combo[combo[0]-1]
        result.append((actual_combo, combo))
    return result


def get_best_neighbor(seq: List[int], tabu_moves: List[Tuple[int, int]]) -> Tuple[List[int], Tuple[int, int]]:
    """
    Get the neighbor with the minimum value of the objective function of a sequence if the corresponding move is not tabu
    - seq: list of integer numbers from 1 to n with n=len(seq) that represents a sequence of jobs
    - tabu_moves: list of tuples which represent the tabu list, every tuple has the ids of the jobs swapped
    return value: a neighbors, which is represented by a tuple:
        the first element of the tuple is a sequence in the same format as seq, neighbor of seq
        the second element is the move that creates the new sequence, which is represented as a tuple with the ids of the jobs swapped
    """
    actual_neighborhood = neighborhood(seq)
    first_neighbor = actual_neighborhood[0]
    actual_neighbor, actual_best, actual_move = first_neighbor[0], tot_value(first_neighbor[0]), first_neighbor[1]
    # explore the neighborhood and find the neighbor with the minimum value
    for neighbor, move in actual_neighborhood[1:]:
        if move not in tabu_moves:
            neighbor_value = tot_value(neighbor)
            if neighbor_value <= actual_best:
                actual_neighbor, actual_best, actual_move = neighbor, neighbor_value, move
    
    return actual_neighbor, actual_move


def tabu_search():
    """
    Execute the tabu search algorithm with a starting solution and a tabu list with tabu tenure equals to the variable TABU_TENURE.
    It makes a prefixed number of iterations, given by the variable ITERATIONS.
    It tracks the best solution found during each iterations, and the best global solution found.
    It prints the starting solution with its value, and the starting tabu list, which is empty.
    Then it prints the sequence found at each iteration and its value.
    Finally it prints the best solution found in these iterations and its value.
    """
    best_solution = (STARTING, tot_value(STARTING))
    tabu_moves = []
    actual_sequence = STARTING
    print(f"Starting sequence: {STARTING} with value: {tot_value(STARTING)}. Tabu list: {tabu_moves}")

    for i in range(ITERATIONS):
        actual_sequence, move = get_best_neighbor(actual_sequence, tabu_moves)
        # check if this is the best solution found so far
        if tot_value(actual_sequence) < best_solution[1]:
            best_solution = actual_sequence, tot_value(actual_sequence)
        # make the last move tabu
        tabu_moves.append(move)
        # remove the oldest move if tabu list is full
        if len(tabu_moves) > TABU_TENURE:
            tabu_moves.pop(0)
        print(f"Best sequence found at iteration {i+1}: {actual_sequence} with value: {tot_value(actual_sequence)}. Tabu list: {tabu_moves}")
        # print(f"{i+1} & {str(actual_sequence).replace('[','').replace(']','')} & {tot_value(actual_sequence)} & {str(tabu_moves).replace('[','').replace(']','')} \\\\")

    print(f"Best sequence found after {ITERATIONS} iterations: {best_solution[0]}, with value: {best_solution[1]}")


if __name__ == "__main__":
    tabu_search()
