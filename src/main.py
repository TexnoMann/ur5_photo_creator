from libs.ur import *
from libs.cubicInterpolation import *

ip = 192.168.0.67
port = 3004
config filename = "config.xml"
time_delay = 0.002
init_pos = [0.0, -pi/2,0,-pi/2,0.0,0.0]

u5 = UR(ip, port, config_filename, time_delay)
trj_planer = PoseTrjPlaner(2.0);
initPoint = [0.0, -pi/2,0,-pi/2,0.0,0.0]
finalPoint = [0.0, -pi/2, -pi/2,-,0.0,0.0]
trj_planer.poseCubicInterpolation(initPoint, finalPoint, 10.0)


ur5.init(init_pos)
