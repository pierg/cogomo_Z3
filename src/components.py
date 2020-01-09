from src.contract import *
from src.sat_checks import *
import itertools as it




class NoSelectionFound(Exception):
    pass

class Component(Contract):

    def __init__(self,
                 id=None,
                 description=None,
                 variables=None,
                 assumptions=None,
                 guarantees=None):
        super().__init__(assumptions=assumptions,
                         variables=variables,
                         guarantees=guarantees)

        if id is None:
            raise Exception("Attribute Error")
        elif isinstance(id, str):
            self.id = id
        else:
            raise Exception("Attribute Error")

        if description is None:
            self.description = ""
        elif isinstance(description, str):
            self.description = description
        else:
            raise Exception("Attribute Error")

    def get_id(self):
        return self.id

    def __str__(self):
        """Override the print behavior"""
        astr = 'componend id:\t' + self.id + '\n'
        astr += 'assumptions:\t'
        for assumption in self.assumptions:
            astr += str(assumption) + ', '
        astr = astr[:-2] + '\nguarantees:\t'
        for guarantee in self.guarantees:
            astr += str(guarantee) + ', '
        return astr[:-2] + '\n'


class ComponentsLibrary:

    def __init__(self,
                 name=None,
                 list_of_components=None):

        if name is None:
            raise Exception("Attribute Error")
        elif isinstance(name, str):
            self.name = name
        else:
            raise Exception("Attribute Error")

        if list_of_components is None:
            self.list_of_components = []
        elif isinstance(list_of_components, list):
            self.list_of_components = list_of_components
        else:
            raise Exception("Attribute Error")

    def add_component(self, component):
        if isinstance(component, Component):
            self.list_of_components.append(component)
        else:
            raise Exception("Attribute Error")

    def add_components(self, components_list):
        if isinstance(components_list, list):
            for component in components_list:
                self.add_component((component))
        else:
            raise Exception("Attribute Error")


    def get_components(self):
        return self.list_of_components
    
    def extract_selection(self, assumptions, to_be_refined):
        """
        Extract all candidate compositions in the library that once combined refine 'to_be_refined'
        and are consistent with assumptions
        :param assumptions: List of assumptions
        :param to_be_refined: List of propositions
        :return: List
        """

        candidates_for_each_proposition = {}

        for proposition in to_be_refined:

            """Check if any component refine the to_be_refined"""
            for component in self.get_components():

                if is_set_smaller_or_equal(component.get_guarantees(), proposition):

                    """Check Assumptions Consistency"""
                    if len(assumptions) > 0:

                        assumptions = {component.id(): component.get_assumptions(),
                                       "specification": assumptions}

                        satis, model = sat_check(assumptions)

                        """If the contract has compatible assumptions, add it to the list of contracts 
                        that can refine to_be_refined"""
                        if satis:
                            if proposition in candidates_for_each_proposition:
                                candidates_for_each_proposition[proposition].append(component)
                            else:
                                candidates_for_each_proposition[proposition] = [component]
                    else:
                        if proposition in candidates_for_each_proposition:
                            candidates_for_each_proposition[proposition].append(component)
                        else:
                            candidates_for_each_proposition[proposition] = [component]

        """Check that all the propositions of to_be_refined can be refined"""
        if not all(props in candidates_for_each_proposition for props in to_be_refined):
            raise Exception("The specification cannot be refined further with the components in the library")

        """Create candidate compositions, each refining to_be_refined"""
        candidates_compositions = [[value for (key, value) in zip(candidates_for_each_proposition, values)]
                                   for values in it.product(*candidates_for_each_proposition.values())]

        """Eliminate duplicate components (a component might refine mutiple guarantees)"""
        for i, c in enumerate(candidates_compositions):
            c = list(set(c))
            candidates_compositions[i] = c

        """Filter incomposable candidates"""
        candidates_compositions[:] = it.filterfalse(incomposable_check, candidates_compositions)

        print(str(len(candidates_compositions)) + " candidate compositions found:")
        for i, candidate in enumerate(candidates_compositions):
            for component in candidate:
                print(str(component) + "\n")

        return candidates_compositions



def incomposable_check(list_contracts):
    """Return True if the list of contracts is not satisfiable, not compatible or not feasible"""
    if not isinstance(list_contracts, list):
        raise Exception("Wrong Parameter")

    propositions = set([])

    for contract in list_contracts:
        for elem in contract.get_assumptions():
            propositions.add(elem)
        for elem in contract.get_guarantees():
            propositions.add(elem)

    return not sat_check_simple(propositions)