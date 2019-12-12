from src.contract import Contract

class CGTGoal():
    """
    Contract-based Goal Tree

    Attributes:
        contracts: a list of contract objects
        alphabet: a list of tuples containing the shared alphabet among all contracts
    """
    def __init__(self,
                 name="",
                 description="",
                 contracts=None,
                 sub_goals=None,
                 sub_operation=None,
                 parent_goal=None,
                 parent_operation=None):
        """Initialize a contracts object"""

        super().__init__()

        self.name = name
        self.description = description

        """List of assumption/guarantees pairs (Contract objects)
           Each element in the list represents a contract in CONJUNCTION"""
        if not isinstance(contracts, list):
            self.contracts = [contracts]
        else:
            self.contracts = contracts

        # List of children and its relationship with them (COMPOSITION / CONJUNCTION)
        self.sub_goals = sub_goals
        self.sub_operation = sub_operation

        # Parent goal and its relation (COMPOSITION / CONJUNCTION)
        self.parent_goal = parent_goal
        self.parent_operation = parent_operation

    def set_parent(self, parent_goal, parent_operation):
        self.parent_goal = parent_goal
        self.parent_operation = parent_operation

    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def set_description(self, description):
        self.description = description

    def get_description(self):
        return self.description

    def get_subgoals_ops(self):
        return self.sub_goals, self.sub_operation

    def get_contracts(self):
        return self.contracts


    def __str__(self, level=0):
        """Override the print behavior"""
        ret = "\t" * level + repr(self.name) + "\n"
        ret += "\t" * level + repr(self.description) + "\n"
        for n, contract in enumerate(self.contracts):
            if n > 0:
                ret += "\t" * level + "\t/\\ \n"
            ret += "\t" * level + "A:\t\t" + \
                   ', '.join(str(x) for x in contract.get_assumptions()).replace('\n', ' ').replace(' ', '') + "\n"
            ret += "\t" * level + "G:\t\t" + \
                   ', '.join(str(x) for x in contract.get_guarantees()).replace('\n', ' ').replace(' ', '') + "\n"
            # if contract.is_abstracted():
            #     ret += "\t" * level + "G_abs:\t" + \
            #            ', '.join(str(x) for x in contract.get_abstract_guarantees()).replace('\n', ' ').replace(' ',
            #                                                                                                     '') + "\n"
        ret += "\n"
        if self.sub_goals is not None and len(self.sub_goals) > 0:
            ret += "\t" * level + "\t" + self.sub_operation + "\n"
            level += 1
            for child in self.sub_goals:
                ret += child.__str__(level + 1)
        return ret

    def __eq__(self, other):
        """Override the default Equals behavior"""
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return False

    def __ne__(self, other):
        """Define a non-equality test"""
        return not self.__eq__(other)
