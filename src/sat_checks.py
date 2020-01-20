import re
import subprocess

smvfile = "nusmvfile.smv"


def And(list_propoositions):
    """Returns a string representing the logical AND of list_propoositions"""
    if len(list_propoositions) > 1:
        ret = ""
        for i, elem in enumerate(list_propoositions):
            ret += elem
            if i < len(list_propoositions) - 1:
                ret += " & "
        return ret
    else:
        return list_propoositions[0]


def Or(list_propoositions):
    """Returns a string representing the logical OR of list_propoositions"""
    if len(list_propoositions) > 1:
        ret = "("
        for i, elem in enumerate(list_propoositions):
            ret += elem
            if i < len(list_propoositions) - 1:
                ret += " | "
        ret += ")"
        return ret
    else:
        return list_propoositions[0]


def Implies(prop_1, prop_2):
    """Returns a string representing the logical IMPLIES of prop_1 and prop_2"""
    return '(' + prop_1 + ' -> ' + prop_2 + ')'


def Not(prop):
    """Returns a string representing the logical NOT of prop"""
    return '! (' + prop + ')'


def check_satisfiability(variables, propositions):

    propositions_copy = propositions.copy()

    for index, prop in enumerate(propositions_copy):
        """Renaming propositions"""
        propositions_copy[index] = re.sub("_port_\d+", "", prop)

    """Write the NuSMV file"""
    with open(smvfile, 'w') as ofile:

        # write module heading declaration
        ofile.write('MODULE main\n')

        # write variable type declarations
        ofile.write('VAR\n')
        for name, type in variables.items():
            ofile.write('\t' + name + ': ' + type + ';\n')

        ofile.write('\n')

        ofile.write('LTLSPEC ')

        ofile.write(Not(And(propositions_copy)))

        ofile.write('\n')

    output = subprocess.check_output(['NuSMV', smvfile], encoding='UTF-8').splitlines()

    output = [x for x in output if not (x[:3] == '***' or x[:7] == 'WARNING' or x == '')]

    for line in output:

        if line[:16] == '-- specification':
            if 'is false' in line:
                return True
            elif 'is true' in line:
                return False


def check_validity(variables, proposition):

    """Renaming propositions"""
    proposition_copy = re.sub("_port_\d+", "", proposition)

    """Write the NuSMV file"""
    with open(smvfile, 'w') as ofile:

        # write module heading declaration
        ofile.write('MODULE main\n')

        # write variable type declarations
        ofile.write('VAR\n')
        for name, type in variables.items():
            ofile.write('\t' + name + ': ' + type + ';\n')

        ofile.write('\n')

        ofile.write('LTLSPEC ' + proposition_copy)

    output = subprocess.check_output(['NuSMV', smvfile], encoding='UTF-8').splitlines()

    output = [x for x in output if not (x[:3] == '***' or x[:7] == 'WARNING' or x == '')]

    for line in output:

        if line[:16] == '-- specification':
            if 'is false' in line:
                return False
            elif 'is true' in line:
                return True


def check_ports_are_compatible(prop_1_names, prop_2_names):
    """Returns True if the two propositions or list of propositions share at least one port (variable)"""

    if not isinstance(prop_1_names, list):
        prop_1_names = [prop_1_names]

    if not isinstance(prop_2_names, list):
        prop_2_names = [prop_2_names]

    for var_names_1 in prop_1_names:
        for var_names_2 in prop_2_names:
            if var_names_1 == var_names_2:
                return True
    return False


def is_set_smaller_or_equal(variables_refined, variables_abstracted, props_refined, props_abstracted):
    """
    Checks if the conjunction of props_refined is contained in the conjunction of props_abstracted, i.e. prop_2 is a bigger set
    :param props_refined: single proposition or list of propositions
    :param props_abstracted: single proposition or list of propositions
    :return: True if prop_1 is a refinement of prop_2
    """

    if props_abstracted is False:
        return True

    if check_ports_are_compatible(list(variables_refined.keys()), list(variables_abstracted.keys())) is False:
        return False

    refinement = None
    abstract = None

    """Check Attributes"""
    if isinstance(props_refined, list):
        if len(props_refined) == 1:
            refinement = props_refined[0]
        else:
            refinement = And(props_refined)
    elif isinstance(props_refined, str):
        refinement = props_refined

    if isinstance(props_abstracted, list):
        if len(props_abstracted) == 1:
            abstract = props_abstracted[0]
        else:
            abstract = And(props_abstracted)
    elif isinstance(props_abstracted, str):
        abstract = props_abstracted

    result = check_validity(merge_two_dicts(variables_abstracted, variables_refined), Implies(refinement, abstract))

    if result:
        print("\t\t\trefined:\t" + str(refinement) + "\n\t\t\tabstract:\t" + str(abstract))

    return result


def merge_two_dicts(x, y):
    z = x.copy()
    z.update(y)
    return z
