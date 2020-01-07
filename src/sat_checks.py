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


def is_set_smaller_or_equal(props_refined, props_abstracted):
    """
    Checks if the conjunction of props_refined is contained in the conjunction of props_abstracted, i.e. prop_2 is a bigger set
    :param props_refined: single proposition or list of propositions
    :param props_abstracted: single proposition or list of propositions
    :return: True if prop_1 is a refinement of prop_2
    """

    if props_abstracted is False:
        return True

    refinement = None
    abstract = None

    """Check Attributes"""
    if isinstance(props_refined, list):
        for elem in props_refined:
            if not isinstance(elem, BoolRef):
                raise Exception("Attribute Error")
            refinement = And(props_refined)
    elif isinstance(props_refined, BoolRef):
        refinement = props_refined

    if isinstance(props_abstracted, list):
        for elem in props_abstracted:
            if not isinstance(elem, BoolRef):
                raise Exception("Attribute Error")
            abstract = And(props_abstracted)
    elif isinstance(props_abstracted, BoolRef):
        abstract = props_abstracted

    result, model = z3_validity_check(Implies(refinement, abstract))

    return result

