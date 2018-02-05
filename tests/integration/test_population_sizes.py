import tempfile
import unittest

import axelrod as axl
import axelrod_dojo as axl_dojo

POPULATION_SIZE = 20


class TestPopulationSizes(unittest.TestCase):

    def test_basic_pop_size(self):
        # Set up Tmp file
        temp_file = tempfile.NamedTemporaryFile(delete=False)
        # we will set the objective to be
        cycler_objective = axl_dojo.prepare_objective(name="score", turns=10, repetitions=1)
        # Lets use an opponent_list of just one:
        opponent_list = [axl.TitForTat()]
        # params to pass through
        cycler_kwargs = {
            "sequence_length": 10
        }

        population = axl_dojo.Population(params_class=axl_dojo.CyclerParams,
                                         params_kwargs=cycler_kwargs,
                                         size=POPULATION_SIZE,
                                         objective=cycler_objective,
                                         output_filename=temp_file.name,
                                         opponents=opponent_list)

        # Before run
        self.assertEqual(len(population.population), POPULATION_SIZE)

        # After Run
        population.run(generations=5)
        self.assertEqual(len(population.population), POPULATION_SIZE)

        # close the temp file
        temp_file.close()

    def test_bottleneck_pop_size(self):
        # Set up Tmp file
        temp_file = tempfile.NamedTemporaryFile(delete=False)
        # we will set the objective to be
        cycler_objective = axl_dojo.prepare_objective(name="score", turns=10, repetitions=1)
        # Lets use an opponent_list of just one:
        opponent_list = [axl.TitForTat()]
        # params to pass through
        cycler_kwargs = {
            "sequence_length": 10
        }

        population = axl_dojo.Population(params_class=axl_dojo.CyclerParams,
                                         params_kwargs=cycler_kwargs,
                                         size=POPULATION_SIZE,
                                         bottleneck=1,
                                         objective=cycler_objective,
                                         output_filename=temp_file.name,
                                         opponents=opponent_list)

        # Before run
        self.assertEqual(len(population.population), POPULATION_SIZE)

        # After Run
        population.run(generations=5)
        self.assertEqual(len(population.population), POPULATION_SIZE)

        # close the temp file
        temp_file.close()
