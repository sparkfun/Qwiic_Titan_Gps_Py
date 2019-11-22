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
MAX_GPS_BUFFER = 255

_i2c = qwiic_i2c.getI2CDriver()

gnss_messages = {

    'Time'           : 0,
    'Latitude'       : 0,
    'Lat'            : 0,
    'Lat_Direction'  : "",
    'Longitude'      : 0,
    'Long'           : 0,
    'Long_Direction' : "",
    'Altitude'       : 0,
    'Altitude_Units' : "",
    'Sat_Number'     : 0,
    'Geo_Separation' : 0,
    'Geo_Sep_Units'  : "",
    'Data_Age'       : 0,
    'Ref_Station_ID' : 0
}

def connect_to_module():
    return qwiic_i2c.isDeviceConnected(address)

def get_raw_data():

    raw_sentences = ""
    buffer_tracker = MAX_GPS_BUFFER
    raw_data = []

    while buffer_tracker != 0: 

        if buffer_tracker > MAX_I2C_BUFFER:
            raw_data += _i2c.readBlock(address, 0x00, MAX_I2C_BUFFER)
            buffer_tracker = buffer_tracker - MAX_I2C_BUFFER
            if raw_data[0] == 0x0A:
                break

        elif buffer_tracker < MAX_I2C_BUFFER:
            raw_data += _i2c.readBlock(address, 0x00, buffer_tracker)
            buffer_tracker = 0
            if raw_data[0] == 0x0A:
                break

        for raw_bytes in raw_data: 
            raw_sentences = raw_sentences + chr(raw_bytes)
        
    return raw_sentences

def prepare_data():

    sentences = get_raw_data()
    clean_gnss_list = []
    complete_sentence_list = []
    gnss_list = sentences.split('\n')

    for sentence in gnss_list:
        if sentence is not '':
            clean_gnss_list.append(sentence)

    for index,sentence in enumerate(clean_gnss_list):
        if not sentence.startswith('$') and index is not 0:
            joined = clean_gnss_list[index - 1] + sentence
            complete_sentence_list.append(joined)
        else:
            complete_sentence_list.append(sentence)


    return complete_sentence_list

def get_nmea_data():
    gps_data = prepare_data()
    msg = ""
    for sentence in gps_data:
        try:
            msg = pynmea2.parse(sentence)
            add_to_gnss_messages(msg)
        except pynmea2.nmea.ParseError:
            pass

    return True

def add_to_gnss_messages(sentence): 
    try:
        gnss_messages['Time'] = sentence.lat_dir
        gnss_messages['Lat_Direction'] = sentence.lat_dir
        gnss_messages['Long_Direction'] = sentence.lon_dir
        gnss_messages['Latitude'] = sentence.latitude
        gnss_messages['Lat'] = sentence.lat
        gnss_messages['Longitude'] = sentence.longitude
        gnss_messages['Long'] = sentence.lon
        gnss_messages['Altitude'] = sentence.altitude
        gnss_messages['Altitude_Units'] = sentence.altitude_units
        gnss_messages['Sat_Number'] = sentence.num_sats
        gnss_messages['Geo_Separation'] = sentence.geo_sep
        gnss_messages['Geo_Sep_Units'] = sentence.geo_sep_units
        gnss_messages['Data_Age'] = sentence.age_gps_data
        gnss_messages['Ref_Station_ID'] = sentence.ref_station_id
    except KeyError:
        pass
    except AttributeError:
        pass

    return True

def run_example():

    if connect_to_module:
        print("Connected.")

        while True:
            if get_nmea_data() is True:
                for k,v in gnss_messages.items():
                    print(k, ":", v)

            sleep(1)


if __name__ == '__main__':
    try:
        run_example()
    except (KeyboardInterrupt, SystemExit) as exErr:
        print("Ending Basic Example.")
        sys.exit(0)
