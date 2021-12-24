## Installing Required Libraries
```
pip install metawear
pip install PyQt5
```

## Running the Applications
The main application for data logging is found in:
./ust-data-logger/ustLogger.py

The system was tested & ran on Python 3.9.5 with Visual Studio Code

To run the application, open the file in VSCode and right click the file and select: 
"Run Current File in Interactive Window"

If you have an error like the following:
```
Exception ignored on calling ctypes callback function: <bound method MetaWear._write_gatt_char> .... etc etc etc
```
Close the interactive tab and run the following "scan_connect.py" in an interactive window.

Find the Metawear BT device and enter in its index. Once the system successfully connects and disconnects, go back to "ustLogger.py" and re-run.
