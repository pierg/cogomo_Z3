from src.sat_checks import *


# s = Solver()
#
# L = 5000
# d = Real('d')
# x = Int('x')
# z = Real('z')
#
# s.assert_and_track(d == x * L, 'a2')
# print(s.check())
# print(s.unsat_core())


# distance_front = Real('distance_front')  # measured distance
#
#
# s = Solver()
#
# s.assert_and_track("example:", Not(Or(distance_front>0,)))
#
#
# satis = s.check()
# if str(satis) == "sat":
#     print(s.model())
# else:
#     print(s.unsat_core())

#
# pedal_1 = Real('pedal_1')
# pedal_2 = Real('pedal_2')
# cmd = Real('cmd')
# error = Bool('error')
#
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
#           Implies(Not(error), cmd == cmd + 1)]
#
#
# print(is_contained_in(spec_1, top_spec))
# print(is_contained_in(spec_2, top_spec))
#
#
# print("\n\n____\n\n")
#

# Transmission rate 3 - 27 Mbps
tr_min = 3000000
tr_max = 27000000
tr = Real('tr')

L = 3200

n = Int('n')

delay = Real('delay') # maximum tolerable transmission delay


a_top = And(tr <= tr_max, tr >= tr_min, tr != 0, n < 5)
a_ref = And(tr <= tr_max, tr >= tr_min, tr != 0, n < 5)

# g_top = [Implies(And(tr <= tr_max, tr >= tr_min, tr != 0, n < 5), delay < 0.01)]
# g_ref = [Implies(And(tr <= tr_max, tr >= tr_min, tr != 0, n < 5),  delay == L * n / tr)]


g_top = [delay < 0.01]
g_ref = [tr != 0, tr <= tr_max, tr >= tr_min, n<5,  delay == L * n / tr]



# # Complete
# s2 = [If(pedal_1 < 4, cmd == pedal_1 + 1, error),
#           If(pedal_2 < 4, cmd == pedal_2 + 1, error),
#           Implies(error, cmd == cmd + 1)]


# print(is_contained_in(a_top, a_ref)


# print(is_contained_in(And(n > 5, tr > 4), tr > 3))


# print(is_contained_in(g_ref, g_top))

# print(is_contained_in(s2, top))



