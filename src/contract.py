from src.sat_checks import *

class Contract(object):
    """Contract class stores data attributes of a contract
    """

    def __init__(self,
                 variables=None,
                 assumptions=None,
                 guarantees=None):
        """Initialize a contract object"""
        self.variables = {}
        self.assumptions = []
        self.guarantees = []

        if variables is None:
            self.variables = {}
        elif isinstance(variables, dict):
            self.variables = variables
        else:
            raise Exception("Attribute Error")

        if guarantees is None:
            self.guarantees = []
        elif isinstance(guarantees, list):
            self.add_guarantees(guarantees)
        else:
            raise Exception("Attribute Error")

        if assumptions is None:
            self.assumptions = []
        elif isinstance(assumptions, list):
            self.add_assumptions(assumptions)
        else:
            raise Exception("Attribute Error")

    def add_variable(self, variable):
        """Adds a variable to the contract variables

        Args:param variable: a tuple of strings containing name of the variable and a its type
        """
        name, var_type = variable
        self.variables[name] = var_type


    def add_variables(self, variables):
        """Adds a list of variables to the contract variables

        :param variables: list of tuple of strings each containing name of the variable and a its type
        """
        for variable in variables:
            self.add_variable(variable)


    def merge_variables(self, variables_dictionary):

        variables_copy = self.variables.copy()
        variables_copy.update(variables_dictionary)
        self.variables = variables_dictionary

    def get_variables(self):

        return self.variables

    def add_constant(self, constant):
        """Add integer constant together with the contract variables
        :param constant: a tuple containing the constant name and the value (int)
        """
        name, value = constant
        self.variables[name] = value

    def add_assumptions(self, assumptions):
        for assumption in assumptions:
            self.add_assumption(assumption)

    def add_assumption(self, assumption):
        if isinstance(assumption, str) == False:
            raise AttributeError

        """Check if assumption is a refinement of exising assumptions and vice-versa"""
        for a in self.assumptions:
            if is_set_smaller_or_equal(self.variables, self.variables, assumption, a):
                self.assumptions.remove(a)
            elif is_set_smaller_or_equal(self.variables, self.variables, a, assumption):
                return

        self.assumptions.append(assumption)

        """Check Compatibility"""
        if not check_satisfiability(self.variables, self.assumptions):
            raise Exception("adding " + assumption + " resulted in a incompatible contract:\n" + str(self.assumptions))


    def add_guarantees(self, guarantees):
        for guarantee in guarantees:
            self.add_guarantee(guarantee)

    def add_guarantee(self, guarantee):
        if isinstance(guarantee, str) == False:
            raise AttributeError

        """Check if guarantee is a refinement of exising gurantee and vice-versa"""
        for g in self.guarantees:
            if is_set_smaller_or_equal(self.variables, self.variables, guarantee, g):
                self.guarantees.remove(g)
            elif is_set_smaller_or_equal(self.variables, self.variables, g, guarantee):
                return

        self.guarantees.append(guarantee)

        """Check Consistency"""
        if not check_satisfiability(self.variables, self.guarantees):
            raise Exception("adding " + guarantee + " resulted in a inconsistent contract:\n" + str(self.guarantees))


    def get_assumptions(self):
        return self.assumptions

    def get_ltl_assumptions(self):
        if len(self.assumptions) > 1:
            return And(self.assumptions)
        else:
            return self.assumptions[0]

    def get_ltl_guarantees(self):
        if len(self.guarantees) > 1:
            # return And(self.guarantees)
            return Implies(self.get_ltl_assumptions(), And(self.guarantees))
        else:
            # return self.guarantees[0]
            return Implies(self.get_ltl_assumptions(), self.guarantees[0])

    def get_guarantees(self):

        return self.guarantees

    def is_full(self):
        """
        Check if contract parameters are filled
        :return: A boolean indicating if the contracts parameters are not empty
        """
        return self.variables and self.assumptions and self.guarantees

    def cost(self):
        """
        Used for component selection. Always [0, 1]
        Lower is better
        :return: Real number
        """
        lg = len(self.guarantees)
        la = len(self.assumptions)

        """heuristic
        Low: guarantees while assuming little (assumption set is bigger)
        High: guarantees while assuming a lot (assumption set is smaller)"""

        return la / lg



    def __str__(self):
        """Override the print behavior"""
        astr = '  variables: [ '
        for var in self.variables:
            astr += '(' + var + '), '
        astr = astr[:-2] + ' ]\n  assumptions: [ '
        for assumption in self.assumptions:
            astr += str(assumption) + ', '
        astr = astr[:-2] + ' ]\n  guarantees: [ '
        for guarantee in self.guarantees:
            astr += str(guarantee) + ', '
        return astr[:-2] + ' ]\n]'

