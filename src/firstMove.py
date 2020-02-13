import sys
import logging
from copy import deepcopy
from time import *
from math import pi, sin


#Initializing RTDE lib
import libs.rtde.rtde as rtde
import libs.rtde.rtde_config as rtde_config
import libs.rtde.csv_writer as csv_writer
import libs.rtde.csv_reader as csv_reader
#from kinCheck import *

#Initializing connection properties
ROBOT_HOST = '192.168.88.6'
ROBOT_PORT = 30004
config_filename = "config.xml"
trj_filename = "traektorys.csv"
out_data_filename = "data.csv"
# trj_file=open(trj_filename,"r")
out_file=open(out_data_filename,"w")

DELAY=0.002
run=False


log=logging.getLogger()
log.setLevel(logging.INFO)
gentime=0
finalTime=60*10^3
q=[]
i=0
while(gentime<finalTime):
    q.append([0.5*sin(gentime),-pi/2,0,-pi/2,0,0])
    gentime+=DELAY





#Init function for writing ang moving:

def check_position(list_of_state,list_of_sets):
    E=0.0001
    count=0
    assert(len(list_of_state)==len(list_of_sets)),"Error parameters for trajectory"
    for i in range(0,len(list_of_state)):
        if abs(list_of_state[i]-list_of_sets[i])<=E:
            count+=1;
    if count==6:
        return True
    else:
        return False

def state_to_poslist(state):
    list = state.__dict__["actual_q"]
    return deepcopy(list)


def sets_to_list(sets):
    list = []
    for i in range(0,6):
        list.append(sets.__dict__["input_double_register_%i" % i])
    return list

def write_list_in_sets(sets, list):
    for i in range (0,6):
        sets.__dict__["input_double_register_%i" % i] = list[i]
    return sets

def goToStartPoint(startPoint,sets, watchdog, run, DELAY, connection):
    state=connection.receive()
    list=state_to_poslist(state);
    print(list)
    firsttime=time();
    while(run):
        try:
            print("firstTime1: ",str(time()-firsttime))
            state=connection.receive()

            #print(state_to_poslist(state))
            if state is None:
                run=False
            if check_position(state_to_poslist(state),startPoint):
                break
            if state.output_int_register_0!=0:
                print("secondTime: ",str(time()-firsttime))
                sets=write_list_in_sets(sets, startPoint)
                connection.send(sets)
            connection.send(watchdog)
        except KeyboardInterrupt:
            print("Stop!")
            run=False

def moveTrj(trjList, sets, watchdog, run, DELAY, connection):
    firsttime=time();
    for i in range(0,len(trjList)):
        if not run:
            break
        try:
            state=connection.receive()
            if state is None:
                run=False
            writer.writerow(state)
            if state.output_int_register_0!=0:
                sets=write_list_in_sets(sets, trjList[i])
                connection.send(sets)
            connection.send(watchdog)
        except KeyboardInterrupt:
            print("Stop!")
            run=False
            sys.exit()


#Initializing config file, output and input recipes

conf=rtde_config.ConfigFile(config_filename)
state_names, state_types = conf.get_recipe('state')
sets_names, sets_types = conf.get_recipe('sets')
watchdog_names, watchdog_types = conf.get_recipe('watchdog')


#Open csv reader and writer
writer = csv_writer.CSVWriter(out_file, state_names, state_types)
writer.writeheader()

# reader=csv_reader.CSVReader(trj_file, delimiter = ',')

# trajectory=[]
# for i in range(0,len(reader.target_q_1)):
#     trajectory.append([reader.target_q_1[i], reader.target_q_2[i], reader.target_q_3[i], reader.target_q_4[i], reader.target_q_5[i], reader.target_q_6[i]])
trajectory = q

logging.info("Start connection to UR10")

#Connect to UR10 :)
connection=rtde.RTDE(ROBOT_HOST, ROBOT_PORT)
connection.connect()

#Print version controller
connection.get_controller_version()

#Send settings for input and output and wathdog
connection.send_output_setup(state_names, state_types)
sets = connection.send_input_setup(sets_names, sets_types)
watchdog = connection.send_input_setup(watchdog_names, watchdog_types)

#Format registers
sets.input_double_register_0 = trajectory[0][0]
sets.input_double_register_1 = trajectory[0][1]
sets.input_double_register_2 = trajectory[0][2]
sets.input_double_register_3 = trajectory[0][3]
sets.input_double_register_4 = trajectory[0][4]
sets.input_double_register_5 = trajectory[0][5]

watchdog.input_int_register_0 = 0

#Send connection-message on robot
if not connection.send_start():
    sys.exit()

#check trajectory
# if checkTrajectory(trajectory) is None:
#     sys.exit()

connection.send(sets)

#Go my litle Ur10:)
run=True
goToStartPoint(trajectory[0],sets, watchdog, run, DELAY, connection)
moveTrj(trajectory,sets, watchdog, run, DELAY, connection)



connection.send_pause()
connection.disconnect()
