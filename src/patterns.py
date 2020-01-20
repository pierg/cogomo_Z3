from src.contract import *


class PatternException(object):
    print("Pattern Exception")


class Pattern(Contract):
    """
    General Pattern Class
    """
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.add_assumption("TRUE")


class CoreMovement(Pattern):
    """
    Core Movements Patterns
    All the variables are locations where there robot can be at a certain time
    """

    def add_physical_assumptions(self):
        """
        Add the assumptions that the robot cannot be at multiple locations at the same time
        """

        list_locations = []
        for location, type in self.get_variables().items():
            list_locations.append(location)

        # Eliminating duplicates
        list_locations = list(dict.fromkeys(list_locations))

        ltl_formula = "G("
        for i, loc in enumerate(list_locations):
            ltl_formula += "(" + loc
            for loc_other in list_locations:
                if loc != loc_other:
                    ltl_formula += " & !" + loc_other
            ltl_formula += ")"
            if i < len(list_locations) -1 :
                ltl_formula += " | "

        ltl_formula += ")"

        self.add_assumption(ltl_formula)


class Visit(CoreMovement):
    """
    Visit a set of locations in an unspecified order.
    """

    def __init__(self, name, list_of_locations=None):
        """
        :type list_of_locations: list of location, each location is a boolean
        indicating if the robot is at that location
        """
        super().__init__(name)
        if list_of_locations is None:
            raise PatternException

        for location in list_of_locations:
            self.add_variable((location, 'FALSE'))
            self.add_guarantee("F(" + location + ")")


class SequencedVisit(CoreMovement):
    """
    Visit a set of locations in sequence, one after the other.
    """

    def __init__(self, name, list_of_locations=None):
        """
        :type list_of_locations: list of location, each location is a boolean
        indicating if the robot is at that location
        """
        super().__init__(name)
        if list_of_locations is None:
            raise PatternException

        guarantee = "F("
        for n, location in enumerate(list_of_locations):
            self.add_variable((location, 'FALSE'))

            guarantee += location
            if n == len(list_of_locations) - 1:
                for _ in range(len(list_of_locations)):
                    guarantee += ")"
            else:
                guarantee += " & F("

        self.add_guarantee(guarantee)


class OrderedVisit(CoreMovement):
    """
    Sequence visit does not forbid to visit a successor location before its predecessor, but only that after the
    predecessor is visited the successor is also visited. Ordered visit forbids a successor to be visited
    before its predecessor.
    """


    def __init__(self, name, list_of_locations=None):
        """
        :type list_of_locations: list of location, each location is a boolean
        indicating if the robot is at that location
        """
        super().__init__(name)
        if list_of_locations is None:
            raise PatternException

        guarantee = "F("
        for n, location in enumerate(list_of_locations):
            self.add_variable((location, 'boolean'))

            guarantee += location
            if n == len(list_of_locations) - 1:
                for _ in range(len(list_of_locations)):
                    guarantee += ")"
            else:
                guarantee += " & F("

        self.add_guarantee(guarantee)

        for n, location in enumerate(list_of_locations):
            if n < len(list_of_locations)-1:
                self.add_guarantee("!" + list_of_locations[n+1] + " U " + list_of_locations[n])


class GlobalAvoidance(Pattern):
    """
    Visit a set of locations in an unspecified order.
    """

    def __init__(self, name, list_of_locations=None):
        """
        :type list_of_locations: list of location, each location is a boolean
        indicating if the robot is at that location
        """
        super().__init__(name)
        if list_of_locations is None:
            raise PatternException

        for location in list_of_locations:
            self.add_variable((location, 'boolean'))
            self.add_guarantee("G(!" + location + ")")


class DelayedReaction(Pattern):
    """
    Delayed Reaction Pattern
    """
    def __init__(self, name, trigger=None, reaction=None):
        """

        :param name:
        :param trigger: variable representing the atomic proposition for the trigger event
        :param reaction: variable representing the atomic proposition for the reaction
        """
        super().__init__(name)
        if trigger is None or reaction is None:
            raise PatternException

        self.add_variable((trigger, 'boolean'))
        self.add_variable((reaction, 'boolean'))

        self.add_guarantee("G(" + trigger + " -> F(" + reaction + "))")