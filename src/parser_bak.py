import re
from src.cgtgoal import *

# contract file attributes
TAB_WIDTH = 2
FILE_HEADER_INDENT = 0

CONSTANTS_HEADER_INDENT = 1
CONSTANTS_DATA_INDENT = 2
CGT_HEADER_INDENT = 1
CGT_DATA_INDENT = 2
GOAL_HEADER_INDENT = 1
GOAL_DATA_INDENT = 2

COMMENT_CHAR = '##'
ASSIGNMENT_CHAR = ':='
OPERATORS = '<|>|!=| == | >= | <= | \|\| |&&'

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

    contract = CGTGoal() # contract and check holders

    cgtgoal = CGTGoal()

    goal_dictionary = {}

    constants = {}
    file_header = ''
    goal_header = ''

    with open(specfile, 'r') as ifile:
        for line in ifile:
            line, ntabs = _clean_line(line)

            # skip empty lines
            if not line:
                continue

            # parse file header line
            elif ntabs == FILE_HEADER_INDENT:
                # store previously parsed contract
                if GOAL_HEADER in file_header or ENDGOALS_HEADER in file_header:
                    if contract.is_full():
                        # contract.saturate_guarantees()
                        goal_dictionary[contract.get_name()] = CGTGoal(contract.get_name(), contracts=contract)
                    else:
                        raise Exception("The Goal has Incomplete Parameters")
                # parse file headers
                if CONSTANTS_HEADER in line:
                    file_header = line
                elif GOAL_HEADER in line:
                    if file_header:
                        contract = CGTGoal()
                    file_header = line
                elif CGT_HEADER in line:
                    file_header = line
                else:
                    raise Exception("Unexpected File Header")

            else:

                if CONSTANTS_HEADER in file_header:
                    if ntabs == CONSTANTS_DATA_INDENT:
                        var, init = line.split(ASSIGNMENT_CHAR, 1)
                        constants[var.strip()] = int(init.strip())

                elif GOAL_HEADER in file_header:
                    if ntabs == GOAL_HEADER_INDENT:
                        goal_header = line
                    elif ntabs == GOAL_DATA_INDENT:
                        if GOAL_NAME_HEADER in goal_header:
                            contract.set_name(line.strip())
                            for key, value in constants.items():
                                contract.add_constant((key, value))
                        elif GOAL_DESCRIPTION_HEADER in goal_header:
                            contract.set_description(line.strip())
                        elif CONTRACT_VARIABLES_HEADER in goal_header:
                            var, init = line.split(ASSIGNMENT_CHAR, 1)
                            contract.add_variable((var.strip(), init.strip()))
                        elif CONTRACT_ASSUMPTIONS_HEADER in goal_header:
                            list_of_variables = re.split(OPERATORS, line)
                            list_stripped = []
                            for elem in list_of_variables:
                                list_stripped.append(elem.strip())
                            for variable in list_stripped:
                                regx = re.compile(variable + '\s|' + variable + '$')
                                line = regx.sub("self.variables['" + variable + "']", line)
                            contract.add_assumption(line.strip())
                        elif CONTRACT_GUARANTEES_HEADER in goal_header:
                            list_of_variables = re.split(OPERATORS, line)
                            list_stripped = []
                            for elem in list_of_variables:
                                list_stripped.append(elem.strip())
                            for variable in list_stripped:
                                regx = re.compile(variable + '\s|' + variable + '$')
                                line = regx.sub("self.variables['" + variable + "']", line)
                            contract.add_guarantee(line.strip())
                        else:
                            raise Exception("Unexpected Goal Header")



    print("Loaded Goals:\n\n____________________________________________________________________\n\n")
    for key, value in goal_dictionary.items():
        print(str(value) + "____________________________________________________________________\n\n")
    return goal_dictionary


def _clean_line(line):
    """Returns a comment-free, tab-replaced line with no whitespace and the number of tabs"""
    line = line.split(COMMENT_CHAR, 1)[0] # remove comments
    line = line.replace('\t', ' ' * TAB_WIDTH) # replace tabs with spaces
    return line.strip(), _line_indentation(line)

def _line_indentation(line):
    """Returns the number of indents on a given line"""
    return int((len(line) - len(line.lstrip(' '))) / TAB_WIDTH)
