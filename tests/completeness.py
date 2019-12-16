#!/usr/bin/env python
"""Test Library module provides a test suite for LTL contract verifier"""

import os
import sys

from src.parser import parse
from src.cgtgoal import *

from src.operations import *

sys.path.append(os.path.join(os.getcwd(), os.path.pardir))





if __name__ == "__main__":

    goals = parse('../spec/test_completeness.txt')

    try:
        refine_goal(goals['communicate_with_platoon_leader_abstracted'],
                    goals['communicate_with_platoon_leader_refined'])
    except Exception:
        print("Refinement not complete, Fixing..")

        refine_goal(goals['communicate_with_platoon_leader_abstracted_complete'],
                    goals['communicate_with_platoon_leader_refined_complete'])
        #
        # refine_goal(goals['communicate_with_platoon_leader'], goals['communicate_with_platoon_leader_refined_complete'])




