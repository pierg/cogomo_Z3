from z3 import *


class Contract(object):
    """Contract class stores data attributes of a contract

    Attributes:
        name: a string name for the contract
        variables: a dictionary containing the string of the variable as key, and the Z3 variable as value
        assumptions: a list of Z3 relations assumed by contract
        guarantees: a list of Z3 relations relations guaranteed by contract
    """

    def __init__(self,
                 variables=None,
                 assumptions=None,
                 guarantees=None):
        """Initialize a contract object"""

        if guarantees is None:
            self.guarantees = []
        else:
            self.guarantees = guarantees

        if assumptions is None:
            self.assumptions = []
        else:
            self.assumptions = assumptions

        if variables is None:
            self.variables = {}
        else:
            self.variables = variables

    def add_variable(self, variable):
        """Adds a variable to the contract variables

        Args:param variable: a tuple of strings containing name of the variable and a its type
        """
        name, var_type = variable
        if var_type == 'REAL':
            self.variables[name] = Real(name)
        elif var_type == 'BOOL':
            self.variables[name] = Bool(name)

    def add_variables(self, variables):
        """Adds a list of variables to the contract variables

        :param variables: list of tuple of strings each containing name of the variable and a its type
        """
        for variable in variables:
            self.add_variable(variable)

    def get_variables(self):

        return self.variables

    def add_constant(self, constant):
        """Add integer constant together with the contract variables
        :param constant: a tuple containing the constant name and the value (int)
        """
        name, value = constant
        self.variables[name] = int(value)

    def add_assumption(self, assumption):
        """Adds an assumption to the contract assumptions

        Args:
            assumption: Z3 proposition where the variables are contained in self.variables
        """
        self.assumptions.append(eval(assumption))

    def add_guarantee(self, guarantee):
        """Adds a guarantee to the contract guarantees

        Args:
            guarantee: Z3 proposition where the variables are contained in self.variables
        """
        self.guarantees.append(eval(guarantee))


    def get_assumptions(self):

        return self.assumptions

    def get_guarantees(self):

        return self.guarantees

    def is_full(self):
        """
        Check if contract parameters are filled
        :return: A boolean indicating if the contracts parameters are not empty
        """
        return self.name and self.variables and self.assumptions and self.guarantees

    def compute_entropy(self):
        """
        Used fot the synthesis
        :return: A real indircating the between assumptions and guarantees
        """
        lg = len(self.guarantees)
        la = len(self.assumptions)

        return lg / (la + lg)

    def is_abstracted(self):
        return False

    def saturate_guarantees(self):
        """
        In CoGoMo we assume that the assumptions are always satisfied, no saturation needed
        """
        pass

    def __str__(self):
        """Override the print behavior"""
        astr = '[\n  name: [ ' + self.name + ' ]\n'
        astr += '  variables: [ '
        for var in self.variables:
            astr += '(' + var + '), '
        astr = astr[:-2] + ' ]\n  assumptions: [ '
        for assumption in self.assumptions:
            astr += str(assumption) + ', '
        astr = astr[:-2] + ' ]\n  guarantees: [ '
        for guarantee in self.guarantees:
            astr += str(guarantee) + ', '
        return astr[:-2] + ' ]\n]'