import axelrod as axl
from axelrod_dojo.utils import Params
from numpy import random

C, D = axl.Action


class CyclerParams(Params):
    """
    This cycler params class processes the best sequence of moves to beat a single any single opponent
    """

    def __init__(self, set_seq=None, seq_length: int = 200, mutation_probability=0.1):

        if set_seq is None:
            # generates sequence uses a map to the Action class to change a sequence of 1 & 0s to C & D actions
            self.sequence = list(map(axl.Action, random.randint(0, 1 + 1, (seq_length, 1))))
            self.sequence_length = seq_length
        else:
            #  when passing a sequence, make a copy of the sequence to ensure mutation is for the instance only.
            self.sequence = list(set_seq)
            self.sequence_length = len(set_seq)

        self.mutation_probability = mutation_probability

    def vector_to_instance(self):
        super().vector_to_instance()

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
        return CyclerParams(set_seq=seq_p1 + seq_p2)

    def from_repr(self):
        super().from_repr()

    def create_vector_bounds(self):
        super().create_vector_bounds()

    def params(self):
        super().params()

    def player(self):
        return axl.Cycler(self.get_sequence())

    def receive_vector(self, vector):
        super().receive_vector(vector)

    def __repr__(self):
        super().__repr__()

    def mutate(self):
        # we treat the mutation probability uniquely for the entire sequence, and we will only mutate a single gene
        # if the mutation occurs
        if random.rand() <= self.mutation_probability:
            mutated_sequence = self.get_sequence()
            # no +1 as the len() will get the index of the last item
            index_to_change = random.randint(0, len(mutated_sequence))

            # Mutation - change a single gene
            if mutated_sequence[index_to_change] == C:
                mutated_sequence[index_to_change] = D
            else:
                mutated_sequence[index_to_change] = C
            self.sequence = mutated_sequence

    def random(self):
        super().random()

    def copy(self):
        # seq length will be provided when copying
        return CyclerParams(set_seq=self.get_sequence(), mutation_probability=self.get_mutation_probability())

    def get_sequence(self):
        return self.sequence

    def get_sequence_length(self):
        return self.sequence_length

    def get_mutation_probability(self):
        return self.mutation_probability
