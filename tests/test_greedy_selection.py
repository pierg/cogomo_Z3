from src.operations import *
import time

component_library = ComponentsLibrary(name="cogomo")

p0 = Bool('p0')
p1 = Bool('p1')
p2 = Bool('p2')
p3 = Bool('p3')
p4 = Bool('p4')
p5 = Bool('p5')

c0 = Component(id="c0", assumptions=[p0 == True], guarantees=[p3 == True])
c1 = Component(id="c1", assumptions=[p3 == True], guarantees=[p2 == True])
c2 = Component(id="c2", assumptions=[p4 == True], guarantees=[p5 == True])
c3 = Component(id="c3", assumptions=[p5 == True], guarantees=[p2 == True])

list_of_candidates = [[c0, c1], [c2, c3]]

if __name__ == '__main__':
    greedy_selection(list_of_candidates)
