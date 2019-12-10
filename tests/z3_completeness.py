from src.sat_checks import *

pedal_1 = Real('pedal_1')
pedal_2 = Real('pedal_2')
cmd = Real('cmd')
error = Bool('error')

# # Top Specification
# top_spec = [Or(cmd > pedal_1, cmd > pedal_2),
#             cmd <= 6.0]
#
# # Incomplete
# spec_1 = [Implies(pedal_1 < 4, cmd == pedal_1 + 1),
#           Implies(pedal_2 < 4, cmd == pedal_2 + 1)]
#
# # Complete
# spec_2 = [If(pedal_1 < 4, cmd == pedal_1 + 1, error),
#           If(pedal_2 < 4, cmd == pedal_2 + 1, error),
#           Implies(error, cmd == cmd + 1)]
#
#
# print(is_contained_in(spec_1, top_spec))
# print(is_contained_in(spec_2, top_spec))
#
#


s = Solver()

x = Real('x')
z = Real('z')

s.assert_and_track(Or(x > 0, z > 100), 'a1')
s.assert_and_track(x < 0, 'a2')
print(s.check())
print(s.unsat_core())