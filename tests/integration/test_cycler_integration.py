import os
import tempfile
import unittest

import axelrod as axl
import axelrod_dojo as axl_dojo


class TestCyclerParams(unittest.TestCase):
    def setUp(self):
        pass

    def test_default_single_opponent_e2e(self):
        temp_file = tempfile.NamedTemporaryFile(delete=False)
        # we will set the objective to be
        cycler_objective = axl_dojo.prepare_objective(name="score", turns=10, repetitions=1)

        # Lets use an opponent_list of just one:
        opponent_list = [axl.TitForTat(), axl.Calculator()]
        cycler = axl_dojo.CyclerParams

        # params to pass through
        cycler_kwargs = {
            "sequence_length": 10
        }

        # assert file is empty to start
        self.assertEqual(temp_file.readline(), b'')  # note that .readline() reads bytes hence b''

        population = axl_dojo.Population(params_class=cycler,
                                         params_kwargs=cycler_kwargs,
                                         size=20,
                                         objective=cycler_objective,
                                         output_filename=temp_file.name,
                                         opponents=opponent_list)

        cycler_generations = 5
        population.run(cycler_generations)

        # assert the output file exists and is not empty
        self.assertTrue(os.path.exists(temp_file.name))
        self.assertNotEqual(temp_file.readline(), b'')  # note that .readline() reads bytes hence b''

        # close the temp file
        temp_file.close()


class test_seeding_function(unittest.TestCase):
    def test_random_player(self):
        # Get seeded players
        seeded_class_one = axl_dojo.utils.get_seeded_opponent_instance(axl.Random)
        seeded_class_two = axl_dojo.utils.get_seeded_opponent_instance(axl.Random)

        # Create matches with seeded instances
        match_one = axl.Match((axl.TitForTat(), seeded_class_one(),), 20)
        match_two = axl.Match((axl.TitForTat(), seeded_class_two(),), 20)

        # Ensure both seeded classes play the same
        self.assertEqual(match_two.play(), match_one.play())

    def test_ZD_player(self):
        # Create a seeded player
        seeded_player_one = axl_dojo.utils.get_seeded_opponent_instance(axl.ZDExtort3)()

        # Play this player against two opponents
        match_one = axl.Match((axl.CollectiveStrategy(), seeded_player_one,), 20)
        match_two = axl.Match((axl.CollectiveStrategy(), seeded_player_one,), 20)

        # Assert it plays the same across matches.
        self.assertEqual(match_two.play(), match_one.play())
