import os
import sys

from src.patterns import *
from src.context import *

from src.operations import *

sys.path.append(os.path.join(os.getcwd(), os.path.pardir))

if __name__ == "__main__":

    Collaborate("collaborate", "weight_power > 10")

    """The designer specifies the mission"""
    visit_locations = OrderedVisit("visit_locations_A_B", ("locA", "locB"))
    pickup_object = DelayedReaction("pickup_HI_when_in_A", "locA", "HI_pickup")


    """Adding contextual assumptions relative to location and the lifting the weight"""
    visit_locations.add_physical_assumptions()
    pickup_object.add_variable(("weight_power", "5..15"))
    pickup_object.add_assumption("G (weight_power > 10)")


    """Building  the CGT with the Mission"""
    goals = {}
    goals["visit_locations"] = CGTGoal("visit_locations", contracts=[visit_locations])
    goals["pickup_object"] = CGTGoal("pickup_object", contracts=[pickup_object])

    goals["mission"] = compose_goals([goals["visit_locations"], goals["pickup_object"]])

    print(goals["mission"])

    """Istanciating a Library of Componenents"""
    component_library = ComponentsLibrary(name="robots")
    component_library.add_components(
        [
            Robot("robot_1", "weight_power > 5 & weight_power < 10"),
            Robot("robot_2", "weight_power > 5 & weight_power < 10"),
            Robot("robot_3", "weight_power > 7 & weight_power < 10"),
            Collaborate("collaborate", "weight_power > 10")
        ])

    specification = Contract(variables={"weight_power": "0..100"}, guarantees=["weight_power > 10"])

    components_selection(component_library, specification)


    robot_1 = Robot("robot_1", "weight_power > 5 & weight_power < 10")
    goals["robot_1"] = CGTGoal("robot_1", contracts=[robot_1])

    goals["mission"] = compose_goals([goals["mission"], goals["robot_1"]])

    print(goals["mission"])

