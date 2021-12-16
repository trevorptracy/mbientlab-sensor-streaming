# usage: python stream_acc.py [mac1] [mac2] ... [mac(n)]
from __future__ import print_function
from mbientlab.metawear import MetaWear, libmetawear, parse_value
from mbientlab.metawear.cbindings import *
from time import sleep
from threading import Event

## TT Includes
import numpy as np
#import matplotlib.pyplot as plt
import re
import matplotlib
#matplotlib.use('TkAgg')
#from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import multiprocessing
import time
import random
from tkinter import *

matplotlib.use('TKAgg')
from matplotlib import pyplot as plt

import platform
import sys

if sys.version_info[0] == 2:
    range = xrange

class State:
    # init
    def __init__(self, device):
        self.device = device
        self.samples = 0
        self.callback = FnVoid_VoidP_DataP(self.data_handler)
    # callback
    def data_handler(self, ctx, data):
        #print("%s -> %s" % (self.device.address, parse_value(data)))
        print("%s" % parse_value(data))
        dataStr = str(parse_value(data))
        xV = re.search(r'x : ([\-\d\.]+)\,', dataStr)
        yV = re.search(r'y : ([\-\d\.]+)\,', dataStr)
        zV = re.search(r'z : ([\-\d\.]+)', dataStr)

        xValue = float(xV.group(1))
        yValue = float(yV.group(1))
        zValue = float(zV.group(1))

        plt.scatter(self.samples, xValue)
        plt.scatter(self.samples, yValue)
        plt.scatter(self.samples, zValue)
        #plt.pause(0.00010)

        #if(self.samples % 50 == 0):
            #plt.pause(0.05)
            #plt.show()
            #(plt.figure()).canvas.draw_idle()

        self.samples+= 1

def main():
    states = []
    # connect
    for i in range(len(sys.argv) - 1):
        d = MetaWear(sys.argv[i + 1])
        d.connect()
        print("Connected to " + d.address)
        states.append(State(d))

    # graph setup
    #plt.axis([0,200,-1,-1])
    #plt.show()
    #window=Tk()

    # configure
    for s in states:
        print("Configuring device")
        # setup ble
        libmetawear.mbl_mw_settings_set_connection_parameters(s.device.board, 7.5, 7.5, 0, 6000)
        sleep(1.5)
        # setup acc
        libmetawear.mbl_mw_acc_set_odr(s.device.board, 100.0)
        libmetawear.mbl_mw_acc_set_range(s.device.board, 16.0)
        libmetawear.mbl_mw_acc_write_acceleration_config(s.device.board)
        # get acc and subscribe
        signal = libmetawear.mbl_mw_acc_get_acceleration_data_signal(s.device.board)
        libmetawear.mbl_mw_datasignal_subscribe(signal, None, s.callback)
        # start acc
        libmetawear.mbl_mw_acc_enable_acceleration_sampling(s.device.board)
        libmetawear.mbl_mw_acc_start(s.device.board)

    # sleep
    sleep(20.0)

    # tear down
    for s in states:
        # stop acc
        libmetawear.mbl_mw_acc_stop(s.device.board)
        libmetawear.mbl_mw_acc_disable_acceleration_sampling(s.device.board)
        # unsubscribe
        signal = libmetawear.mbl_mw_acc_get_acceleration_data_signal(s.device.board)
        libmetawear.mbl_mw_datasignal_unsubscribe(signal)
        # disconnect
        libmetawear.mbl_mw_debug_disconnect(s.device.board)

    # recap
    print("Total Samples Received")
    for s in states:
        print("%s -> %d" % (s.device.address, s.samples))



if __name__ == '__main__':
    #run(doblit=False)
    #run(doblit=True)
    main()