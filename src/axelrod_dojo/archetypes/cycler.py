import axelrod as axl
from numpy import random

from axelrod_dojo.utils import Params

C, D = axl.Action


class CyclerParams(Params):
    """
    Cycler params is a class to aid with the processes of calculating the best sequence of moves for any given set of
    opponents. Each of the population in our algoruthem will be an instance of this class for putting into our
    genetic lifecycle.

    **********
    TODOs:
        * create a metaheuristic for mutations to increase mutation & crossover efficiency (ie, dont change the same
        gene 2 times in a row or try and do a crossover if the genes being swapped are sufficiently different)
    """

    def __init__(self, sequence=None, sequence_length: int = 200, mutation_probability=0.1):

        if sequence is None:
            # generates sequence uses a map to the Action class to change a sequence of 1 & 0s to C & D actions
            self.sequence = self.generate_random_sequence(sequence_length)
            self.sequence_length = sequence_length
        else:
            #  when passing a sequence, make a copy of the sequence to ensure mutation is for the instance only.
            self.sequence = list(sequence)
            self.sequence_length = len(sequence)

        self.mutation_probability = mutation_probability

    def __repr__(self):
        return "{}".format(self.sequence)

    @staticmethod
    def generate_random_sequence(sequence_length):
        """
        Generates a sequence of random moves when an instance is initialised

        Parameters
        ----------
        sequence_length - length or random moves to generate

        Returns
        -------
        list - a list of C & D actions: e.g. [C,C,D,D,C]
        """
        return list(map(axl.Action, random.randint(0, 1 + 1, (sequence_length, 1))))

    def crossover(self, other_cycler):
        """
        creates and returns a new CyclerParams instance with a single crossover point in the middle
        Parameters

        if the length of the sequences is odd, there will be one more element from the self CyclerParams
        ----------
        other_cycler - the other cycler where we get the other half of the sequence

        Returns
        -------
        CyclerParams

        """
        # boring single point crossover:
        crossover_point = int(self.get_sequence_length() // 2)
        # get half 1
        seq_p1 = self.get_sequence()[0: crossover_point]
        # get half 2
        seq_p2 = other_cycler.get_sequence()[crossover_point: other_cycler.get_sequence_length()]
        crossed_sequence = seq_p1 + seq_p2
        return CyclerParams(sequence=crossed_sequence)

    def mutate(self):
        """
        Basic mutation which changes a single gene in the sequence.
        """
        # if the mutation occurs
        if random.rand() <= self.mutation_probability:
            mutated_sequence = self.get_sequence()
            # no +1 as the len() will get the index of the last sequence item
            index_to_change = random.randint(0, len(mutated_sequence))

            # Mutation - change a single gene
            if mutated_sequence[index_to_change] == C:
                mutated_sequence[index_to_change] = D
            else:
                mutated_sequence[index_to_change] = C
            self.sequence = mutated_sequence

    def player(self):
        """
        Create and return a Cycler player with the sequence that has been generated with this run.

        Returns
        -------
        Cycler(sequence)
        """
        return axl.Cycler(self.get_sequence_str())

    def copy(self):
        """
        Returns a copy of the current cyclerParams

        Returns
        -------
        CyclerParams - a separate instance copy of itself.
        """
        # seq length will be provided when copying
        return CyclerParams(sequence=self.get_sequence(), mutation_probability=self.get_mutation_probability())

    def get_sequence_str(self):
        """
        Concatenate all the actions as a string for constructing Cycler players

        [C,D,D,C,D,C] -> "CDDCDC"
        [C,C,D,C,C,C] -> "CCDCCC"
        [D,D,D,D,D,D] -> "DDDDDD"

        Returns
        -------
        str
        """
        string_sequence = ""
        for action in self.sequence:
            string_sequence += str(action)

        return string_sequence

    # Getters --------------------
    def get_sequence(self):
        return self.sequence

    def get_sequence_length(self):
        return self.sequence_length

    def get_mutation_probability(self):
        return self.mutation_probability
