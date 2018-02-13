import unittest

import axelrod as axl
from axelrod_dojo.archetypes.cycler import CyclerParams

C, D = axl.Action


class TestCyclerParams(unittest.TestCase):
    def setUp(self):
        self.instance = None

    # Basic creation methods setting the correct params

    def test_creation_seqLen(self):
        # TODO: create a particular creation separate to length
        axl.seed(0)
        test_length = 10
        self.instance = CyclerParams(sequence_length=test_length)
        self.assertEqual(self.instance.get_sequence(), [D, C, C, D, C, C, C, C, C, C])
        self.assertEqual(self.instance.get_sequence_length(), test_length)
        self.assertEqual(len(self.instance.get_sequence()), test_length)

    def test_creation_seq(self):
        test_seq = [C, C, D, C, C, D, D, C, D, D]
        self.instance = CyclerParams(sequence=test_seq)
        self.assertEqual(self.instance.get_sequence_length(), len(test_seq))
        self.assertEqual(self.instance.get_sequence(), test_seq)

    # def test_creation_both(self):
    #     TO BE IMPLEMENTED
    #     ------------
    #     test_length = 10
    #     test_seq = [C, C, D, C, C, D, D, C, D, D]
    #     self.assertRaises(ValueError, CyclerParams(set_seq=test_seq, seq_length=test_length))

    def test_crossover_even_length(self):
        # Even test
        test_seq_1 = [C] * 6
        test_seq_2 = [D] * 6
        result_seq = [C, C, C, D, D, D]

        self.instance = CyclerParams(sequence=test_seq_1)
        instance_two = CyclerParams(sequence=test_seq_2)
        out_cycler = self.instance.crossover(instance_two)
        self.assertEqual(result_seq, out_cycler.get_sequence())

    def test_crossover_odd_length(self):
        # Odd Test
        test_seq_1 = [C] * 7
        test_seq_2 = [D] * 7
        result_seq = [C, C, C, C, D, D, D]

        self.instance = CyclerParams(sequence=test_seq_1)
        instance_two = CyclerParams(sequence=test_seq_2)
        out_cycler = self.instance.crossover(instance_two)
        self.assertEqual(result_seq, out_cycler.get_sequence())

    def test_mutate(self):
        test_seq = [C, D, D, C, C, D, D]
        self.instance = CyclerParams(sequence=test_seq, mutation_probability=1)
        self.instance.mutate()
        # these are dependent on each other but testing both will show that we haven't just removed a gene
        self.assertEqual(len(test_seq), self.instance.get_sequence_length())
        self.assertNotEqual(test_seq, self.instance.get_sequence())

    def test_copy(self):
        test_seq = [C, D, D, C, C, D, D]
        self.instance = CyclerParams(sequence=test_seq)
        instance_two = self.instance.copy()
        self.assertFalse(self.instance is instance_two)
