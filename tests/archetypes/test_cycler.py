import unittest

import axelrod as axl
from axelrod_dojo.archetypes.cycler import CyclerParams

C, D = axl.Action


class TestCyclerParams(unittest.TestCase):
    def setUp(self):
        self.instance = None

    # Basic creation methods setting the correct params

    def test_creation_seqLen(self):
        test_length = 10
        self.instance = CyclerParams(seq_length=test_length)
        self.assertEqual(self.instance.get_sequence_length(), test_length)
        self.assertEqual(len(self.instance.get_sequence()), test_length)

    def test_creation_seq(self):
        test_seq = [C, C, D, C, C, D, D, C, D, D]
        self.instance = CyclerParams(set_seq=test_seq)
        self.assertEqual(self.instance.get_sequence_length(), len(test_seq))
        self.assertEqual(self.instance.get_sequence(), test_seq)

    # def test_creation_both(self):
    #     TO BE IMPLEMENTED
    #     ------------
    #     test_length = 10
    #     test_seq = [C, C, D, C, C, D, D, C, D, D]
    #     self.assertRaises(ValueError, CyclerParams(set_seq=test_seq, seq_length=test_length))

    def test_crossover_1(self):
        test_seq_1 = [C, D, D, C, C, D, D, C]
        test_seq_2 = [C, D, C, C, D, D, C, D]
        result_seq = [C, D, D, C, D, D, C, D]

        self.instance = CyclerParams(set_seq=test_seq_1)
        instance_two = CyclerParams(set_seq=test_seq_2)
        out_cycler = self.instance.crossover(instance_two)
        self.assertEqual(out_cycler.get_sequence(), result_seq)

    def test_crossover_2(self):
        test_seq_1 = [C, D, D, C, C, D, D]
        test_seq_2 = [C, D, C, C, D, D, C]
        result_seq = [C, D, D, C, D, D, C]

        self.instance = CyclerParams(set_seq=test_seq_1)
        instance_two = CyclerParams(set_seq=test_seq_2)
        out_cycler = self.instance.crossover(instance_two)
        self.assertEqual(out_cycler.get_sequence(), result_seq)

    def test_mutate(self):
        test_seq = [C, D, D, C, C, D, D]
        self.instance = CyclerParams(set_seq=test_seq, mutation_probability=1)
        self.instance.mutate()
        # these are dependent on each other but testing both will show that we haven't just removed a gene
        self.assertEqual(len(test_seq), self.instance.get_sequence_length())
        self.assertNotEqual(test_seq, self.instance.get_sequence())

    def test_copy(self):
        test_seq = [C, D, D, C, C, D, D]
        self.instance = CyclerParams(set_seq=test_seq)
        instance_two = self.instance.copy()
        self.assertFalse(self.instance is instance_two)
