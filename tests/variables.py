from src.sat_checks import *

Delta_m = 1  # meters
RSSI_net = 60  # dbm
Epsilon_d = 1
D_platoon = 10  # platooning distance
D_safe = 20  # safety distance

# Variables
velocity_ego_t = Real('velocity_ego_t')    # current speed of the vehicle, at time t
velocity_ego_t1 = Real('velocity_ego_t1')  # speed of the ego vehicle at time t+1
steering_ego = Real('steering_ego')

velocity_lea = Real('velocity_lea')
steering_lea = Real('steering_lea')

distance_front = Real('distance_front')  # measured distance
distance_real = Real('distance_real')

sig_network = Bool('sig_network')  # network ON
connected_platoon = Bool('connected_platoon')
sig_rssi = Real('sig_rssi')
sig_radar = Bool('sig_radar')
sig_gps = Bool('sig_gps')
latitude = Real('latitude')
longitude = Real('longitude')
position_x = Real('position_x')
position_network = Real('position_network')

radar_accuracy = Real('radar_accuracy')
gps_accuracy = Real('gps_accuracy')

ang_gas = Real('ang_gas')
break_req = Real('break_req')
acc_ego = Real('acc_ego')



# Top Specification
top_spec = [Or(cmd > pedal_1, cmd > pedal_2),
            cmd <= 6.0]

# Incomplete
spec_1 = [Implies(pedal_1 < 4, cmd == pedal_1 + 1),
          Implies(pedal_2 < 4, cmd == pedal_2 + 1)]

# Complete
spec_2 = [If(pedal_1 < 4, cmd == pedal_1 + 1, error),
          If(pedal_2 < 4, cmd == pedal_2 + 1, error),
          Implies(error, cmd == cmd + 1)]


print(is_contained_in(spec_1, top_spec))
print(is_contained_in(spec_2, top_spec))

