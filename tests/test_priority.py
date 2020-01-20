from src.sat_checks import *
from src.parser import *
from src.operations import *

"""Parse Goals from Structured Text File"""

goals = parse('../input_files/test_conjunction.txt')


try:
    goal_conjoined = conjoin_goals(
        [goals["goal_1"], goals["goal_2"]],
        name="goal_conjoined",
        description="description of goal_conjoined")

except Exception:
    """Let's prioritize 'goal_1' over 'goal_2' """

    print("\nPrioritizing goals...")
    goal_1 = goals["goal_1"]
    goal_2 = goals["goal_2"]
    prioritize_goal(goal_1, goal_2)

    print("\nTrying to conjoin again...")
    goal_conjoined = conjoin_goals([goal_1, goal_2])

    print(goal_conjoined)
