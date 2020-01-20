from src.sat_checks import *
from src.parser import *
from src.operations import *

"""Parse Goals from Structured Text File"""

goals = parse('../input_files/test_composition.txt')


goal_composed = compose_goals(
    [goals["goal_1"], goals["goal_2"]],
    name="goal_composed",
    description="description of goal_composed")

print(goal_composed)

