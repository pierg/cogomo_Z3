from src.sat_checks import *


s = Solver()

connection = Bool("connection")
n = Real("n")
tr = Int('tr')
delay = Real("delay")
a_l = Real("a_l")
b = Bool("b")


dictionary_props = {
    "p2": delay == 10 / tr,
    "p3": tr != 0
}

# dictionary_satisfiability_check(dictionary_props)

#
# z3_satisfiability_check([b, Not(b)])
#
# sat_check_simple([b, Not(b)])

# sat_check_simple([delay == 10 / tr, tr !=0, tr == 0])
# sat_check_simple([tr !=0, tr == 0])

# z3_satisfiability_check([delay == 10 / tr, tr != 0])

sat_check(dictionary_props)



# z3_satisfiability_check([delay == 10 / tr,
#                          tr != 0,
#                          n > 5,
#                          n < 3])
#
