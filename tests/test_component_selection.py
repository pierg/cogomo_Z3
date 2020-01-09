from src.operations import *
import time

component_library = ComponentsLibrary(name="cogomo")

p0 = Bool('p0')
p1 = Bool('p1')
p2 = Bool('p2')
p3 = Bool('p3')
p4 = Bool('p4')

component_library.add_components(
    [
        Component(id="c0", assumptions=[p0 == True], guarantees=[p1 == True]),
        Component(id="c1", assumptions=[p3 == True], guarantees=[p2 == True]),
        Component(id="c2", assumptions=[p2 == True], guarantees=[p3 == True]),
        Component(id="c3", assumptions=[p3 == True], guarantees=[p4 == True])
    ])

spec_a = []
spec_g = [p4 == True]

specification = Contract(assumptions=spec_a, guarantees=spec_g)


def run_2_4():
    start_time = time.time()
    components_selection(component_library, specification)
    elapsed_time = time.time() - start_time
    return elapsed_time


if __name__ == '__main__':
    run_2_4()
