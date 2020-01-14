#!/usr/bin/env python
"""Test Library module provides a test suite for LTL contract verifier"""

import os
import sys

from src.parser import parse
from src.cgtgoal import *

from src.operations import *

sys.path.append(os.path.join(os.getcwd(), os.path.pardir))


def case1():
    goals = parse('../input_files/test_completeness.txt')

    try:
        refine_goal(goals['communicate_with_platoon_leader_abstracted'],
                    goals['communicate_with_platoon_leader_refined'])
    except Exception:
        print("Refinement not complete, Fixing..")

        refine_goal(goals['communicate_with_platoon_leader_abstracted_complete'],
                    goals['communicate_with_platoon_leader_refined_complete'])

        print(goals['communicate_with_platoon_leader_abstracted_complete'])
        print(goals['communicate_with_platoon_leader_refined_complete'])

def case2():
    goals = parse('../input_files/decomposition.txt')

    try:
        communicate_with_platoon_leader_refined = compose_goals([
            goals['enstablish_connection'],
            goals['enstablish_connection']], "communicate_with_platoon_leader_refined")

        refine_goal(goals['communicate_with_platoon_leader'],
                    communicate_with_platoon_leader_refined)

    except Exception:
        print("Refinement not complete, Fixing..")

        refine_goal(goals['communicate_with_platoon_leader_abstracted_complete'],
                    goals['communicate_with_platoon_leader_refined_complete'])




if __name__ == "__main__":

    goals = parse('../input_files/decomposition.txt')

    try:
        communicate_with_platoon_leader_refined = compose_goals([
            goals['enstablish_connection'],
            goals['retrieve_information']], "communicate_with_platoon_leader_refined")

        refine_goal(goals['communicate_with_platoon_leader'],
                    communicate_with_platoon_leader_refined)

    except Exception:
        print("Exception occurred")
        print("Fixing the assumptions..")

        communicate_with_platoon_leader_refined = compose_goals([
            goals['enstablish_connection_fixed'],
            goals['retrieve_information']], "communicate_with_platoon_leader_refined")

        refine_goal(goals['communicate_with_platoon_leader'],
                    communicate_with_platoon_leader_refined)



