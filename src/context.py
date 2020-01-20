from src.components import *


class Context(Component):
    """
    General Context Class
    """

    def __init__(self, name):
        super().__init__(id=name)
        self.name = name
        self.add_assumption("TRUE")


class Robot(Context):

    def __init__(self, name, weight_power=None):
        """
        :type lifting_power:
        """
        super().__init__(name)

        self.add_variable(('weight_power', "5..15"))
        self.add_guarantee(weight_power)


class Collaborate(Context):

    def __init__(self, name, weight_power=None):
        super().__init__(name)

        self.add_variable(('weight_power', "5..15"))
        self.add_assumptions(["weight_power_port_1 > 5", "weight_power_port_2 > 5"])
        self.add_guarantee(weight_power)

