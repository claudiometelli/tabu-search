from itertools import permutations
from tabusearch import ITERATIONS, tot_value, neighborhood

def greedy_ls(seq):
    best_sequence, best_value = seq, tot_value(seq)
    iterations = 0
    while True:
        actual_neighborhood = neighborhood(best_sequence)
        first_neighbor = actual_neighborhood[0]
        actual_neighbor, actual_best = first_neighbor[0], tot_value(first_neighbor[0])

        for neighbor, _ in actual_neighborhood[1:]:
            neighbor_value = tot_value(neighbor)
            if neighbor_value <= actual_best:
                actual_neighbor, actual_best = neighbor, neighbor_value
        
        if actual_best < best_value:
            iterations += 1
            best_sequence, best_value = actual_neighbor, actual_best
            if iterations == 10: break
        else:
            break
        
    return best_sequence, best_value, iterations


if __name__ == "__main__":
    total_iterations = 0
    max_iterations_reached = 0
    average_value = 0
    possible_sequences = [list(seq) for seq in list(permutations(range(1, 7)))]
    for sequence in possible_sequences:
        best_sequence, best_value, iterations = greedy_ls(sequence)
        average_value += best_value
        if iterations < ITERATIONS:
            total_iterations += iterations
        else:
            max_iterations_reached += 1
    average_value /= len(possible_sequences)
    average_iterations = total_iterations / len(possible_sequences)
    print(f"Greedy Local Search found {len(possible_sequences) - max_iterations_reached} local minimum within {ITERATIONS} iterations.")
    print(f"Greedy Local Search found {max_iterations_reached} solutions stopping after {ITERATIONS} iterations.")
    print(f"Average value: {average_value}.")
    print(f"Average iterations of the algorithm: {average_iterations}")
