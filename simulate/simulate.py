import random
from mendelianPea.pea.pea import Pea
import pandas as pd


class SimNotRun(Exception):
    pass


class Simulate(object):
    """
    Simulate pea evolution for a given number of generation
    """
    GENERATION_COLUMNS = ["color_gene", "shape_gene", "color", "shape", "survival", "color_D", "color_R", "color_DR",
                          "shape_D", "shape_R", "shape_DR"]

    ITERATION_COLUMNS = ["Iteration", "Generation", "Green", "Yellow", "Round", "Wrinkled",
                         "Color Dominant Homozygote", "Color Recessive Homozygote", "Color Heterozygote",
                         "Shape Dominant Homozygote", "Shape Recessive Homozygote", "Shape Heterozygote", "Total"]

    def __init__(self, generation0, no_of_generations, no_of_children, base_survival, advantage):
        """

        :param generation0 (DataFrame of peas): This is the start point for the simulation
        :param no_of_generations (int): Total number of generations to simulate
        :param advantage (dict): Dictionary holding the gene data along with survival probability
        :param no_of_children (int): Number of children a pair of peas can spawn per generation
        """
        generation0_df = pd.DataFrame(
            [(x._color_gene, x._shape_gene, x.active_color_gene, x.active_shape_gene, x.survival,
              1 if x.is_color_dominant_homozygote() else 0,
              1 if x.is_color_recessive_homozygote() else 0,
              1 if x.is_color_hetrozygote() else 0,
              1 if x.is_shape_dominant_homozygote() else 0,
              1 if x.is_shape_recessive_homozygote() else 0,
              1 if x.is_shape_hetrozygote() else 0,
              ) for x in generation0],
            columns=Simulate.GENERATION_COLUMNS)
        self.generation0 = generation0_df
        self.cur_generation = generation0_df
        self.next_generation = pd.DataFrame()

        self.no_of_generations = no_of_generations
        self.advantage = advantage
        self.base_survival = base_survival
        self.no_of_children = no_of_children
        self.generation_index = 0
        self.stats = None
        if self.advantage is not None:
            Pea.set_advantage(self.advantage)
        if self.base_survival is not None:
            Pea.set_base_survival(self.base_survival)

        self.generation_results = []
        self.iteration_results = pd.DataFrame()

    def _init_data(self, ):
        """
        Re-initialises the simulation
        :return:
        """
        self.cur_generation = self.generation0
        self.next_generation = pd.DataFrame()

        self.generation_index = 0
        self.stats = None
        Pea.set_advantage(self.advantage)
        Pea.set_base_survival(self.base_survival)

    def kill_peas(self, pea_df):
        """
        Randomly kills peas based on their survival probability
        :param pea_list: list of peas
        :return:
        """
        for s in pea_df:
            p = random.random()
            if s["survival"] < p:
                pea_df.drop(index=s.index, inplace=True)
        return pea_df

    def spawn_peas(self, pea1, pea2):
        """
        it spawn peas based on no_of_childern parameter
        :param pea1: parent 1
        :param pea2: parent 2
        :return (list of peas): randomly selecting peas for the next generation based on their survival probability
        """
        result = pd.DataFrame([], columns=Simulate.GENERATION_COLUMNS)
        for _ in range(self.no_of_children):
            child = Pea.spawn(pea1, pea2)
            p = random.random()
            if p < child.survival:  # This pea survived
                new_df = pd.DataFrame([[child._color_gene, child._shape_gene, child.active_color_gene,
                                        child.active_shape_gene, child.survival,
                                        1 if child.is_color_dominant_homozygote() else 0,
                                        1 if child.is_color_recessive_homozygote() else 0,
                                        1 if child.is_color_hetrozygote() else 0,
                                        1 if child.is_shape_dominant_homozygote() else 0,
                                        1 if child.is_shape_recessive_homozygote() else 0,
                                        1 if child.is_shape_hetrozygote() else 0,
                                        ]], columns=Simulate.GENERATION_COLUMNS)
                result = pd.concat((result, new_df), ignore_index=True)
        return result

    def get_next_generation(self, cur_generation):
        """
        Generates the next generation based on the current generation and kills the current generation
        :param cur_generation: list of peas
        :return: next generation as a list of peas
        """
        cur_generation = cur_generation.sample(frac=1)
        self.next_generation = pd.DataFrame([], columns=Simulate.GENERATION_COLUMNS)
        while not cur_generation.empty:
            pea1 = cur_generation[0:1]
            cur_generation.drop(index=pea1.index.values[0], inplace=True)
            if cur_generation.empty:
                break
            pea2 = cur_generation[0:1]
            cur_generation.drop(index=pea2.index.values[0], inplace=True)

            p1 = Pea(**{"color": pea1.color_gene.values[0], "shape": pea1.shape_gene.values[0]})
            p2 = Pea(**{"color": pea2.color_gene.values[0], "shape": pea2.shape_gene.values[0]})
            result_df = self.spawn_peas(p1, p2)
            if self.next_generation.empty:
                self.next_generation = result_df
            else:
                self.next_generation = pd.concat((self.next_generation, result_df), ignore_index=True)
        if not cur_generation.empty and cur_generation.shape[0] == 1:
            cur_generation.drop(cur_generation.index, inplace=True)  # Just discard this pea
        return self.next_generation

    def run(self, iteration, net_progression=None):
        """
        Run the simulation based on the supplied parameters
        :return:
        """

        if net_progression is None:
            net_progression = pd.DataFrame()

        while len(self.cur_generation) > 0 and self.generation_index < self.no_of_generations:

            self.cur_generation = self.get_next_generation(self.cur_generation)
            self.generation_index += 1
            lst = [[iteration, self.generation_index] + self.get_cur_generation_stats()]

            new_df = pd.DataFrame(lst, columns=Simulate.ITERATION_COLUMNS)
            if net_progression.empty:
                net_progression = new_df
            else:
                net_progression = pd.concat((net_progression, new_df), ignore_index=True)
            print("Completed Generation : {} : Total Population: {}".format(self.generation_index,
                                                                            net_progression.tail(1)["Total"].values[0]))

        return net_progression

    def run_iterations(self, iterations, advantage=None, base_survival=None):
        for y in range(iterations):
            self._init_data()
            if advantage is not None:
                Pea.set_advantage(self.advantage)
            if base_survival is not None:
                Pea.set_base_survival(self.base_survival)

            cur_generation_results = self.run(y, None)
            self.generation_results.append(cur_generation_results)

            lst = [[y, self.generation_index] + self.get_cur_generation_stats()]
            new_df = pd.DataFrame(lst, columns=Simulate.ITERATION_COLUMNS)
            if self.iteration_results.empty:
                self.iteration_results = new_df
            else:
                self.iteration_results = pd.concat((self.iteration_results, new_df), ignore_index=True)
            print("Iteration : {} : TotalPoulation : {}".format(y, self.iteration_results.tail(1)["Total"].values[0]))

    def get_cur_generation_stats(self):
        if not self.cur_generation.empty:
            total_count = self.cur_generation.shape[0]
            green_count = self.cur_generation[self.cur_generation["color"] == "G"]["color"].count()
            yellow_count = total_count - green_count
            wrinkled_count = self.cur_generation[self.cur_generation["shape"] == "w"]["shape"].count()
            round_count = total_count - wrinkled_count
            color_D = self.cur_generation["color_D"].sum()
            color_R = self.cur_generation["color_R"].sum()
            color_DR = self.cur_generation["color_DR"].sum()
            shape_D = self.cur_generation["shape_D"].sum()
            shape_R = self.cur_generation["shape_R"].sum()
            shape_DR = self.cur_generation["shape_DR"].sum()
            return [green_count / total_count, yellow_count / total_count, round_count / total_count,
                    wrinkled_count / total_count,
                    color_D / total_count, color_R / total_count, color_DR / total_count,
                    shape_D / total_count, shape_R / total_count, shape_DR / total_count,
                    total_count]
        else:
            return [0] * 11

    def save_xls(self, file_path):

        if len(self.generation_results) > 0:
            with pd.ExcelWriter(file_path) as writer:
                self.iteration_results.to_excel(writer, "Net Results")
                for n, df in enumerate(self.generation_results):
                    df.to_excel(writer, 'iteration_{}'.format(n), index=False)
                writer.save()
        else:
            raise SimNotRun("Please run the simulation before saving the results in an excel")
