import z3
from src.components import *
from src.operations import *

Delta_m = 1  # meters

velocity_ego_t = Real('velocity_ego_t')  # current speed of the vehicle, at time t
acc_ego = Real('acc_ego')
sig_gps = Bool('sig_gps')
latitude = Real('latitude')
longitude = Real('longitude')
gps_accuracy = Real('gps_accuracy')
position_x = Real('position_x')
sig_radar = Bool('sig_radar')
distance_front = Real('distance_front')  # measured distance
distance_real = Real('distance_real')
radar_accuracy = Real('radar_accuracy')
sig_network = Bool('sig_network')  # network ON
position_network = Real('position_network')

accelerometer = Component(
    id="accelerometer",
    assumptions=[velocity_ego_t > 0],
    guarantees=[acc_ego > 0])

gps_sensor_1 = Component(
    id="gps_sensor_1",
    assumptions=[sig_gps == True],
    guarantees=[latitude > 0, longitude > 0, gps_accuracy == 3])

gps_sensor_2 = Component(
    id="gps_sensor_2",
    assumptions=[sig_gps == True],
    guarantees=[latitude > 0, longitude > 0, gps_accuracy == 2])

gps_sensor_3 = Component(
    id="gps_sensor_3",
    assumptions=[sig_gps == True],
    guarantees=[latitude > 0, longitude > 0, gps_accuracy == 5])

kalman_filter = Component(
    id="kalman_filter",
    assumptions=[acc_ego > 0, latitude > 0, longitude > 0, gps_accuracy > 2],
    guarantees=[position_x > 0])

radar_1 = Component(
    id="radar_1",
    assumptions=[sig_radar == True],
    guarantees=[distance_front > 0, radar_accuracy == 22])

radar_2 = Component(
    id="radar_2",
    assumptions=[sig_radar == True],
    guarantees=[distance_front > 0, radar_accuracy == 18])

radar_3 = Component(
    id="radar_3",
    assumptions=[sig_radar == True],
    guarantees=[distance_front > 0, radar_accuracy == 30])

network = Component(
    id="network",
    assumptions=[sig_network == True],
    guarantees=[position_network > 0])

sensor_fusion = Component(
    id="sensor_fusion",
    assumptions=[position_x > 0, position_network > 0, distance_front > 0, radar_accuracy > 20],
    guarantees=[Implies(distance_front > distance_real, (distance_front - distance_real) < Delta_m),
                Implies(distance_front <= distance_real, (distance_real - distance_front) <= Delta_m)])

list_components = [accelerometer,
                   gps_sensor_1,
                   gps_sensor_2,
                   gps_sensor_3,
                   kalman_filter,
                   radar_1,
                   radar_2,
                   radar_3,
                   network,
                   sensor_fusion]

component_library = ComponentsLibrary(name="cogomo", list_of_components=list_components)

specification = Contract(
    assumptions=[],
    guarantees=[(distance_front > 0),
                Implies(distance_front > distance_real, (distance_front - distance_real) < Delta_m),
                Implies(distance_front <= distance_real, (distance_real - distance_front) <= Delta_m)]
)

components_selection(component_library, specification)
