from src.cgtgoal import CGTGoal
from src.sat_checks import *
from src.contract import *

import itertools


class WrongParametersError(Exception):
    """
    raised if the parameters passed are wrong
    """
    pass


def compose_goals(list_of_goal, name=None, description=""):
    """

    :param name: Name of the goal
    :param contracts: List of contracts to compose
    :return: True, composed_goals if successful
    """

    contracts = {}

    for goal in list_of_goal:
        contracts[goal.get_name()] = goal.get_contracts()

    if name is None:
        name = '_'.join("{!s}".format(key) for (key, val) in list(contracts.items()))

    composition_contracts = (dict(list(zip(contracts, x))) for x in itertools.product(*iter(contracts.values())))

    composed_contract_list = []
    for contracts in composition_contracts:
        composed_contract = compose_contracts(contracts)
        composed_contract_list.append(composed_contract)


    composed_goal = CGTGoal(name=name,
                            description=description,
                            contracts=composed_contract_list,
                            sub_goals=list_of_goal,
                            sub_operation="COMPOSITION")

    # Connecting children to the parent
    for goal in list_of_goal:
        goal.set_parent(composed_goal, "COMPOSITION")

    return composed_goal


def conjoin_goals(goals, name="", description=""):

    conjoined_contracts = []

    for goal in goals:
        conjoined_contracts.append(goal.get_contracts())

    # Flattening list
    conjoined_contracts = [item for sublist in conjoined_contracts for item in sublist]

    conjoined_contract = conjoin_contracts(conjoined_contracts)

    # Creating a new Goal parent
    conjoined_goal = CGTGoal(name=name,
                             description=description,
                             contracts=conjoined_contracts,
                             sub_goals=goals,
                             sub_operation="CONJUNCTION")

    conjoined_goal.set_assumptions(Or())

    # Connecting children to the parent
    for goal in goals:
        goal.set_parent(conjoined_goal, "CONJUNCTION")

    return conjoined_goal


def prioritize_goal(first_priority, second_priority):
    """
    Makes the assumption of one goal dependent on the satisfiability of the assumptions of the second goal
    :param first_priority:
    :param second_priority:
    :return: lower priority goal
    """
    stronger_assumptions = first_priority.get_assumptions()
    negated_stronger_assumptions = Not(And(stronger_assumptions))
    second_priority.add_assumption(negated_stronger_assumptions)




def compose_contracts(contracts):
    """
    :param contracts: dictionary of goals or list of contracts to compose
    :return: True, contract which is the composition of the contracts in the goals or the contracts in the list
             False, unsat core of smt, list of proposition to fix that cause a conflict when composing
    """

    contracts_dictionary = {}
    # Transform list into a dictionary contract-name -> proposition
    if isinstance(contracts, list):
        for contract in contracts:
            contracts_dictionary[contract.get_name()] = contract
    elif isinstance(contracts, dict):
        contracts_dictionary = contracts
    else:
        raise WrongParametersError

    composed_name = ""
    variables = []
    assumptions = {}
    guarantees = {}

    for name, contract in list(contracts_dictionary.items()):
        composed_name += name + "_"
        variables.append(contract.get_variables())
        assumptions[name + "_assumptions"] = contract.get_assumptions()
        guarantees[name + "_guarantees"] = contract.get_guarantees()

    # CHECK COMPATILITY
    satis, model = sat_check(assumptions)
    if not satis:
        print(("Fix the following assumptions:\n" + str(model)))
        raise Exception("The composition is uncompatible")

    # CHECK CONSISTENCY
    satis, model = sat_check(guarantees)
    if not satis:
        print(("Fix the following guarantees:\n" + str(model)))
        raise Exception("The composition is inconsistent")

    # CHECK SATISFIABILITY
    satis, model = sat_check(merge_two_dicts(assumptions, guarantees))
    if not satis:
        print(("Fix the following conditions:\n" + str(model)))
        raise Exception("The composition is unsatisfiable")

    print("The composition is compatible, consistent and satisfiable. Composing now...")

    a_composition = list(assumptions.values())
    g_composition = list(guarantees.values())

    # Flatting the lists
    a_composition = [item for sublist in a_composition for item in sublist]
    g_composition = [item for sublist in g_composition for item in sublist]

    # Eliminating duplicates of assertions
    a_composition = list(dict.fromkeys(a_composition))
    g_composition = list(dict.fromkeys(g_composition))

    a_composition_simplified = a_composition[:]
    g_composition_simplified = g_composition[:]

    print(("Assumptions:\n\t\t" + str(a_composition_simplified)))
    print(("Guarantees:\n\n\t\t" + str(g_composition_simplified)))


    # List of guarantees used to simpolify assumptions, used later for abstraction
    g_elem_list = []
    # Compare each element in a_composition with each element in g_composition
    for a_elem in a_composition:
        for g_elem in g_composition:
            if is_contained_in(a_elem, g_elem):
                print(("Simplifying assumption " + str(a_elem)))
                a_composition_simplified.remove(a_elem)
                g_elem_list.append(g_elem)
                # g_composition_simplified.remove(g_elem)

    # Check for contract abstractions to be adjusted
    for guarantee in g_elem_list:
        for contract in list(contracts_dictionary.values()):
            if contract.is_abstracted():
                contract.abstract_guarantee_if_exists(guarantee)


    # Build the abstracted contract if there are other abstracted contracts
    if abstracted_contracts:
        g_composition = list(abstracted_guarantees.values())
        g_composition = [item for sublist in g_composition for item in sublist]
        g_composition = list(dict.fromkeys(g_composition))

        print(("Abstracted Guarantees:\n\n\t\t" + str(g_composition)))

        return True, Contract(a_composition_simplified, g_composition_simplified,
                              abstract_guarantees=g_composition)

    # Check for guarantee abstraction demanded by the designer
    if abstract_on_guarantees is not None:
        # Check the guarantees are an abstraction of the actual guarantees
        if is_contained_in(g_composition_simplified, abstract_on_guarantees):
            return True, Contract(a_composition_simplified, g_composition_simplified,
                                  abstract_guarantees=abstract_on_guarantees)
        else:
            raise AbstractionError


    composed_contract = Contract(name=composed_name,
                                 variables=variables,
                                 assumptions=a_composition_simplified,
                                 guarantees=g_composition_simplified)

    return True, composed_contract


def conjoin_contracts(contracts):

    contracts_dictionary = {}
    # Transform list into a dictionary contract-name -> proposition
    if isinstance(contracts, list):
        for contract in contracts:
            contracts_dictionary[contract.get_name()] = contract
    elif isinstance(contracts, dict):
        contracts_dictionary = contracts
    else:
        raise WrongParametersError

    for pair_contract in itertools.combinations(contracts, r=2):

        assumptions = {}
        guarantees = {}

        for contract in pair_contract:
            assumptions[contract.get_name() + "_assumptions"] = contract.get_assumptions()
            guarantees[contract.get_name() + "_guarantees"] = contract.get_guarantees()

        # Check if assumptions are not mutually exclusive
        sat_1, model = sat_check(assumptions)
        if sat_1:
            sat_2, model = sat_check(guarantees)
            if not sat_2:
                print("The assumptions in the conjunction of contracts are not mutually exclusive")
                print("Conflict with the following guarantees:\n" + str(model))
                raise Exception("Conjunction Failed")

    print("The conjunction satisfiable.")

    # assumptions = {}
    # guarantees = {}
    #
    # for source_goal, propositions in list(contracts_dictionary.items()):
    #     assumptions[source_goal + "_assumptions"] = propositions.get_assumptions()
    #     guarantees[source_goal + "_guarantees"] = propositions.get_guarantees()

    # new_contract = Contract()

    return True




def merge_two_dicts(x, y):
    z = x.copy()
    z.update(y)
    return z
