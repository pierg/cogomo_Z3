from src.sat_checks import *
from src.contract import *
from src.cgtgoal import CGTGoal

import copy

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
    """

    :param goals: list of goals to compose
    :param name: name of the new goal
    :param description: description of the new goal
    :return: new goal
    """

    """For each contract pair, checks the consistency of the guarantees among the goals that have common assumptions"""
    for pair_of_goals in itertools.combinations(goals, r=2):
        """Goal_name -> List of Assumptions"""
        assumptions = {}

        """Goal_name -> List of Guarantees"""
        guarantees = {}

        for contract_1 in pair_of_goals[0].get_contracts():

            assumptions[pair_of_goals[0].get_name() + "_assumptions"] = contract_1.get_assumptions()
            guarantees[pair_of_goals[0].get_name() + "_guarantees"] = contract_1.get_guarantees()

            for contract_2 in pair_of_goals[1].get_contracts():

                assumptions[pair_of_goals[1].get_name() + "_assumptions"] = contract_2.get_assumptions()
                guarantees[pair_of_goals[1].get_name() + "_guarantees"] = contract_2.get_guarantees()

                """Checking Consistency only when the assumptions are satisfied together"""
                sat_1, model = sat_check(assumptions)
                if sat_1:
                    """Checking Consistency only when the assumptions are satisfied together"""
                    sat_2, model = sat_check(guarantees)
                    if not sat_2:
                        print("The assumptions in the conjunction of contracts are not mutually exclusive")
                        print("Conflict with the following guarantees:\n" + str(model))
                        raise Exception("Conjunction Failed")

    print("The conjunction satisfiable.")

    # Creating new list of contracts
    list_of_new_contracts = []

    for goal in goals:
        contracts = goal.get_contracts()
        for contract in contracts:
            new_contract = copy.deepcopy(contract)
            list_of_new_contracts.append(new_contract)

    # Creating a new Goal parent
    conjoined_goal = CGTGoal(name=name,
                             description=description,
                             contracts=list_of_new_contracts,
                             sub_goals=goals,
                             sub_operation="CONJUNCTION")

    # Connecting children to the parent
    for goal in goals:
        goal.set_parent(conjoined_goal, "CONJUNCTION")

    return conjoined_goal


def prioritize_goal(first_priority_goal, second_priority_goal):
    """
    Makes the assumption of one goal dependent on the satisfiability of the assumptions of the second goal
    :param first_priority_goal:
    :param second_priority_goal:
    :return: lower priority goal
    """

    stronger_assumptions_list = []

    for contract in first_priority_goal.get_contracts():
        stronger_assumptions_list.append(And(contract.get_assumptions()))

    print(second_priority_goal)

    for contract in second_priority_goal.get_contracts():
        contract.add_assumption(Not(Or(stronger_assumptions_list)))

    print(second_priority_goal)



def propagate_assumptions(abstract_goal, refined_goal):
    """

    :return:
    """
    contracts_refined = refined_goal.get_contracts()
    contracts_abstracted = abstract_goal.get_contracts()

    variables = []

    if len(contracts) > 1:
        assumptions_list = []
        guarantee_list = []
        for contract in contracts:
            variables.append(contract.get_variables())
            assumptions_list.append(contract.get_z3_assumptions())
            guarantee_list.append(contract.get_z3_guarantees())
        assumptions = Or(assumptions_list)
        guarantees = And(guarantee_list)
        return Contract(variables, assumptions, guarantees)
    else:
        variables.append(contracts[0].get_variables())
        assumptions = contracts[0].get_z3_assumptions()
        guarantees = contracts[0].get_z3_guarantees()
        return Contract(variables, assumptions, guarantees)


def refine_goal(abstract_goal, refined_goal):
    """

    :param abstract_goal:
    :param refined_goal:
    :return:
    """

    abstracted_contracts = get_z3_contract(abstract_goal)
    refined_contracts = get_z3_contract(refined_goal)

    if not is_z3_refinement(refined_contracts, abstracted_contracts):
        raise Exception("Incomplete Refinement!")

    print("The refinement has been proven, connecting the goals..")
    refined_goal.set_parent(abstract_goal, "ABSTRACTION")

    abstract_goal.set_refinement(refined_goal)

    print("The goals are now connected with each other")




def get_z3_contract(goal):
    contracts = goal.get_contracts()
    variables = []

    if len(contracts) > 1:
        assumptions_list = []
        guarantee_list = []
        for contract in contracts:
            variables.append(contract.get_variables())
            assumptions_list.append(contract.get_z3_assumptions())
            guarantee_list.append(contract.get_z3_guarantees())
        assumptions = Or(assumptions_list)
        guarantees = And(guarantee_list)
        return Contract(variables, assumptions, guarantees)
    else:
        variables.append(contracts[0].get_variables())
        assumptions = contracts[0].get_z3_assumptions()
        guarantees = contracts[0].get_z3_guarantees()
        return Contract(variables, assumptions, guarantees)


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

    # List of guarantees used to simpolify assumptions, used later for abstraction
    g_elem_list = []
    # Compare each element in a_composition with each element in g_composition
    for a_elem in a_composition:
        for g_elem in g_composition:
            if is_contained_in(a_elem, g_elem):
                print("Simplifying assumption " + str(a_elem))
                a_composition_simplified.remove(a_elem)
                g_elem_list.append(g_elem)

    print(("Assumptions:\n\t\t" + str(a_composition_simplified)))
    print(("Guarantees:\n\n\t\t" + str(g_composition_simplified)))


    composed_contract = Contract(variables=variables,
                                 assumptions=a_composition_simplified,
                                 guarantees=g_composition_simplified)

    return composed_contract


def merge_two_dicts(x, y):
    z = x.copy()
    z.update(y)
    return z
