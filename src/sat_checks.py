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


def is_contained_in(prop_1, prop_2):
    """
    Checks if prop_1 is contained in prop_2, i.e. prop_2 is a bigger set
    :param prop_1: single proposition or list of propositions
    :param prop_2: single proposition or list of propositions
    :return: True if prop_1 is a refinement of prop_2
    """

    # convert to list
    if not isinstance(prop_1, list):
        prop_1 = [prop_1]

    if not isinstance(prop_2, list):
        prop_2 = [prop_2]

    if False in prop_2:
        return True

    refinement = And(prop_1)
    abstract = And(prop_2)

    result, model = z3_validity_check(Implies(refinement, abstract))

    return result

