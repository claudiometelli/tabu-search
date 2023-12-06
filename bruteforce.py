from itertools import permutations
from tabusearch import STARTING, tot_value


if __name__ == "__main__":
    """
    This program just tries all the possible permutations of sequences and computes the respective objective function.
    It finds sequence with the best objective function value.
    It also finds how many optimal sequence there are.
    """
    best_sequence, best_value = STARTING, tot_value(STARTING)
    possible_sequences = [list(seq) for seq in list(permutations(range(1, 7)))]
    values = []
    for sequence in possible_sequences:
        value = tot_value(sequence)
        values.append(value)
        if value < best_value:
            best_sequence, best_value = sequence, value
    best_values = values.count(best_value)
    print(f"Best sequence among {len(possible_sequences)} possible sequences is {best_sequence}, with the optimal value: {best_value}.")
    print(f"There {'are' if best_values > 2 else 'is'} also {best_values-1} other sequences that has this optimal value.")