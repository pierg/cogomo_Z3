from src.sat_checks import *

var_a = {"a": "BOOL"}

var_b = {"b": "BOOL"}

var_x = {"x": "1..100"}

var_y = {"b": "2..10"}


print(is_set_smaller_or_equal(var_x, var_x, "x > 5", "x > 1"))
