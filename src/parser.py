import re
from src.cgtgoal import *

# contract file attributes
TAB_WIDTH = 2
FILE_HEADER_INDENT = 0

CONSTANTS_HEADER_INDENT = 0
CONSTANTS_DATA_INDENT = 1
GOAL_HEADER_INDENT = 0
GOAL_SUBHEADER_INDENT = 1
GOAL_DATA_INDENT = 2

COMMENT_CHAR = '#'
ASSIGNMENT_CHAR = ':='
OPERATORS = '==|\*|\/|-|<=|>=|<|>|\+|!=|\(|\)'
# OPERATORS = '<|>|!=| == | >= | <= | \|\| |&& | * '
# OPERATORS = '<|>|!=|==|>=|<=|\|&&|*'


CONSTANTS_HEADER = 'CONSTANTS'

GOAL_HEADER = 'GOAL'
ENDGOALS_HEADER = 'ENDGOALS'
GOAL_NAME_HEADER = 'NAME'
GOAL_DESCRIPTION_HEADER = 'DESCRIPTION'
CONTRACT_VARIABLES_HEADER = 'VARIABLES'
CONTRACT_ASSUMPTIONS_HEADER = 'ASSUMPTIONS'
CONTRACT_GUARANTEES_HEADER = 'GUARANTEES'

CGT_HEADER = 'CGT'
CGT_CONJUNCTION_HEADER = 'CONJUNCTION'
CGT_COMPOSITION_HEADER = 'COMPOSITION'
CGT_NAME_HEADER = 'NAME'
CGT_TREE_HEADER = 'TREE'
CGT_END_TREE = 'ENDTREE'
CGT_END_OPERATION = 'ENDTREE|CONJUNCTION|COMPOSITION'


def parse(specfile):
    """Parses the system specification file and returns the contracts and checks

    Args:
        specfile: a string input file name for the system specification file

    Returns:
        A tuple containing a contracts object and a checks object
    """

    cgt_goal = CGTGoal()
    contract = Contract()  # contract and check holders

    goal_dictionary = {}

    constants = {}
    file_header = ''
    goal_header = ''

    with open(specfile, 'r') as ifile:
        for line in ifile:
            line, ntabs = _count_line(line)

            # skip empty lines
            if not line:
                continue

            # parse file header line
            elif ntabs == FILE_HEADER_INDENT:
                # store previously parsed contract
                if GOAL_HEADER in file_header or ENDGOALS_HEADER in file_header:
                    if contract.is_full():
                        # contract.saturate_guarantees()
                        goal_dictionary[cgt_goal.get_name()] = CGTGoal(cgt_goal.get_name(), contracts=contract)
                    else:
                        raise Exception("The Goal has Incomplete Parameters")
                # parse file headers
                if CONSTANTS_HEADER in line:
                    file_header = line
                elif GOAL_HEADER in line:
                    if file_header:
                        cgt_goal = CGTGoal()
                        contract = Contract()
                    file_header = line
                elif CGT_HEADER in line:
                    file_header = line
                else:
                    raise Exception("Unexpected File Header")

            else:

                if CONSTANTS_HEADER in file_header:
                    if ntabs == CONSTANTS_DATA_INDENT:
                        var, init = line.split(ASSIGNMENT_CHAR, 1)
                        if "." in init.strip():
                            constants[var.strip()] = float(init.strip())
                        else:
                            constants[var.strip()] = int(init.strip())

                elif GOAL_HEADER in file_header:
                    if ntabs == GOAL_HEADER_INDENT:
                        goal_header = line
                    elif ntabs == GOAL_SUBHEADER_INDENT:
                        goal_header = line
                    elif ntabs == GOAL_DATA_INDENT:
                        if GOAL_NAME_HEADER in goal_header:
                            cgt_goal.set_name(line.strip())
                            for key, value in constants.items():
                                contract.add_constant((key, value))
                        elif GOAL_DESCRIPTION_HEADER in goal_header:
                            cgt_goal.set_description(line.strip())
                        elif CONTRACT_VARIABLES_HEADER in goal_header:
                            var, init = line.split(ASSIGNMENT_CHAR, 1)
                            contract.add_variable((var.strip(), init.strip()))
                        elif CONTRACT_ASSUMPTIONS_HEADER in goal_header:
                            list_of_variables = re.split(OPERATORS, line)
                            list_stripped = []
                            for elem in list_of_variables:
                                stripped = elem.strip()
                                if stripped is not '' and not _is_string_number(stripped):
                                    list_stripped.append(stripped)
                            for variable in list_stripped:
                                regx = re.compile('\s' + variable + '|' + variable + '\s|' + variable + '$')
                                line = regx.sub("self.variables['" + variable + "']", line)
                            contract.add_assumption(line.strip())
                        elif CONTRACT_GUARANTEES_HEADER in goal_header:
                            list_of_variables = re.split(OPERATORS, line)
                            list_stripped = []
                            for elem in list_of_variables:
                                stripped = elem.strip()
                                if stripped is not '' and not _is_string_number(stripped):
                                    list_stripped.append(stripped)
                            for variable in list_stripped:
                                regx = re.compile('\s' + variable + '|' + variable + '\s|' + variable + '$')
                                line = regx.sub("self.variables['" + variable + "']", line)
                            contract.add_guarantee(line.strip())
                        else:
                            raise Exception("Unexpected Goal Header")

    print("Loaded Goals:\n\n____________________________________________________________________\n\n")
    for key, value in goal_dictionary.items():
        print(str(value) + "____________________________________________________________________\n\n")
    return goal_dictionary


def _is_string_number(string):
    """Returns true if string is a float or int"""
    try:
        int(string)
        return True
    except:
        try:
            float(string)
            return True
        except:
            return False


def _count_line(line):
    """Returns a comment-free, tab-replaced line with no whitespace and the number of tabs"""
    line = line.split(COMMENT_CHAR, 1)[0]  # remove comments
    tab_count = 0
    space_count = 0
    for char in line:
        if char == ' ':
            space_count += 1
        elif char == '\t':
            tab_count += 1
        else:
            break
    tab_count += int(space_count / 4)
    line = line.replace('\t', ' ' * TAB_WIDTH)  # replace tabs with spaces
    return line.strip(), tab_count
