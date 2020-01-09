from src.sat_checks import *
from src.contract import *
from src.cgtgoal import CGTGoal
from src.components import *
import itertools as it
import operator

import copy


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

    """List of Lists of Contract, 
    each element of the list is a list with the contracts in conjunctions, 
    and each element is in composition with the other elements"""

    contracts_dictionary = {}
    for goal in list_of_goal:
        contracts_dictionary[goal.get_name()] = goal.get_contracts()

    composition_contracts = (dict(list(zip(contracts, x))) for x in it.product(*iter(contracts.values())))

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
    for pair_of_goals in it.combinations(goals, r=2):
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


def components_selection(component_library, specification):
    if not isinstance(component_library, ComponentsLibrary):
        raise Exception("Attribute Error")

    if not isinstance(specification, Contract):
        raise Exception("Attribute Error")

    spec_assumptions = specification.get_assumptions()
    spec_guarantees = specification.get_guarantees()

    set_components_to_return = []

    try:
        candidates_compositions = component_library.extract_selection(spec_assumptions, spec_guarantees)
    except Exception as e:
        print("No refinement possible")
        print(e)
        return []

    first_selected_components = greedy_selection(candidates_compositions)
    print("Selected components " + str([component.get_id() for component in first_selected_components]) + " out of " +
          str(len(candidates_compositions)) + " candidates")

    set_components_to_return.append(first_selected_components)

    components_to_search = first_selected_components.copy()
    component_already_searched = []

    while len(components_to_search) != 0:

        print("Looking for components that refine the assumptions")
        components_to_search_copy = components_to_search.copy()

        for component in components_to_search_copy:

            """Remove component from list of components to search 
            and keep track that it has been searched (avoid loops)"""
            components_to_search.remove(component)
            component_already_searched.append(component)

            component_assumptions = component.get_assumptions()

            """Extract all candidate compositions that can provide the assumptions, if they exists"""
            try:
                candidates_compositions = component_library.extract_selection(spec_assumptions, component_assumptions)
            except Exception as e:
                print(e)
                print("No selection found")
                continue

            """Greedly select one composition"""
            new_selected_components = greedy_selection(candidates_compositions)
            print("Selected components " + str(
                [component.get_id() for component in new_selected_components]) + " out of " +
                  str(len(candidates_compositions)) + " candidates")

            if new_selected_components not in set_components_to_return:
                set_components_to_return.append(new_selected_components)

            """Add components to be searched only if they have not already been searched before"""
            for comp in new_selected_components:
                if comp not in component_already_searched:
                    components_to_search.append(comp)


    """Flattening list of selections and eliminating duplicates"""
    flat_list_refining_components = list(set([item for sublist in set_components_to_return for item in sublist]))

    print(str(len(flat_list_refining_components)) +
          " components found in the library that composed refine the specifications:")

    for n, l in enumerate(set_components_to_return):
        ret = "\t" * n
        for component in l:
            ret += component.get_id() + " "
        print(ret)

    return flat_list_refining_components


def propagate_assumptions(abstract_goal, refined_goal):
    """

    :return:
    """
    contracts_refined = refined_goal.get_contracts()
    contracts_abstracted = abstract_goal.get_contracts()

    if len(contracts_refined) != len(contracts_abstracted):
        raise Exception("Propagating assumptions among goals with different number of conjoined contracts")

    for i, contract in enumerate(contracts_refined):
        """And(.....) of all the assumptions of the abstracted contract"""
        assumptions_abs_z3 = contracts_abstracted[i].get_z3_assumptions()
        """List of all the assumptions of the refined contract"""
        assumptions_ref = contract.get_assumptions()
        assumptions_to_add = []
        for assumption in assumptions_ref:
            if not is_set_smaller_or_equal(assumptions_abs_z3, assumption):
                assumptions_to_add.append(assumption)

        """Unify alphabets"""
        vars = contract.get_variables()
        contracts_abstracted[i].merge_variables(contract.get_variables())
        contracts_abstracted[i].add_assumptions(assumptions_to_add)


def is_a_refinement(refined_contract, abstracted_contract):
    """
    Check if A1 >= A2 and if G1 <= G2
    """

    a_check, model_a = z3_validity_check(Implies(abstracted_contract.get_assumptions()[0],
                                                 refined_contract.get_assumptions()[0]))

    g_check, model_g = z3_validity_check(Implies(refined_contract.get_guarantees()[0],
                                                 abstracted_contract.get_guarantees()[0]))

    if not a_check:
        print("Assumptions are not a valid refinement: " + str(model_a))

    if not g_check:
        print("Guarantees are not a valid refinement")
        print("REFINED:\n" + str(refined_contract.get_guarantees()[0]))
        print("\n\nABSTRACT:\n" + str(abstracted_contract.get_guarantees()[0]))
        print("\n\nCOUNTEREXAMPLE:\n" + str(model_g))

    return a_check and g_check



def is_refinement_correct(refined_contract, abstracted_contract):
    """
    Check if A1 >= A2 and if G1 <= G2
    """

    a_check = is_set_smaller_or_equal(abstracted_contract.get_assumptions(), refined_contract.get_assumptions())

    g_check = is_set_smaller_or_equal(refined_contract.get_guarantees(), abstracted_contract.get_guarantees())

    return a_check and g_check


def refine_goal(abstract_goal, refined_goal):
    """

    :param abstract_goal:
    :param refined_goal:
    :return:
    """

    propagate_assumptions(abstract_goal, refined_goal)

    abstracted_contracts = get_z3_contract(abstract_goal)
    refined_contracts = get_z3_contract(refined_goal)

    if not is_a_refinement(refined_contracts, abstracted_contracts):
        raise Exception("Incomplete Refinement!")

    print("The refinement has been proven, connecting the goals..")
    refined_goal.set_parent(abstract_goal, "ABSTRACTION")

    abstract_goal.set_refinement(refined_goal)

    print("The goals are now connected with each other")


def get_z3_contract(goal):
    contracts = goal.get_contracts()
    variables = {}

    if len(contracts) > 1:
        assumptions_list = []
        guarantee_list = []
        for contract in contracts:
            merge_two_dicts(variables, contract.get_variables())
            assumptions_list.append(contract.get_z3_assumptions())
            guarantee_list.append(contract.get_z3_guarantees())
        assumption = Or(assumptions_list)
        guarantee = And(guarantee_list)
        return Contract(variables, [assumption], [guarantee])
    else:
        merge_two_dicts(variables, contracts[0].get_variables())
        assumption = contracts[0].get_z3_assumptions()
        guarantee = contracts[0].get_z3_guarantees()
        return Contract(variables, [assumption], [guarantee])


def compose_contracts(contracts):
    """
    :param contracts: dictionary of goals name and contract
    :return: True, contract which is the composition of the contracts in the goals or the contracts in the list
             False, unsat core of smt, list of proposition to fix that cause a conflict when composing
    """

    contracts_dictionary = {}
    if isinstance(contracts, dict):
        contracts_dictionary = contracts
    else:
        raise WrongParametersError

    composed_name = ""
    variables = {}
    assumptions = {}
    guarantees = {}

    for name, contract in list(contracts_dictionary.items()):
        composed_name += name + "_"
        merge_two_dicts(variables, contract.get_variables())
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
            if is_set_smaller_or_equal(a_elem, g_elem):
                print("Simplifying assumption " + str(a_elem))
                a_composition_simplified.remove(a_elem)
                g_elem_list.append(g_elem)

    print(("Assumptions:\n\t\t" + str(a_composition_simplified)))
    print(("Guarantees:\n\n\t\t" + str(g_composition_simplified)))

    composed_contract = Contract(variables=variables,
                                 assumptions=a_composition_simplified,
                                 guarantees=g_composition_simplified)

    return composed_contract


def greedy_selection(candidate_compositions):
    """
    Scan all the possible compositions and compute costs for each of them,
    If there are multiple compositions iwth the same cost, pick the more refined one
    (bigger assumptions, smaller guarantees)
    :param: List of List
    """

    """If only one candidate return that one"""
    if len(candidate_compositions) == 1:
        print("\tgreedly seelected the only candidate")
        return candidate_compositions[0]

    best_candidates = []
    lowest_cost = float('inf')

    print("Choosing greedly one composition...")

    for composition in candidate_compositions:
        cost = 0
        for component in composition:
            cost += component.cost()
        if cost < lowest_cost:
            best_candidates.append(composition)
        elif cost == lowest_cost:
            best_candidates.append(composition)

    if len(best_candidates) == 1:
        print("\tgreedly seelected the best candidate based on cost")
        return best_candidates[0]

    else:
        """Keep score of the candidates"""

        """Dict: candidate_id -> points"""
        candidates_points = {}
        for candidate in best_candidates:
            candidates_points[tuple(candidate)] = 0

        print("Generating pairs for all " + str(len(best_candidates)) + " candidates")
        candidate_pairs = it.combinations(best_candidates, 2)

        n_comparisons = 0
        for candidate_a, candidate_b in candidate_pairs:

            contract_a = Contract()
            contract_b = Contract()

            for component_a in candidate_a:
                contract_a.add_assumptions(component_a.get_assumptions())
                contract_a.add_guarantees(component_a.get_guarantees())

            for component_b in candidate_b:
                contract_b.add_assumptions(component_b.get_assumptions())
                contract_b.add_guarantees(component_b.get_guarantees())

            if is_refinement_correct(contract_a, contract_b):
                candidates_points[tuple(candidate_a)] += 1
            else:
                candidates_points[tuple(candidate_b)] += 1

            n_comparisons += 1


        print(str(n_comparisons) + " comparisons have been made")
        """Extract the candidate with the highest score (the most refined)"""
        best_candidate = max(candidates_points.items(), key=operator.itemgetter(1))[0]

        print("\tgreedly seelected the best candidate based on biggest assumption set")
        return list(best_candidate)


def merge_two_dicts(x, y):
    z = x.copy()
    z.update(y)
    return z
