import re

from z3 import *


def sat_check(propositions_dictionary):
    """Check the satisfiability of the keys of the dictionary passed
    If satisfiabile it returns True and an assignment example
    If insatisfiabile it returns False and the list of elements generating the insatisfiability (unsat_core)"""

    s = Optimize()

    for name, value in list(propositions_dictionary.items()):
        if isinstance(value, list):
            for elem in value:
                prop_strign = name + ": " + str(elem)
                s.assert_and_track(elem, Bool(prop_strign))
        else:
            prop_strign = name + ": " + str(value)
            s.assert_and_track(value, Bool(prop_strign))

    r = s.check()

    if r == sat:
        # print("The formula is satisfiable")
        return True, s.model()
    elif r == unknown:
        print("Failed to prove")
        print((s.model()))
        raise Exception("Failed to prove")
    else:
        # print("The formula is unsatisfiable")
        return False, s.unsat_core()


def sat_check_simple(list_propositions):
    s = Optimize()

    for prop in list_propositions:
        s.add(prop)

    r = s.check()

    if r == sat:
        return True
    elif r == unknown:
        print("Failed to prove")
        print((s.model()))
        raise Exception("Failed to prove")
    else:
        return False


def z3_validity_check(z3_formula):
    s = Solver()

    s.add(Not(z3_formula))

    r = s.check()

    if r == unsat:
        # print("the formula is proven, no counterexample found")
        return True, None
    elif r == unknown:
        # print("failed to prove")
        # print((s.model()))
        raise Exception("failed to prove")
    else:
        # print("counterexample")
        # print((s.model()))
        return False, s.model()


def check_ports_are_compatible(prop_1, prop_2):
    """Returns True if the two propositions or list of propositions share at least one port (variable)"""

    prop_1_names = []
    prop_2_names = []

    if isinstance(prop_1, BoolRef):
        prop_1 = [prop_1]
    if isinstance(prop_2, BoolRef):
        prop_2 = [prop_2]

    for elem in prop_1:
        if not isinstance(elem, BoolRef):
            raise Exception("Attribute Error")

        list_var = re.split('(?<![A-Za-z0-9.])[0-9.]+|[\s\W]|(?<![\w\d])True(?![\w\d])|(?<![\w\d])False(?![\w\d])', str(elem))

        for var in list_var:
            stripped = var.strip()
            if stripped is not '':
                prop_1_names.append(stripped)

    for elem in prop_2:
        if not isinstance(elem, BoolRef):
            raise Exception("Attribute Error")

        list_var = re.split('(?<![A-Za-z0-9.])[0-9.]+|[\s\W]|(?<![\w\d])True(?![\w\d])|(?<![\w\d])False(?![\w\d])', str(elem))

        for var in list_var:
            stripped = var.strip()
            if stripped is not '':
                prop_2_names.append(stripped)

    for var_names_1 in prop_1_names:
        for var_names_2 in prop_2_names:
            if var_names_1 == var_names_2:
                return True

    return False

def is_set_smaller_or_equal(props_refined, props_abstracted):
    """
    Checks if the conjunction of props_refined is contained in the conjunction of props_abstracted, i.e. prop_2 is a bigger set
    :param props_refined: single proposition or list of propositions
    :param props_abstracted: single proposition or list of propositions
    :return: True if prop_1 is a refinement of prop_2
    """

    if props_abstracted is False:
        return True

    if check_ports_are_compatible(props_refined, props_abstracted) is False:
        return False

    refinement = None
    abstract = None


    """Check Attributes"""
    if isinstance(props_refined, list):
        if len(props_refined) == 1:
            refinement = props_refined[0]
        else:
            refinement = And(props_refined)
    elif isinstance(props_refined, BoolRef):
        refinement = props_refined

    if isinstance(props_abstracted, list):
        if len(props_abstracted) == 1:
            abstract = props_abstracted[0]
        else:
            abstract = And(props_abstracted)
    elif isinstance(props_abstracted, BoolRef):
        abstract = props_abstracted

    print("\t\t\trefined:\t" + str(refinement) + "\n\t\t\tabstract:\t" + str(abstract))

    result, model = z3_validity_check(Implies(refinement, abstract))

    print("\t\t\t" + str(result))

    return result

