#-----------------------------------------------------------------------------
# qwiic_titan_gps.py
#
# Python library for the SparkFun's line of u-Blox GPS units.
#
# SparkFun GPS Breakout - XA1110
#   https://www.sparkfun.com/products/14414
#
#------------------------------------------------------------------------
#
# Written by SparkFun Electronics, November 2019
#
# This python library supports the SparkFun Electroncis qwiic
# qwiic sensor/board ecosystem
#
# More information on qwiic is at https:// www.sparkfun.com/qwiic
#
# Do you like this library? Help support SparkFun. Buy a board!
#==================================================================================
# Copyright (c) 2019 SparkFun Electronics
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#==================================================================================
#
# This is mostly a port of existing Arduino functionaly, so pylint is sad.
# The goal is to keep the public interface pthonic, but internal is internal
#
# pylint: disable=line-too-long, bad-whitespace, invalid-name, too-many-public-methods
#

"""
qwiic_titan_gps
============
Python library for [SparkFun GPS Breakot -
XA1110](https://www.sparkfun.com/products/14414)

This python package is a port of the existing [SparkFun GPS Arduino\
Library](https://github.com/sparkfun/SparkFun_I2C_GPS_Arduino_Library).

This package can be used in conjunction with the overall [SparkFun qwiic Python Package](https://github.com/sparkfun/Qwiic_Py)

New to qwiic? Take a look at the entire [SparkFun qwiic ecosystem](https://www.sparkfun.com/qwiic).

"""

#======================================================================
# NOTE: For Raspberry Pi
#======================================================================
# For this sensor to work on the Raspberry Pi, I2C clock stretching
# must be enabled.
#
# To do this:
#   - Login as root to the target Raspberry Pi
#   - Open the file /boot/config.txt in your favorite editor (vi, nano ...etc)
#   - Scroll down until the bloct that contains the following is found:
#           dtparam=i2c_arm=on
#           dtparam=i2s=on
#           dtparam=spi=on
#   - Add the following line:
#           # Enable I2C clock stretching
#           dtparam=i2c_arm_baudrate=10000
#
#   - Save the file
#   - Reboot the raspberry pi
#======================================================================
from time import sleep
import sys
import qwiic_i2c
import pynmea2

address = 0x10

MAX_I2C_BUFFER = 32
MAX_DATA_BUFFER = 255

_i2c = qwiic_i2c.getI2CDriver()

def connect_to_module():
    return qwiic_i2c.isDeviceConnected(address)

def get_raw_data():
    raw_sentences = ""
    buffer_tracker = MAX_DATA_BUFFER

    while buffer_tracker != 0: 

        if buffer_tracker > MAX_I2C_BUFFER:
            raw_data = _i2c.readBlock(address, 0x00, MAX_I2C_BUFFER)
            buffer_tracker = buffer_tracker - MAX_I2C_BUFFER
            if raw_data[0] == 0x0A:
                break

        elif buffer_tracker < MAX_I2C_BUFFER:
            raw_data = _i2c.readBlock(address, 0x00, buffer_tracker)
            buffer_tracker = 0
            if raw_data[0] == 0x0A:
                break

        for sentence in raw_data: 
            raw_sentences = raw_sentences + chr(sentence)
        
    return raw_sentences

def prepare_data():
    sentences = get_raw_data()
    gnss_list = sentences.split('$')
    clean_gnss_list = []
    for sentence in gnss_list:
        clean_gnss_list.append('$' + sentence.replace('\n',''))
    return clean_gnss_list

def run_example():

    if connect_to_module:
        print("Connected.")

        while True:
            gps_data = prepare_data()
            for sentence in gps_data:
                try:
                   msg = pynmea2.parse(sentence)
                   print(msg.lat)
                   print(msg.lon)
                except:
                    print(sentence)
                    pass

        sleep(.100)

if __name__ == '__main__':
    try:
        run_example()
    except (KeyboardInterrupt, SystemExit) as exErr:
        print("Ending Basic Example.")
        sys.exit(0)
