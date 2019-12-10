#!/usr/bin/env python
"""Test Library module provides a test suite for LTL contract verifier"""

import os
import sys

from src.parser import parse
from src.cgtgoal import *

from src.operations import *

sys.path.append(os.path.join(os.getcwd(), os.path.pardir))



def incompatible_goals():
    """Parse Goals from Structured Text File"""

    goals = parse('../spec/incompatible_goals.txt')

    """Declare New Goals that are built on top of existing goals"""

    keep_short_distance = conjoin_goals(
        [goals["accelerate_distance"], goals["decelerate_distance"], goals["maintainspeed_distance"]],
        name="keep_short_distance",
        description="keep a short distance from the vehicle ahead")

    # keep_short_distance = compose_goals(
    #     [goals["accelerate_distance"], goals["decelerate_distance"], goals["maintainspeed_distance"]],
    #     name="keep_short_distance",
    #     description="keep a short distance from the vehicle ahead")



def inconsistent_goals():
    """Parse Goals from Structured Text File"""

    goals = parse('../spec/inconsistent_goals.txt')

    """Declare New Goals that are built on top of existing goals"""

    keep_short_distance = compose_goals(
        [goals["accelerate_follow"], goals["decelerate_distance"]],
        name="keep_short_distance",
        description="keep a short distance from the vehicle ahead")


def priority_goals():
    """Parse Goals from Structured Text File"""

    goals = parse('../spec/priority_goals.txt')

    """Declare New Goals that are built on top of existing goals"""

    keep_short_distance = conjoin_goals(
        [goals["accelerate_follow"], goals["decelerate_distance"]],
        name="keep_short_distance",
        description="keep a short distance from the vehicle ahead")



def conjoing_and_prioritise_goals():
    """Parse Goals from Structured Text File"""

    # Incomposable - Conflict Detected
    goals = parse('../spec/incomposable_goals.txt')

    # Composable
    goals = parse('../spec/composable_goals.txt')


    """Declare New Goals that are built on top of existing goals"""

    keep_short_distance = None
    follow_leader = None

    try:
        keep_short_distance = conjoin_goals(
            [goals["accelerate_distance"], goals["decelerate_distance"], goals["maintainspeed_distance"]],
            name="keep_short_distance",
            description="keep a short distance from the vehicle ahead")

        follow_leader = conjoin_goals(
            [goals["accelerate_follow"], goals["decelerate_follow"], goals["maintainspeed_follow"]],
            name="follow_leader",
            description="follow the leader vehicle by keeping its speed")

        following_mode = conjoin_goals(
            [keep_short_distance, follow_leader],
            name="following_mode",
            description="following mode of the platooning")

    except Exception:
        """Let's prioritize 'keep_short_distance' over 'follow_leader' """

        print("\nPrioritizing goals...")
        prioritize_goal(keep_short_distance, follow_leader)

        print("\nTrying to conjoin again...")
        following_mode = conjoin_goals(
            [keep_short_distance, follow_leader],
            name="following_mode",
            description="following mode of the platooning")


if __name__ == "__main__":

    # incompatible_goals()
    # inconsistent_goals()
    # priority_goals()

    conjoing_and_prioritise_goals()


    print("END")
