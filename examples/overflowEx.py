###################################################################
#                                                                 #
#                    PLOT A LIVE GRAPH (PyQt5)                    #
#                  -----------------------------                  #
#            EMBED A MATPLOTLIB ANIMATION INSIDE YOUR             #
#            OWN GUI!                                             #
#                                                                 #
###################################################################
from __future__ import print_function

import sys
import os


from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *

from PyQt5 import QtGui, QtCore

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import functools
import numpy as np
import random as rd
import matplotlib
matplotlib.use("Qt5Agg")
from matplotlib.figure import Figure
from matplotlib.animation import TimedAnimation
from matplotlib.lines import Line2D
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import time
import threading


from mbientlab.metawear import MetaWear, libmetawear, parse_value
from mbientlab.metawear.cbindings import *
from time import sleep
from threading import Event
import re


running = True
recordingA = False
file_openA = False
acc_file = "acc.csv"

recordingG = False
file_openG = False
gyro_file = "gyro.csv"

recordingM = False
file_openM = False
mag_file = "mag.csv"

video_running = False
capture_thread = None
videoFlag = False
running = False

from PyQt5 import QtCore,QtWidgets,QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QFileDialog, QGraphicsRectItem, QGraphicsScene, QMessageBox, QMainWindow
import cv2
import sys
import MainWindow
import time
import datetime
import serial
import numpy as np

     
class MainWindowB(QMainWindow):
  
    # constructor
    def __init__(self):
        super().__init__()
  
        # setting geometry
        self.setGeometry(100, 100,
                         800, 600)
  
        # setting style sheet
        self.setStyleSheet("background : lightgrey;")
  
        # getting available cameras
        self.available_cameras = QCameraInfo.availableCameras()
  
        # if no camera found
        if not self.available_cameras:
            # exit the code
            sys.exit()
  
        # creating a status bar
        self.status = QStatusBar()
  
        # setting style sheet to the status bar
        self.status.setStyleSheet("background : white;")
  
        # adding status bar to the main window
        self.setStatusBar(self.status)
  
        # path to save
        self.save_path = ""
  
        # creating a QCameraViewfinder object
        self.viewfinder = QCameraViewfinder()
  
        # showing this viewfinder
        self.viewfinder.show()
  
        # making it central widget of main window
        self.setCentralWidget(self.viewfinder)
  
        # Set the default camera.
        self.select_camera(0)
  
        # creating a tool bar
        toolbar = QToolBar("Camera Tool Bar")
  
        # adding tool bar to main window
        self.addToolBar(toolbar)
  
        # creating a photo action to take photo
        click_action = QAction("Click photo", self)
  
        # adding status tip to the photo action
        click_action.setStatusTip("This will capture picture")
  
        # adding tool tip
        click_action.setToolTip("Capture picture")
  
  
        # adding action to it
        # calling take_photo method
        click_action.triggered.connect(self.click_photo)
  
        # adding this to the tool bar
        toolbar.addAction(click_action)
  
        # similarly creating action for changing save folder
        change_folder_action = QAction("Change save location",
                                       self)
  
        # adding status tip
        change_folder_action.setStatusTip("Change folder where picture will be saved saved.")
  
        # adding tool tip to it
        change_folder_action.setToolTip("Change save location")
  
        # setting calling method to the change folder action
        # when triggered signal is emitted
        change_folder_action.triggered.connect(self.change_folder)
  
        # adding this to the tool bar
        toolbar.addAction(change_folder_action)
  
        # creating a combo box for selecting camera
        camera_selector = QComboBox()
  
        # adding status tip to it
        camera_selector.setStatusTip("Choose camera to take pictures")
  
        # adding tool tip to it
        camera_selector.setToolTip("Select Camera")
        camera_selector.setToolTipDuration(2500)
  
        # adding items to the combo box
        camera_selector.addItems([camera.description()
                                  for camera in self.available_cameras])
  
        # adding action to the combo box
        # calling the select camera method
        camera_selector.currentIndexChanged.connect(self.select_camera)
  
        # adding this to tool bar
        toolbar.addWidget(camera_selector)
  
        # setting tool bar stylesheet
        toolbar.setStyleSheet("background : white;")
  
        # setting window title
        self.setWindowTitle("PyQt5 Cam")
  
        # showing the main window
        self.show()
  
    # method to select camera
    def select_camera(self, i):
  
        # getting the selected camera
        self.camera = QCamera(self.available_cameras[i])
  
        # setting view finder to the camera
        self.camera.setViewfinder(self.viewfinder)
  
        # setting capture mode to the camera
        self.camera.setCaptureMode(QCamera.CaptureStillImage)
  
        # if any error occur show the alert
        self.camera.error.connect(lambda: self.alert(self.camera.errorString()))
  
        # start the camera
        self.camera.start()
  
        # creating a QCameraImageCapture object
        self.capture = QCameraImageCapture(self.camera)
  
        # showing alert if error occur
        self.capture.error.connect(lambda error_msg, error,
                                   msg: self.alert(msg))
  
        # when image captured showing message
        self.capture.imageCaptured.connect(lambda d,
                                           i: self.status.showMessage("Image captured : " 
                                                                      + str(self.save_seq)))
  
        # getting current camera name
        self.current_camera_name = self.available_cameras[i].description()
  
        # inital save sequence
        self.save_seq = 0
  
    # method to take photo
    def click_photo(self):
        photosToTake=1
        i=0
        while(i<photosToTake):
            # time stamp
            timestamp = time.strftime("%d-%b-%Y-%H_%M_%S")
    
            # capture the image and save it on the save path
            self.capture.capture(os.path.join(self.save_path, 
                                            "%s-%04d-%s.jpg" % (
                self.current_camera_name,
                self.save_seq,
                timestamp
            )))
    
            # increment the sequence
            self.save_seq += 1
            i=i+1

    
    # change folder method
    def change_folder(self):
  
        # open the dialog to select path
        path = QFileDialog.getExistingDirectory(self, 
                                                "Picture Location", "")
  
        # if path is selected
        if path:
  
            # update the path
            self.save_path = path
  
            # update the sequence
            self.save_seq = 0
  
    # method for alerts
    def alert(self, msg):
  
        # error message
        error = QErrorMessage(self)
  
        # setting text to the error message
        error.showMessage(msg)

class CustomMainWindow(QMainWindow):
    def __init__(self):
        super(CustomMainWindow, self).__init__()
        # Define the geometry of the main window
        self.setGeometry(300, 300, 1500, 500)
        self.setWindowTitle("MBientlab Sensor Stream")
        # Create FRAME_A
        self.FRAME_A = QFrame(self)
        self.FRAME_A.setStyleSheet("QWidget { background-color: %s }" % QColor(210,210,235,255).name())
        self.LAYOUT_A = QGridLayout()
        self.FRAME_A.setLayout(self.LAYOUT_A)
        self.setCentralWidget(self.FRAME_A)

        # Place the Start Recording button
        self.startRec = QPushButton(text = 'Start Recording')
        self.startRec.setFixedSize(500, 30)
        self.startRec.clicked.connect(self.startRecAction)
        self.LAYOUT_A.addWidget(self.startRec, *(1,0))
        # Place the Stop Recording button
        self.startRec = QPushButton(text = 'Stop Recording')
        self.startRec.setFixedSize(500, 30)
        self.startRec.clicked.connect(self.stopRecAction)
        self.LAYOUT_A.addWidget(self.startRec, *(2,0))
        # Place the Exit button
        self.startRec = QPushButton(text = 'Exit Program')
        self.startRec.setFixedSize(500, 30)
        self.startRec.clicked.connect(self.exitAction)
        self.LAYOUT_A.addWidget(self.startRec, *(2,2))


        # Place the matplotlib figure (Solo's)
        self.myFigX = CustomFigCanvas(colorVal="red")
        self.myFigY = CustomFigCanvas(colorVal="green")
        self.myFigZ = CustomFigCanvas(colorVal="blue")
        #self.LAYOUT_A.addWidget(self.myFigX, *(0,1))
        #self.LAYOUT_A.addWidget(self.myFigY, *(0,2))
        #self.LAYOUT_A.addWidget(self.myFigZ, *(0,3))
        ########## (Combined)
        self.myFigXYZ = CustomFigCanvasXYZ()
        self.LAYOUT_A.addWidget(self.myFigXYZ, *(0,0))
        # Place the matplotlib figure (Solo's)
        self.myFigXG = CustomFigCanvas(colorVal="red")
        self.myFigYG = CustomFigCanvas(colorVal="green")
        self.myFigZG = CustomFigCanvas(colorVal="blue")
        #self.LAYOUT_A.addWidget(self.myFigX, *(0,1))
        #self.LAYOUT_A.addWidget(self.myFigY, *(0,2))
        #self.LAYOUT_A.addWidget(self.myFigZ, *(0,3))
        ########## (Combined)
        self.myFigXYZG = CustomFigCanvasXYZG()
        self.LAYOUT_A.addWidget(self.myFigXYZG, *(0,1))
        # Place the matplotlib figure (Solo's)
        self.myFigXMag = CustomFigCanvas(colorVal="red")
        self.myFigYMag = CustomFigCanvas(colorVal="green")
        self.myFigZMag = CustomFigCanvas(colorVal="blue")
        #self.LAYOUT_A.addWidget(self.myFigX, *(0,1))
        #self.LAYOUT_A.addWidget(self.myFigY, *(0,2))
        #self.LAYOUT_A.addWidget(self.myFigZ, *(0,3))
        ########## (Combined)
        self.myFigXYZMag = CustomFigCanvasXYZMag()
        self.LAYOUT_A.addWidget(self.myFigXYZMag, *(0,2))

        #self.ui = Ui_MainWindow()
        #self.ui.setupUi(self)
        #self.LAYOUT_A.addWidget(self.ui, *(2,2))
        
        myDataLoop = threading.Thread(name = 'myDataLoopSensor', target = dataSendLoopSensor, daemon = True, args = (self.addData_callbackFuncX,self.addData_callbackGyro,self.addData_callbackMag))
        myDataLoop.start()
        self.show()
        

    def zoomBtnAction(self):
        print("Start Recording")
        #self.myFig.zoomIn(5)
        # Update Global
        return
    def startRecAction(self):
        if(recordingA==True):
            print("Already Recording..")
            return
        listOfGlobals = globals()
        listOfGlobals['recordingA']=True
        listOfGlobals['recordingG']=True
        listOfGlobals['recordingM']=True
        print("Start Recording")
        #self.myFig.zoomIn(5)
        # Update Global
        return
    def stopRecAction(self):
        if(recordingA==False):
            print("Not Recording..")
            return
        listOfGlobals = globals()
        listOfGlobals['recordingA']=False
        listOfGlobals['recordingG']=False
        listOfGlobals['recordingM']=False
        print("Stop Recording")
        #self.myFig.zoomIn(5)
        # Update Global
        return
    def exitAction(self):
        print("Exiting...")
        listOfGlobals = globals()
        listOfGlobals['running']=False
        sleep(2.0)
        self.close()
        return

    def addData_callbackFuncX(self, value):
        # print("Add data: " + str(value))
        # Check to see recording status
        self.myFigX.addData(value[1])
        self.myFigY.addData(value[2])
        self.myFigZ.addData(value[3])
        self.myFigXYZ.addData(value) #for triple graph
        return
    def addData_callbackGyro(self, value):
        # print("Add data: " + str(value))
        self.myFigXG.addData(value[1])
        self.myFigYG.addData(value[2])
        self.myFigZG.addData(value[3])
        self.myFigXYZG.addData(value) #for triple graph
        return
    def addData_callbackMag(self, value):
        # print("Add data: " + str(value))
        self.myFigXMag.addData(value[1])
        self.myFigYMag.addData(value[2])
        self.myFigZMag.addData(value[3])
        self.myFigXYZMag.addData(value) #for triple graph
        return

class CustomFigCanvas(FigureCanvas, TimedAnimation):
    def __init__(self, **kwargs):
        # set default argument values
        self.colorVal = "black" #default
        # get a list of all predefined values directly from __dict__
        allowed_keys = list(self.__dict__.keys())
        # Update __dict__ but only for keys that have been predefined 
        # (silently ignore others)
        self.__dict__.update((key, value) for key, value in kwargs.items() 
                             if key in allowed_keys)
        # To NOT silently ignore rejected keys
        rejected_keys = set(kwargs.keys()) - set(allowed_keys)
        if rejected_keys:
            raise ValueError("Invalid arguments in constructor:{}".format(rejected_keys))


        self.addedData = []
        #print(matplotlib.__version__)
        # The data
        self.xlim = 200
        self.n = np.linspace(0, self.xlim - 1, self.xlim)
        a = []
        b = []
        a.append(2.0)
        a.append(4.0)
        a.append(2.0)
        b.append(4.0)
        b.append(3.0)
        b.append(4.0)
        self.y = (self.n * 0.0) + 50
        # The window
        self.fig = Figure(figsize=(10,10), dpi=100)
        self.ax1 = self.fig.add_subplot(111)
        # self.ax1 settings
        self.ax1.set_xlabel(' ')
        self.ax1.set_ylabel(' ')
        self.line1 = Line2D([], [], color=self.colorVal)
        self.line1_tail = Line2D([], [], color='red', linewidth=2)
        self.line1_head = Line2D([], [], color='red', marker='o', markeredgecolor='r')
        self.ax1.add_line(self.line1)
        self.ax1.add_line(self.line1_tail)
        self.ax1.add_line(self.line1_head)
        self.ax1.set_xlim(0, self.xlim - 1)
        self.ax1.set_ylim(-10, 10)

        self.ax1.grid(False)
        self.ax1.axis('off')
        #self.ax1.set(facecolor = "orange")
        #self.ax1.patch.set_alpha(0.1)

        FigureCanvas.__init__(self, self.fig)
        TimedAnimation.__init__(self, self.fig, interval = 50, blit = True)
        return

    def new_frame_seq(self):
        return iter(range(self.n.size))

    def set_graph_color(self, colorVal):
        self.line1 = Line2D([], [], color=colorVal)
        return

    def _init_draw(self):
        lines = [self.line1, self.line1_tail, self.line1_head]
        for l in lines:
            l.set_data([], [])
        return

    def addData(self, value):
        self.addedData.append(value)
        return

    def zoomIn(self, value):
        bottom = self.ax1.get_ylim()[0]
        top = self.ax1.get_ylim()[1]
        bottom += value
        top -= value
        self.ax1.set_ylim(bottom,top)
        self.draw()
        return

    def _step(self, *args):
        # Extends the _step() method for the TimedAnimation class.
        try:
            TimedAnimation._step(self, *args)
        except Exception as e:
            self.abc += 1
            #print(str(self.abc))
            TimedAnimation._stop(self)
            pass
        return

    def _draw_frame(self, framedata):
        margin = 2
        while(len(self.addedData) > 0):
            self.y = np.roll(self.y, -1)
            self.y[-1] = self.addedData[0]
            del(self.addedData[0])

        self.line1.set_data(self.n[ 0 : self.n.size - margin ], self.y[ 0 : self.n.size - margin ])
        self.line1_tail.set_data(np.append(self.n[-10:-1 - margin], self.n[-1 - margin]), np.append(self.y[-10:-1 - margin], self.y[-1 - margin]))
        self.line1_head.set_data(self.n[-1 - margin], self.y[-1 - margin])
        self._drawn_artists = [self.line1, self.line1_tail, self.line1_head]
        return

class CustomFigCanvasXYZ(FigureCanvas, TimedAnimation):
    def __init__(self):
        self.addedDataX = []
        self.addedDataY = []
        self.addedDataZ = []
        #print(matplotlib.__version__)
        # The data
        self.xlim = 200
        self.n = np.linspace(0, self.xlim - 1, self.xlim)
        a = []
        b = []
        a.append(2.0)
        a.append(4.0)
        a.append(2.0)
        b.append(4.0)
        b.append(3.0)
        b.append(4.0)
        self.y = (self.n * 0.0) + 50
        self.y2 = (self.n * 0.0) + 50
        self.y3 = (self.n * 0.0) + 50
        # The window
        self.fig = Figure(figsize=(10,10), dpi=100)
        self.ax1 = self.fig.add_subplot(111)
        # self.ax1 settings
        self.ax1.set_xlabel('Accelerometer')
        self.ax1.set_ylabel(' ')
        self.line1 = Line2D([], [], color='blue')
        self.line1_tail = Line2D([], [], color='blue', linewidth=2)
        self.line1_head = Line2D([], [], color='blue', marker='o', markeredgecolor='r')
        self.ax1.add_line(self.line1)
        self.ax1.add_line(self.line1_tail)
        self.ax1.add_line(self.line1_head)
        self.ax1.set_xlim(0, self.xlim - 1)
        self.ax1.set_ylim(-10, 10)
        # LINE 2 settings
        #self.ax1.set_xlabel('time')
        #self.ax1.set_ylabel('raw data')
        self.line2 = Line2D([], [], color='red')
        self.line2_tail = Line2D([], [], color='red', linewidth=2)
        self.line2_head = Line2D([], [], color='red', marker='o', markeredgecolor='r')
        self.ax1.add_line(self.line2)
        self.ax1.add_line(self.line2_tail)
        self.ax1.add_line(self.line2_head)
        #self.ax1.set_xlim(0, self.xlim - 1)
        #self.ax1.set_ylim(-10, 10)
        # LINE 3 settings
        self.line3 = Line2D([], [], color='green')
        self.line3_tail = Line2D([], [], color='green', linewidth=2)
        self.line3_head = Line2D([], [], color='green', marker='o', markeredgecolor='r')
        self.ax1.add_line(self.line3)
        self.ax1.add_line(self.line3_tail)
        self.ax1.add_line(self.line3_head)

        FigureCanvas.__init__(self, self.fig)
        TimedAnimation.__init__(self, self.fig, interval = 50, blit = True)
        return

    def new_frame_seq(self):
        return iter(range(self.n.size))

    def _init_draw(self):
        linesX = [self.line1, self.line1_tail, self.line1_head]
        for lX in linesX:
            lX.set_data([], [])
        linesY = [self.line2, self.line2_tail, self.line2_head]
        for lY in linesY:
            lY.set_data([], [])
        linesZ = [self.line3, self.line3_tail, self.line3_head]
        for lZ in linesZ:
            lZ.set_data([], [])
        return

    def addData(self, value):
        self.addedDataX.append(value[1])
        self.addedDataY.append(value[2])
        self.addedDataZ.append(value[3])
        return

    def zoomIn(self, value):
        bottom = self.ax1.get_ylim()[0]
        top = self.ax1.get_ylim()[1]
        bottom += value
        top -= value
        self.ax1.set_ylim(bottom,top)
        self.draw()
        return

    def _step(self, *args):
        # Extends the _step() method for the TimedAnimation class.
        try:
            TimedAnimation._step(self, *args)
        except Exception as e:
            self.abc += 1
            #print(str(self.abc))
            TimedAnimation._stop(self)
            pass
        return

    def _draw_frame(self, framedata):
        margin = 2
        while(len(self.addedDataX) > 0):
            # X DATA
            self.y = np.roll(self.y, -1)
            self.y[-1] = self.addedDataX[0]
            del(self.addedDataX[0])
            # Y DATA
            self.y2 = np.roll(self.y2, -1)
            self.y2[-1] = self.addedDataY[0]
            del(self.addedDataY[0])
            # Z DATA
            self.y3 = np.roll(self.y3, -1)
            self.y3[-1] = self.addedDataZ[0]
            del(self.addedDataZ[0])

        self.line1.set_data(self.n[ 0 : self.n.size - margin ], self.y[ 0 : self.n.size - margin ])
        self.line1_tail.set_data(np.append(self.n[-10:-1 - margin], self.n[-1 - margin]), np.append(self.y[-10:-1 - margin], self.y[-1 - margin]))
        self.line1_head.set_data(self.n[-1 - margin], self.y[-1 - margin])
        #self._drawn_artists = [self.line1, self.line1_tail, self.line1_head]

        self.line2.set_data(self.n[ 0 : self.n.size - margin ], self.y2[ 0 : self.n.size - margin ])
        self.line2_tail.set_data(np.append(self.n[-10:-1 - margin], self.n[-1 - margin]), np.append(self.y2[-10:-1 - margin], self.y2[-1 - margin]))
        self.line2_head.set_data(self.n[-1 - margin], self.y2[-1 - margin])
        #self._drawn_artists = [self.line2, self.line2_tail, self.line2_head]

        self.line3.set_data(self.n[ 0 : self.n.size - margin ], self.y3[ 0 : self.n.size - margin ])
        self.line3_tail.set_data(np.append(self.n[-10:-1 - margin], self.n[-1 - margin]), np.append(self.y3[-10:-1 - margin], self.y3[-1 - margin]))
        self.line3_head.set_data(self.n[-1 - margin], self.y3[-1 - margin])
        self._drawn_artists = [self.line1, self.line1_tail, self.line1_head, self.line2, self.line2_tail, self.line2_head, self.line3, self.line3_tail, self.line3_head]
        return

class CustomFigCanvasXYZG(FigureCanvas, TimedAnimation):
    def __init__(self):
        self.addedDataX = []
        self.addedDataY = []
        self.addedDataZ = []
        #print(matplotlib.__version__)
        # The data
        self.xlim = 200
        self.n = np.linspace(0, self.xlim - 1, self.xlim)
        a = []
        b = []
        a.append(2.0)
        a.append(4.0)
        a.append(2.0)
        b.append(4.0)
        b.append(3.0)
        b.append(4.0)
        self.y = (self.n * 0.0) + 50
        self.y2 = (self.n * 0.0) + 50
        self.y3 = (self.n * 0.0) + 50
        # The window
        self.fig = Figure(figsize=(10,10), dpi=100)
        self.ax1 = self.fig.add_subplot(111)
        # self.ax1 settings
        self.ax1.set_xlabel('Gyroscope')
        self.ax1.set_ylabel(' ')
        self.line1 = Line2D([], [], color='blue')
        self.line1_tail = Line2D([], [], color='blue', linewidth=2)
        self.line1_head = Line2D([], [], color='blue', marker='o', markeredgecolor='r')
        self.ax1.add_line(self.line1)
        self.ax1.add_line(self.line1_tail)
        self.ax1.add_line(self.line1_head)
        self.ax1.set_xlim(0, self.xlim - 1)
        self.ax1.set_ylim(-2000, 2000)
        # LINE 2 settings
        #self.ax1.set_xlabel('time')
        #self.ax1.set_ylabel('raw data')
        self.line2 = Line2D([], [], color='red')
        self.line2_tail = Line2D([], [], color='red', linewidth=2)
        self.line2_head = Line2D([], [], color='red', marker='o', markeredgecolor='r')
        self.ax1.add_line(self.line2)
        self.ax1.add_line(self.line2_tail)
        self.ax1.add_line(self.line2_head)
        #self.ax1.set_xlim(0, self.xlim - 1)
        #self.ax1.set_ylim(-10, 10)
        # LINE 3 settings
        self.line3 = Line2D([], [], color='green')
        self.line3_tail = Line2D([], [], color='green', linewidth=2)
        self.line3_head = Line2D([], [], color='green', marker='o', markeredgecolor='r')
        self.ax1.add_line(self.line3)
        self.ax1.add_line(self.line3_tail)
        self.ax1.add_line(self.line3_head)

        FigureCanvas.__init__(self, self.fig)
        TimedAnimation.__init__(self, self.fig, interval = 50, blit = True)
        return

    def new_frame_seq(self):
        return iter(range(self.n.size))

    def _init_draw(self):
        linesX = [self.line1, self.line1_tail, self.line1_head]
        for lX in linesX:
            lX.set_data([], [])
        linesY = [self.line2, self.line2_tail, self.line2_head]
        for lY in linesY:
            lY.set_data([], [])
        linesZ = [self.line3, self.line3_tail, self.line3_head]
        for lZ in linesZ:
            lZ.set_data([], [])
        return

    def addData(self, value):
        self.addedDataX.append(value[1])
        self.addedDataY.append(value[2])
        self.addedDataZ.append(value[3])
        return

    def zoomIn(self, value):
        bottom = self.ax1.get_ylim()[0]
        top = self.ax1.get_ylim()[1]
        bottom += value
        top -= value
        self.ax1.set_ylim(bottom,top)
        self.draw()
        return

    def _step(self, *args):
        # Extends the _step() method for the TimedAnimation class.
        try:
            TimedAnimation._step(self, *args)
        except Exception as e:
            self.abc += 1
            #print(str(self.abc))
            TimedAnimation._stop(self)
            pass
        return

    def _draw_frame(self, framedata):
        margin = 2
        while(len(self.addedDataX) > 0):
            # X DATA
            self.y = np.roll(self.y, -1)
            self.y[-1] = self.addedDataX[0]
            del(self.addedDataX[0])
            # Y DATA
            self.y2 = np.roll(self.y2, -1)
            self.y2[-1] = self.addedDataY[0]
            del(self.addedDataY[0])
            # Z DATA
            self.y3 = np.roll(self.y3, -1)
            self.y3[-1] = self.addedDataZ[0]
            del(self.addedDataZ[0])

        self.line1.set_data(self.n[ 0 : self.n.size - margin ], self.y[ 0 : self.n.size - margin ])
        self.line1_tail.set_data(np.append(self.n[-10:-1 - margin], self.n[-1 - margin]), np.append(self.y[-10:-1 - margin], self.y[-1 - margin]))
        self.line1_head.set_data(self.n[-1 - margin], self.y[-1 - margin])
        #self._drawn_artists = [self.line1, self.line1_tail, self.line1_head]

        self.line2.set_data(self.n[ 0 : self.n.size - margin ], self.y2[ 0 : self.n.size - margin ])
        self.line2_tail.set_data(np.append(self.n[-10:-1 - margin], self.n[-1 - margin]), np.append(self.y2[-10:-1 - margin], self.y2[-1 - margin]))
        self.line2_head.set_data(self.n[-1 - margin], self.y2[-1 - margin])
        #self._drawn_artists = [self.line2, self.line2_tail, self.line2_head]

        self.line3.set_data(self.n[ 0 : self.n.size - margin ], self.y3[ 0 : self.n.size - margin ])
        self.line3_tail.set_data(np.append(self.n[-10:-1 - margin], self.n[-1 - margin]), np.append(self.y3[-10:-1 - margin], self.y3[-1 - margin]))
        self.line3_head.set_data(self.n[-1 - margin], self.y3[-1 - margin])
        self._drawn_artists = [self.line1, self.line1_tail, self.line1_head, self.line2, self.line2_tail, self.line2_head, self.line3, self.line3_tail, self.line3_head]
        return

class CustomFigCanvasXYZMag(FigureCanvas, TimedAnimation):
    def __init__(self):
        self.addedDataX = []
        self.addedDataY = []
        self.addedDataZ = []
        #print(matplotlib.__version__)
        # The data
        self.xlim = 200
        self.n = np.linspace(0, self.xlim - 1, self.xlim)
        a = []
        b = []
        a.append(2.0)
        a.append(4.0)
        a.append(2.0)
        b.append(4.0)
        b.append(3.0)
        b.append(4.0)
        self.y = (self.n * 0.0) + 50
        self.y2 = (self.n * 0.0) + 50
        self.y3 = (self.n * 0.0) + 50
        # The window
        self.fig = Figure(figsize=(10,10), dpi=100)
        self.ax1 = self.fig.add_subplot(111)
        # self.ax1 settings
        self.ax1.set_xlabel('Magnetometer')
        self.ax1.set_ylabel(' ')
        self.line1 = Line2D([], [], color='blue')
        self.line1_tail = Line2D([], [], color='blue', linewidth=2)
        self.line1_head = Line2D([], [], color='blue', marker='o', markeredgecolor='r')
        self.ax1.add_line(self.line1)
        self.ax1.add_line(self.line1_tail)
        self.ax1.add_line(self.line1_head)
        self.ax1.set_xlim(0, self.xlim - 1)
        self.ax1.set_ylim(-2048, 2048)
        # LINE 2 settings
        #self.ax1.set_xlabel('time')
        #self.ax1.set_ylabel('raw data')
        self.line2 = Line2D([], [], color='red')
        self.line2_tail = Line2D([], [], color='red', linewidth=2)
        self.line2_head = Line2D([], [], color='red', marker='o', markeredgecolor='r')
        self.ax1.add_line(self.line2)
        self.ax1.add_line(self.line2_tail)
        self.ax1.add_line(self.line2_head)
        #self.ax1.set_xlim(0, self.xlim - 1)
        #self.ax1.set_ylim(-10, 10)
        # LINE 3 settings
        self.line3 = Line2D([], [], color='green')
        self.line3_tail = Line2D([], [], color='green', linewidth=2)
        self.line3_head = Line2D([], [], color='green', marker='o', markeredgecolor='r')
        self.ax1.add_line(self.line3)
        self.ax1.add_line(self.line3_tail)
        self.ax1.add_line(self.line3_head)

        FigureCanvas.__init__(self, self.fig)
        TimedAnimation.__init__(self, self.fig, interval = 50, blit = True)
        return

    def new_frame_seq(self):
        return iter(range(self.n.size))

    def _init_draw(self):
        linesX = [self.line1, self.line1_tail, self.line1_head]
        for lX in linesX:
            lX.set_data([], [])
        linesY = [self.line2, self.line2_tail, self.line2_head]
        for lY in linesY:
            lY.set_data([], [])
        linesZ = [self.line3, self.line3_tail, self.line3_head]
        for lZ in linesZ:
            lZ.set_data([], [])
        return

    def addData(self, value):
        self.addedDataX.append(value[1])
        self.addedDataY.append(value[2])
        self.addedDataZ.append(value[3])
        return

    def zoomIn(self, value):
        bottom = self.ax1.get_ylim()[0]
        top = self.ax1.get_ylim()[1]
        bottom += value
        top -= value
        self.ax1.set_ylim(bottom,top)
        self.draw()
        return

    def _step(self, *args):
        # Extends the _step() method for the TimedAnimation class.
        try:
            TimedAnimation._step(self, *args)
        except Exception as e:
            self.abc += 1
            #print(str(self.abc))
            TimedAnimation._stop(self)
            pass
        return

    def _draw_frame(self, framedata):
        margin = 2
        while(len(self.addedDataX) > 0):
            # X DATA
            self.y = np.roll(self.y, -1)
            self.y[-1] = self.addedDataX[0]
            del(self.addedDataX[0])
            # Y DATA
            self.y2 = np.roll(self.y2, -1)
            self.y2[-1] = self.addedDataY[0]
            del(self.addedDataY[0])
            # Z DATA
            self.y3 = np.roll(self.y3, -1)
            self.y3[-1] = self.addedDataZ[0]
            del(self.addedDataZ[0])

        self.line1.set_data(self.n[ 0 : self.n.size - margin ], self.y[ 0 : self.n.size - margin ])
        self.line1_tail.set_data(np.append(self.n[-10:-1 - margin], self.n[-1 - margin]), np.append(self.y[-10:-1 - margin], self.y[-1 - margin]))
        self.line1_head.set_data(self.n[-1 - margin], self.y[-1 - margin])
        #self._drawn_artists = [self.line1, self.line1_tail, self.line1_head]

        self.line2.set_data(self.n[ 0 : self.n.size - margin ], self.y2[ 0 : self.n.size - margin ])
        self.line2_tail.set_data(np.append(self.n[-10:-1 - margin], self.n[-1 - margin]), np.append(self.y2[-10:-1 - margin], self.y2[-1 - margin]))
        self.line2_head.set_data(self.n[-1 - margin], self.y2[-1 - margin])
        #self._drawn_artists = [self.line2, self.line2_tail, self.line2_head]

        self.line3.set_data(self.n[ 0 : self.n.size - margin ], self.y3[ 0 : self.n.size - margin ])
        self.line3_tail.set_data(np.append(self.n[-10:-1 - margin], self.n[-1 - margin]), np.append(self.y3[-10:-1 - margin], self.y3[-1 - margin]))
        self.line3_head.set_data(self.n[-1 - margin], self.y3[-1 - margin])
        self._drawn_artists = [self.line1, self.line1_tail, self.line1_head, self.line2, self.line2_tail, self.line2_head, self.line3, self.line3_tail, self.line3_head]
        return


# You need to setup a signal slot mechanism, to
# send data to your GUI in a thread-safe way.
class Communicate(QObject):
    data_signalX = pyqtSignal(list)
    #data_signalX = pyqtSignal(float)

class State:
    # init
    def __init__(self, device):
        self.device = device
        self.samples = 0
        self.callback = FnVoid_VoidP_DataP(self.data_handler)
        self.callbackGyro = FnVoid_VoidP_DataP(self.data_handlerGyro)
        self.callbackMag = FnVoid_VoidP_DataP(self.data_handlerMag)
        self.xData = []
        self.yData = []
        self.zData = []
    # callback
    def data_handler(self, ctx, data):
        #print("%s -> %s" % (self.device.address, parse_value(data)))

        dataStr = str(parse_value(data))
        xV = re.search(r'x : ([\-\d\.]+)\,', dataStr)
        yV = re.search(r'y : ([\-\d\.]+)\,', dataStr)
        zV = re.search(r'z : ([\-\d\.]+)', dataStr)

        global recordingA
        global file_openA
        global acc_file

        if(recordingA==True and file_openA==False):
            #open/create a file
            timestr = time.strftime("%Y%m%d-%H%M%S")
            acc_file = "./csv/acc_"+timestr+".csv"
            fileAcc = open(acc_file, "w")
            accWr = [xV.group(1)+","+yV.group(1)+","+zV.group(1)+"\n"]
            fileAcc.writelines(accWr)
            fileAcc.close()
            file_openA = True
        elif(recordingA==True and file_openA==True):
            #log data
            fileAcc = open(acc_file, "a")
            accWr = [xV.group(1)+","+yV.group(1)+","+zV.group(1)+"\n"]
            fileAcc.writelines(accWr)
            #print("Acc: %s" % parse_value(data))
            print(".", end='', flush=True)
            fileAcc.close()
        elif(recordingA==False and file_openA==True):
            #close file
            file_openA=False

        global xValue
        xValue = float(xV.group(1))
        global yValue
        yValue = float(yV.group(1))
        global zValue
        zValue = float(zV.group(1))

        global arrayVar
        arrayVar = [None] * 4 #empty array size 4
        arrayVar[1] = xValue
        arrayVar[2] = yValue
        arrayVar[3] = zValue

        mySrc.data_signalX.emit(arrayVar)

        self.samples+= 1

    def data_handlerGyro(self, ctx, data):
        #print("Gyro: %s" % parse_value(data))
        dataStr = str(parse_value(data))
        xV = re.search(r'x : ([\-\d\.]+)\,', dataStr)
        yV = re.search(r'y : ([\-\d\.]+)\,', dataStr)
        zV = re.search(r'z : ([\-\d\.]+)', dataStr)

        global recordingG
        global file_openG
        global gyro_file

        if(recordingG==True and file_openG==False):
            #open/create a file
            timestr = time.strftime("%Y%m%d-%H%M%S")
            gyro_file = "./csv/gyro_"+timestr+".csv"
            fileGyro = open(gyro_file, "w")
            gyroWr = [xV.group(1)+","+yV.group(1)+","+zV.group(1)+"\n"]
            fileGyro.writelines(gyroWr)
            fileGyro.close()
            file_openG = True
        elif(recordingG==True and file_openG==True):
            #log data
            fileGyro = open(gyro_file, "a")
            gyroWr = [xV.group(1)+","+yV.group(1)+","+zV.group(1)+"\n"]
            fileGyro.writelines(gyroWr)
            #print("Gyro: %s" % parse_value(data))
            print(".", end='', flush=True)
            fileGyro.close()
        elif(recordingG==False and file_openG==True):
            #close file
            file_openG=False

        global xValueGyro
        xValueGyro = float(xV.group(1))
        global yValueGyro
        yValueGyro = float(yV.group(1))
        global zValueGyro
        zValueGyro = float(zV.group(1))

        global arrayVarGyro
        arrayVarGyro = [None] * 4 #empty array size 4
        arrayVarGyro[1] = xValueGyro
        arrayVarGyro[2] = yValueGyro
        arrayVarGyro[3] = zValueGyro

        mySrcGyro.data_signalX.emit(arrayVarGyro)

        self.samples+= 1

    def data_handlerMag(self, ctx, data):
        #print("Mag: %s" % parse_value(data))
        dataStr = str(parse_value(data))
        xV = re.search(r'x : ([\-\d\.]+)\,', dataStr)
        yV = re.search(r'y : ([\-\d\.]+)\,', dataStr)
        zV = re.search(r'z : ([\-\d\.]+)', dataStr)

        global recordingM
        global file_openM
        global mag_file

        if(recordingM==True and file_openM==False):
            #open/create a file
            timestr = time.strftime("%Y%m%d-%H%M%S")
            mag_file = "./csv/mag_"+timestr+".csv"
            fileMag = open(mag_file, "w")
            magWr = [xV.group(1)+","+yV.group(1)+","+zV.group(1)+"\n"]
            fileMag.writelines(magWr)
            fileMag.close()
            file_openM = True
        elif(recordingM==True and file_openM==True):
            #log data
            fileMag = open(mag_file, "a")
            magWr = [xV.group(1)+","+yV.group(1)+","+zV.group(1)+"\n"]
            fileMag.writelines(magWr)
            #print("Mag: %s" % parse_value(data))
            print(".", end='', flush=True)
            fileMag.close()
        elif(recordingM==False and file_openM==True):
            #close file
            file_openM=False

        global xValueMag
        xValueMag = float(xV.group(1))
        global yValueMag
        yValueMag = float(yV.group(1))
        global zValueMag
        zValueMag = float(zV.group(1))

        global arrayVarMag
        arrayVarMag = [None] * 4 #empty array size 4
        arrayVarMag[1] = xValueMag
        arrayVarMag[2] = yValueMag
        arrayVarMag[3] = zValueMag

        mySrcMag.data_signalX.emit(arrayVarMag)

        self.samples+= 1

def dataSendLoopSensor(addData_callbackFuncX, addData_callbackGyro, addData_callbackMag):
    # Setup the signal-slot mechanism.
    

    global mySrc
    mySrc = Communicate()
    mySrc.data_signalX.connect(addData_callbackFuncX)

    global mySrcGyro
    mySrcGyro = Communicate()
    mySrcGyro.data_signalX.connect(addData_callbackGyro)

    global mySrcMag
    mySrcMag = Communicate()
    mySrcMag.data_signalX.connect(addData_callbackMag)

    states = []
    # connect
    d = MetaWear('D8:D3:B8:56:A8:15')
    d.connect()
    print("Connected to " + d.address)
    states.append(State(d))

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

        # setup gyro
        # get gyro & subscribe
        gyro = libmetawear.mbl_mw_gyro_bmi160_get_rotation_data_signal(s.device.board)
        libmetawear.mbl_mw_datasignal_subscribe(gyro, None, s.callbackGyro)
        # start gyro
        libmetawear.mbl_mw_gyro_bmi160_enable_rotation_sampling(s.device.board)
        libmetawear.mbl_mw_gyro_bmi160_start(s.device.board)

        # setup magnetometer 
        # get mag & subscribe
        libmetawear.mbl_mw_mag_bmm150_set_preset(s.device.board, MagBmm150Preset.HIGH_ACCURACY)
        #libmetawear.mbl_mw_mag_bmm150_set_preset(s.device.board, MagBmm150Preset.LOW_POWER)
        mag = libmetawear.mbl_mw_mag_bmm150_get_b_field_data_signal(s.device.board)
        libmetawear.mbl_mw_datasignal_subscribe(mag, None, s.callbackMag)
        # start mag
        libmetawear.mbl_mw_mag_bmm150_enable_b_field_sampling(s.device.board)
        libmetawear.mbl_mw_mag_bmm150_start(s.device.board)
        

    # sleep
    #listOfGlobals = globals()
    #listOfGlobals['running']=False
    global running
    running=True
    while(running):
        sleep(1.0)

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




if __name__== '__main__':
    # Create Globals
    app = QApplication(sys.argv)
    QApplication.setStyle(QStyleFactory.create('Plastique'))
    myGUI = CustomMainWindow()
    
    camWindow = MainWindowB()
    camWindow.show()

    sys.exit(app.exec_())