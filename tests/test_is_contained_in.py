from src.sat_checks import *


s = Solver()

a = Bool("a")
b = Bool("b")
c = Bool("c")
r = Real("r")


print(is_set_smaller_or_equal(a, [a, b]))

print(is_set_smaller_or_equal([a, b], [a, b]))

print(is_set_smaller_or_equal([a, b], [a]))

print(is_set_smaller_or_equal(r > 5, r > 10))

print(is_set_smaller_or_equal(r > 5, r > 2))