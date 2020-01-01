from enum import Enum


class ColorGene(Enum):
    """
    Enumeration for a color gene on a Pea
    """
    GREEN = "G"
    YELLOW = "y"


class ShapeGene(Enum):
    """
    Enumeration for a shape gene in a pea
    """
    ROUND = "R"
    WRINKLED = "w"


class InvalidGene(Exception):
    """
    Exception class for invalid gene
    """
    pass


class PeaNotAlive(Exception):
    """
    Exception class for dead gene
    """
    pass


class InvalidBaseSurvival(Exception):
    """
    Exception class for invalid base survival probability value
    """
    pass


class Pea(object):
    """
    Pea class

    Attributes:
        VALID_SHAPE_GENES (str): List of valid shpaes for a Pea.
        BASE_SURVIVAL_CHANCE (float): Assigning a starting constant survival probability for a Pea.
        ADVANTAGE (dict) : Initialising survival probabilities based on gene variation
    """

    VALID_SHAPE_GENES = [i.value for i in ShapeGene]
    BASE_SURVIVAL_CHANCE = 0.4

    ADVANTAGE = {ColorGene.YELLOW.value: 0.11, ColorGene.GREEN.value: 0.15, ShapeGene.WRINKLED.value: 0.1}

    GENE_DESCRIPTION = {ColorGene.YELLOW.value: ColorGene.YELLOW.name.capitalize(),
                        ColorGene.GREEN.value: ColorGene.GREEN.name.capitalize(),
                        ShapeGene.WRINKLED.value: ShapeGene.WRINKLED.name.capitalize(),
                        ShapeGene.ROUND.value: ShapeGene.ROUND.name.capitalize()}

    def __init__(self, **kwargs):
        """
        Setting a new Pea instance
        :param kwargs: Selecting color, shape , status and calculating survival chance
        """
        self._color_gene = kwargs.get("color")
        self._shape_gene = kwargs.get("shape")
        self._validate_genes()

        self.active_color_gene = self._get_active_color_gene()
        self.active_shape_gene = self._get_active_shape_gene()
        self._set_survival_chance()
        self._set_description()
        self.is_alive = kwargs.get('is-alive', True)

    def _validate_genes(self):
        """
        Input : a Pea
        :return: Sets a color and and a shape for a it
        """
        self._color_gene = self._valid_gene(self._color_gene, ColorGene)
        self._shape_gene = self._valid_gene(self._shape_gene, ShapeGene)

    def _valid_gene(self, gene, valid_values):
        """
        Validating if the gene is valid
        :param gene: color and shape
        :param valid_values: from the enum defined
        :return: valid values for a Pea gene
        """

        final_gene = None
        if isinstance(gene, list):
            final_gene = ""
            for i in gene:
                if not isinstance(i, valid_values):
                    raise InvalidGene("Not a valid Gene type {}".format(type(i)))
                final_gene += i.value

        if isinstance(gene, str):
            final_gene = gene

        if not isinstance(final_gene, str) or len(final_gene) != 2:
            raise InvalidGene("Not a valid Gene {}".format(final_gene))
        return final_gene

    def _set_survival_chance(self):
        """
        Setting survival chance for a Pea
        :return: setting it up based on the color and shape
        """
        self.survival = Pea.BASE_SURVIVAL_CHANCE + \
                        Pea.ADVANTAGE.get(self.active_color_gene, 0) + \
                        Pea.ADVANTAGE.get(self.active_shape_gene, 0)

        if self.survival > 1:
            self.survival = 1
        if self.survival < 0:
            self.survival = 0

    def _set_description(self):
        """
        Setting up description for a Pea to print it later
        :return: None
        """
        self.description = Pea.GENE_DESCRIPTION.get(self._get_active_color_gene()) + " and " + \
                           Pea.GENE_DESCRIPTION.get(self._get_active_shape_gene())

    def _get_active_color_gene(self):
        """

        :return: returns active  color for a gene. (it may be dominant or recessive gene based on the combination)
        """
        return self._get_active_gene(self._color_gene)

    def _get_active_shape_gene(self):
        """

        :return: returns ac active hape of a gene. (it may be dominant or recessive gene based on the combination)
        """
        return self._get_active_gene(self._shape_gene)

    def _get_active_gene(self, gene):
        """
        Checking if a gene is still alove
        :param gene:
        :return: Returning the active gene (it may be dominant or recessive gene based on the combination from the parents)
        """
        active_gene = None

        for g in gene:
            if g.isupper():
                active_gene = g
                break

        if active_gene is None:
            active_gene = gene[0]

        return active_gene

    def is_color_recessive_homozygote(self):
        return self._get_active_color_gene() == ColorGene.YELLOW.value

    def is_color_dominant_homozygote(self):
        return self._color_gene == "GG"

    def is_color_hetrozygote(self):
        return self._color_gene == "Gy" or self._color_gene == "yG"

    def is_shape_recessive_homozygote(self):
        return self._get_active_shape_gene() == ShapeGene.WRINKLED.value

    def is_shape_dominant_homozygote(self):
        return self._shape_gene == "RR"

    def is_shape_hetrozygote(self):
        return not (self.is_shape_dominant_homozygote() or self.is_shape_recessive_homozygote())

    @classmethod
    def set_advantage(cls, advantage):
        """
        Setting the survival advantage for all Peas
        :param advantage (dict):containing survival advantage for each gene
        :return:
        """
        Pea.ADVANTAGE = advantage

    @classmethod
    def set_base_survival(cls, base_survival):
        """
        Initialising the base survival chance of for a Pea with user supplied base_survival
        :param base_survival (float): Since its a probability value , it should be between 0 and 1
        :return:
        """
        if 0 <= base_survival <= 1:
            Pea.BASE_SURVIVAL_CHANCE = base_survival
        else:
            raise InvalidBaseSurvival("Since its a probability value , it should be between 0 and 1")

    @classmethod
    def get_dominant_homozygote(cls):
        """
        :return: helper function to return a Pea with only dominant genes
        """
        return  Pea(**{"color": [ColorGene.GREEN, ColorGene.GREEN], "shape": [ShapeGene.ROUND, ShapeGene.ROUND]})

    @classmethod
    def get_recessive_homozygote(cls):
        """
        :return: helper function to return a Pea with only recessive genes
        """
        return  Pea(**{"color": [ColorGene.YELLOW, ColorGene.YELLOW], "shape": [ShapeGene.WRINKLED, ShapeGene.WRINKLED]})

    @classmethod
    def get_hetrozygote(cls):
        """

        :return: helper function to return a Pea with dominant and  recessive gene
        """
        return  Pea(**{"color": [ColorGene.GREEN, ColorGene.YELLOW], "shape": [ShapeGene.WRINKLED, ShapeGene.ROUND]})

    @classmethod
    def spawn(cls, pea1, pea2):
        """
        create a child pea from parents
        :param pea1: parent 1
        :param pea2: parent 2
        :return: child with 1 randomly selected gene from parent 1 and 1 randomly selected gene from parent 2
        """
        if not pea1.is_alive or not pea2.is_alive:
            raise PeaNotAlive("Both Peas should be alive to spawn!")

        import random
        c1 = random.choices([char for char in pea1._color_gene])[0]
        c2 = random.choices([char for char in pea2._color_gene])[0]

        s1 = random.choices([char for char in pea1._shape_gene])[0]
        s2 = random.choices([char for char in pea2._shape_gene])[0]
        genome = {"color": c1 + c2, "shape": s1 + s2}
        return Pea(**genome)

    def __str__(self):
        """

        :return: the prinatable version for the Pea class
        """
        return "{}{} : {} , {}".format(self._color_gene, self._shape_gene, self.survival, self.description)

