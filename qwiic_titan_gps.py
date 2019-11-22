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
from __future__ import print_function,division

import sys
import qwiic_i2c
import pynmea2

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
def __checkIsOnRPi():

    # Are we on a Pi? First Linux?

    if sys.platform not in ('linux', 'linux2'):
        return False

    # we can find out if we are on a RPI by looking at the contents
    # of /proc/device-tree/compatable

    try:
        with open('/proc/device-tree/compatible', 'r') as fCompat:

            systype = fCompat.read()

            return systype.find('raspberrypi') != -1
    except IOError:
        return False

# check if stretching is set if on a rpi
#
def _checkForRPiI2CClockStretch():

    #are we on a rpi?
    if not __checkIsOnRPi():
        return

    # read the boot config file and see if the clock stretch param is set
    try:
        with open('/boot/config.txt') as fConfig:

            strConfig = fConfig.read()
            for line in strConfig.split('\n'):
                if line.find('i2c_arm_baudrate') == -1:
                    continue

                # start with a comment?
                if line.strip().startswith('#'):
                    break

                # is the value less <= 10000
                params = line.split('=')
                if int(params[-1]) <= 10000:
                    # Stretching is enabled and set correctly.
                    return

                break
    except IOError:
        pass

    # if we are here, then we are on a Raspberry Pi and Clock Stretching isn't
    # set correctly.
    # Print out a message!

    print("""
============================================================================
 NOTE:

 For the SparkFun GPS Breakout to work on the Raspberry Pi, I2C clock stretching
 must be enabled.

 The following line must be added to the file /boot/config.txt

    dtparam=i2c_arm_baudrate=10000

 For more information, see the note at:
          https://github.com/sparkfun/qwiic_ublox_gps_py
============================================================================
        """)

# Define the device name and I2C addresses. These are set in the class defintion
# as class variables, making them avilable without having to create a class instance.
# This allows higher level logic to rapidly create a index of qwiic devices at
# runtine
#
# The name of this device
_DEFAULT_NAME = "Qwiic GPS"

# Some devices have multiple availabel addresses - this is a list of these addresses.
# NOTE: The first address in this list is considered the default I2C address for the
# device.
_AVAILABLE_I2C_ADDRESS = [0x10]

class QwiicGps(object):
    """
    QwiicGps

        :param address: The I2C address to use for the device.
                        If not provided, the default address is used.
        :param i2c_driver: An existing i2c driver object. If not provided
                        a driver object is created.
        :return: The ublox_gps device object.
        :rtype: Object
    """

    device_name = _DEFAULT_NAME
    available_addresses = _AVAILABLE_I2C_ADDRESS

    MAX_I2C_BUFFER = 32
    MAX_GPS_BUFFER = 255

    _i2c = qwiic_i2c.getI2CDriver()
    _RPiCheck = False

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
    }

    def __init__(self, address=None, i2c_driver=None):


        # As noted above, to run this device on a Raspberry Pi,
        # clock streching is needed.
        #
        # Lets check if it's enabled. This is done only once in
        # the session
        if not QwiicGps._RPiCheck:
            _checkForRPiI2CClockStretch()
            QwiicGps._RPiCheck = True

        # Did the user specify an I2C address?

        self.address = address if address is not None else self.available_addresses[0]

        # load the I2C driver if one isn't provided

        if i2c_driver is None:
            self._i2c = qwiic_i2c.getI2CDriver()
            if self._i2c is None:
                print("Unable to load I2C driver for this platform.")
                return
        else:
            self._i2c = i2c_driver

    # ----------------------------------

    def is_connected(self):
        """
            Determine if a gps device is conntected to the system..

            :return: True if the device is connected, otherwise False.
            :rtype: bool

        """
        return qwiic_i2c.isDeviceConnected(self.address)

    connected = property(is_connected)

    def begin(self):
        """
            Initialize the data transmission lines.

            :return: Returns True on success, False on failure
            :rtype: boolean

        """
        return self.is_connected()

    def get_raw_data(self):
        """
            This function pulls gps data from the module 255 bytes at a time.
            :return: A string of all the gps data.
            :rtype: String
        """
        raw_sentences = ""
        buffer_tracker = self.MAX_GPS_BUFFER
        raw_data = []

        while buffer_tracker != 0:

            if buffer_tracker > self.MAX_I2C_BUFFER:
                raw_data += self._i2c.readBlock(self.address, 0x00, self.MAX_I2C_BUFFER)
                buffer_tracker = buffer_tracker - self.MAX_I2C_BUFFER
                if raw_data[0] == 0x0A:
                    break

            elif buffer_tracker < self.MAX_I2C_BUFFER:
                raw_data += self._i2c.readBlock(self.address, 0x00, buffer_tracker)
                buffer_tracker = 0
                if raw_data[0] == 0x0A:
                    break

            for raw_bytes in raw_data:
                raw_sentences = raw_sentences + chr(raw_bytes)

        return raw_sentences

    def prepare_data(self):
        """
            This function seperates raw GPS data from the module into sentences
            of GNSS data.
            :return: A list of all the gathered GPS data.
            :rtype: List
        """
        sentences = self.get_raw_data()
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

    def get_nmea_data(self):
        """
            This function takes a list of GNSS sentences and uses the pynmea2
            parser to parse the data.
            :return: Returns True on success and False otherwise
            :rtype: Boolean
        """
        gps_data = self.prepare_data()
        msg = ""
        for sentence in gps_data:
            try:
                msg = pynmea2.parse(sentence)
                self.add_to_gnss_messages(msg)
            except pynmea2.nmea.ParseError:
                pass

        return True

    def add_to_gnss_messages(self, sentence):
        """
            This function takes parsed GNSS data and assigns them to the
            respective dictionary key.
            :return: Returns True
            :rtype: Boolean
        """
        try:
            self.gnss_messages['Time'] = sentence.timestamp
            self.gnss_messages['Lat_Direction'] = sentence.lat_dir
            self.gnss_messages['Long_Direction'] = sentence.lon_dir
            self.gnss_messages['Latitude'] = sentence.latitude
            self.gnss_messages['Lat'] = sentence.lat
            self.gnss_messages['Longitude'] = sentence.longitude
            self.gnss_messages['Long'] = sentence.lon
            self.gnss_messages['Altitude'] = sentence.altitude
            self.gnss_messages['Altitude_Units'] = sentence.altitude_units
            self.gnss_messages['Sat_Number'] = sentence.num_sats
            self.gnss_messages['Geo_Separation'] = sentence.geo_sep
            self.gnss_messages['Geo_Sep_Units'] = sentence.geo_sep_units
        except KeyError:
            pass
        except AttributeError:
            pass

        return True
