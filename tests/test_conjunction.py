from src.sat_checks import *
from src.parser import *
from src.operations import *

"""Parse Goals from Structured Text File"""

goals = parse('../input_files/test_conjunction.txt')

goals_2 = parse('../input_files/test_composition.txt')



try:
    goal_conjoined = conjoin_goals(
        [goals["goal_1"], goals["goal_2"]],
        name="goal_conjoined",
        description="description of goal_conjoined")

except Exception:

    goal_conjoined = conjoin_goals(
        [goals["goal_1"], goals["goal_3"]],
        name="goal_conjoined",
        description="description of goal_conjoined")


    print(goal_conjoined)
