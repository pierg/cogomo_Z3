from z3 import *


class Contract(object):
    """Contract class stores data attributes of a contract

    We don't use the Or out of Z3 but we manually build a data structure to check that all the combination can be satisfiable
    If we would do an OR for example here:

    s = Solver()

    x = Real('x')
    z = Real('z')

    s.assert_and_track(Or(x > 0, z > 100), 'a1')
    s.assert_and_track(x < 0, 'a2')
    print(s.check())
    print(s.unsat_core())

    We wouldn't see that the first case (x>0) can never be satisfiable

    CoGoMO checks that as well

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
        elif isinstance(guarantees, list):
            self.guarantees = guarantees
        else:
            raise Exception("Attribute Error")

        if assumptions is None:
            self.assumptions = []
        elif isinstance(assumptions, list):
            self.assumptions = assumptions
        else:
            raise Exception("Attribute Error")

        if variables is None:
            self.variables = {}
        elif isinstance(variables, dict):
            self.variables = variables
        else:
            raise Exception("Attribute Error")

    def add_variable(self, variable):
        """Adds a variable to the contract variables

        Args:param variable: a tuple of strings containing name of the variable and a its type
        """
        name, var_type = variable
        if var_type == 'REAL':
            self.variables[name] = Real(name)
        elif var_type == 'BOOL':
            self.variables[name] = Bool(name)
        elif var_type == 'INT':
            self.variables[name] = Int(name)

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
        """Adds an assumption to the contract assumptions

        Args:
            assumption: Z3 proposition where the variables are contained in self.variables
        """
        if isinstance(assumption, str):
            if(assumption == '--'):
                self.assumptions.append(True)
            else:
                self.assumptions.append(eval(assumption))
        else:
            self.assumptions.append(assumption)

    def add_guarantee(self, guarantee):
        """Adds a guarantee to the contract guarantees

        Args:
            guarantee: Z3 proposition where the variables are contained in self.variables
        """
        if isinstance(guarantee, str):
            self.guarantees.append(eval(guarantee))
        else:
            self.assumptions.append(guarantee)

    def get_assumptions(self):
        return self.assumptions

    def get_z3_assumptions(self):
        if len(self.assumptions) > 1:
            return And(self.assumptions)
        else:
            return self.assumptions[0]

    def get_z3_guarantees(self):
        if len(self.guarantees) > 1:
            # return And(self.guarantees)
            return Implies(self.get_z3_assumptions(), And(self.guarantees))
        else:
            # return self.guarantees[0]
            return Implies(self.get_z3_assumptions(), self.guarantees[0])

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


    def is_abstracted(self):
        return False


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

