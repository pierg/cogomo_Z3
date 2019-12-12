#!/usr/bin/env python
"""Test Library module provides a test suite for LTL contract verifier"""

import os
import sys

from src.parser import parse
from src.cgtgoal import *

from src.operations import *

sys.path.append(os.path.join(os.getcwd(), os.path.pardir))

if __name__ == "__main__":
    """Parse Goals from Structured Text File"""

    goals = parse('./spec/platooning.txt')

    """Declare New Goals that are built on top of existing goals"""
    keep_short_distance = None
    follow_leader = None
    speed_control = None

    try:
        keep_short_distance = conjoin_goals(
            [goals["accelerate_distance"], goals["decelerate_distance"], goals["maintainspeed_distance"]],
            name="keep_short_distance",
            description="keep a short distance from the vehicle ahead")

        follow_leader = conjoin_goals(
            [goals["accelerate_follow"], goals["decelerate_follow"], goals["maintainspeed_follow"]],
            name="follow_leader",
            description="follow the leader vehicle by keeping its speed")

        speed_control = conjoin_goals(
            [keep_short_distance, follow_leader],
            name="speed_control",
            description="control the speed of the vehicle based either on the distance to the vehicle in front "
                        "or according the the leader of the platoon")

        print("CGT BEFORE PRIORITY")
        print(speed_control)

    except Exception:
        """Let's prioritize 'keep_short_distance' over 'follow_leader' """

        print("\nPrioritizing goals...")
        prioritize_goal(keep_short_distance, follow_leader)

        print("\nTrying to conjoin again...")
        speed_control = conjoin_goals(
            [keep_short_distance, follow_leader],
            name="speed_control",
            description="control the speed of the vehicle based either on the distance to the vehicle in front "
                        "or according the the leader of the platoon")

        print("CGT AFTER PRIORITY")
        print(speed_control)

    following_mode = compose_goals(
        [speed_control, goals["communication_leader"]],
        name="following_communication",
        description="followin mode of the platoon"
    )

    print("END")
