import sys
from copy import deepcopy
from time import *
from math import pi, sin


#Initializing RTDE lib
import libs.rtde.rtde as rtde
import libs.rtde.rtde_config as rtde_config


class UR:
    def __init__(self,ip, port, config_filename, time_delay):
        self.__ip = ip
        self.__port = port
        self.__config_filename = config_filename
        self.__time_delay = time_delay
        self.__conf = rtde_config.ConfigFile(self.__config_filename)
        self.__state_names, self.__state_types = self.__conf.get_recipe('state')
        self.__sets_names, self.__sets_types = self.__conf.get_recipe('sets')
        self.__watchdog_names, self.__watchdog_types = self.__conf.get_recipe('watchdog')

    def init(self, initPos):
        self.__connection=rtde.RTDE(self.__ip, self.__port)
        self.__connection.connect()

        #Print version controller
        self.__connection.get_controller_version()

        #Send settings for input and output and wathdog
        self.__connection.send_output_setup(self.__state_names, self.__state_types)
        self.__sets = self.__connection.send_input_setup(self.__sets_names, self.__sets_types)
        self.__target_q = initPos
        self.__watchdog = self.__connection.send_input_setup(self.__watchdog_names, self.__watchdog_types)


        self.__watchdog.input_int_register_0 = 0

        if not self.__connection.send_start():
            sys.exit()

        self.__target_q = self.getStatePoint()
        #Format registers
        self.__sets.input_double_register_0 = self.__target_q[0]
        self.__sets.input_double_register_1 = self.__target_q[1]
        self.__sets.input_double_register_2 = self.__target_q[2]
        self.__sets.input_double_register_3 = self.__target_q[3]
        self.__sets.input_double_register_4 = self.__target_q[4]
        self.__sets.input_double_register_5 = self.__target_q[5]

        self.__connection.send(self.__sets)
        self.__run=True

    def goToPoint(self, p1, p2, trj_planer, time):
        print("Generate trj between p1:", p1, " and ", p2)
        splines = trj_planer.poseCubicInterpolation(p1, p2, time)
        for i in range(0, int(time/self.__time_delay)):
            joints_pos = []
            for k in range(0,6):
                qt = splines[k].calcSpeed(i*self.__time_delay)[0, 0]
                joints_pos.append(qt)
            print("GO to point:",joints_pos)
            self.rt_send(joints_pos)



    def __check_position(self, list_of_state,list_of_sets, eps=1e-4):
        count=0
        assert(len(list_of_state)==len(list_of_sets)),"Error parameters for trajectory"
        for i in range(0,len(list_of_state)):
            if abs(list_of_state[i]-list_of_sets[i])<=eps:
                count+=1;
        if count==6:
            return True
        else:
            return False

    def rt_send(self, target_q):
        try:
            self.__target_q = target_q
            self.__state=self.__connection.receive()
            if self.__state is None:
                self.__run=False
            if self.__state.output_int_register_0!=0:
                self.__sets=self.__write_list_in_sets(self.__sets, self.__target_q)
                self.__connection.send(self.__sets)
            self.__connection.send(self.__watchdog)
            self.__ok = True
        except KeyboardInterrupt:
            print("Stop!")
            self.__ok = False
            sys.exit(0)


    def __state_to_poslist(self, state):
        list = state.__dict__["actual_q"]
        return deepcopy(list)

    def __sets_to_list(self, sets):
        list = []
        for i in range(0,6):
            list.append(sets.__dict__["input_double_register_%i" % i])
        return list

    def __write_list_in_sets(self, sets, list):
        for i in range (0,6):
            sets.__dict__["input_double_register_%i" % i] = list[i]
        return sets

    def stop(self):
        self.__stop()

    def getStatePoint(self):
        self.__state=self.__connection.receive()
        list=self.__state_to_poslist(self.__state);
        print(list)
        return list
