Qwiic GPS Breakout XA1110
==============

<p align="center">
   <img src="https://cdn.sparkfun.com/assets/custom_pages/2/7/2/qwiic-logo-registered.jpg"  width=200>  
   <img src="https://www.python.org/static/community_logos/python-logo-master-v3-TM.png"  width=240>   
</p>
<p align="center">
	<a href="https://pypi.org/project/sparkfun-qwiic-titan-gps/" alt="Package">
		<img src="https://img.shields.io/pypi/pyversions/sparkfun_qwiic_vl53l1x.svg" /></a>
	<a href="https://github.com/sparkfun/Qwiic_Titan_Gps_Py/issues" alt="Issues">
		<img src="https://img.shields.io/github/issues/sparkfun/Qwiic_Titan_Gps_Py.svg" /></a>
	<a href="https://qwiic-titan-gps-py.readthedocs.io/en/latest/" alt="Documentation">
		<img src="https://readthedocs.org/projects/qwiic-titan_gps-py/badge/?version=latest&style=flat" /></a>
	<a href="https://github.com/sparkfun/Qwiic_Titan_Gps_Py/blob/master/LICENSE" alt="License">
		<img src="https://img.shields.io/badge/license-MIT-blue.svg" /></a>
	<a href="https://twitter.com/intent/follow?screen_name=sparkfun">
        	<img src="https://img.shields.io/twitter/follow/sparkfun.svg?style=social&logo=twitter"
           	 alt="follow on Twitter"></a>
	
</p>

<img src="https://cdn.sparkfun.com//assets/parts/1/2/3/4/0/14414-SparkFun_GPS_Breakout_-_XA1110__Qwiic_-01.jpg"  align="right" width=300 alt="SparkFun Qwiic GPS Breakout XA1110">

Python module for the [Qwiic GPS Breakout XA1110 (Qwiic)](https://www.sparkfun.com/products/14414).

This package should be used in conjunction with the overall [SparkFun qwiic Python Package](https://github.com/sparkfun/Qwiic_Py). New to qwiic? Take a look at the entire [SparkFun qwiic ecosystem](https://www.sparkfun.com/qwiic).
## Contents
* [Supported Platforms](#supported-platforms)
* [Dependencies](#dependencies)
* [Installation](#installation)
* [Documentation](#documentation)
* [Example Use](#example-use)

Supported Platforms
---
The Qwiic Titan GPS Python package current supports the following platforms:
* [Raspberry Pi](https://www.sparkfun.com/search/results?term=raspberry+pi)

Platforms to be tested
---
* [Nvidia Jetson Nano](https://www.sparkfun.com/products/15297)
* [Google Coral Development Board](https://www.sparkfun.com/products/15318)

Dependencies 
---------------
This package depends on the Qwiic I2C driver: [Qwiic_I2C_Py](https://github.com/sparkfun/Qwiic_I2C_Py)

Documentation
-------------
The SparkFun Qwiic Titan GPS module documentation is hosted at [ReadTheDocs](https://qwiic-titan-gps-py.readthedocs.io/en/latest/)

Installation
-------------

### PyPi Installation
This repository is hosted on PyPi as the [sparkfun-qwiic-titan-gps](https://pypi.org/project/sparkfun-qwiic-titan-gps/) 
package. On systems that support PyPi installation via pip, this library is installed using the following commands

For all users (note: the user must have sudo privileges):
```sh
sudo pip install sparkfun-qwiic-titan-gps
sudo pip install pynmea2
```
For the current user:

```sh
sudo pip install sparkfun-qwiic-titan-gps
sudo pip install pynmea2
```

### Local Installation
To install, make sure the setuptools package is installed on the system.

Direct installation at the command line:
```sh
python setup.py install
```

To build a package for use with pip:
```sh
python setup.py sdist
 ```
A package file is built and placed in a subdirectory called "dist". This package file can be installed using pip.
```sh
cd dist
pip install sparkfun_qwiic_titan_gps-<version>.tar.gz
  
```
Example Use
---------------

```python
def run_example():

    print("SparkFun u-blox GPS!")
    qwiicGPS = qwiic_titan_gps.QwiicTitanGps()

    if qwiicGPS.connected is False:
        print("Could not connect to to the SparkFun GPS Unit. Double check that\
              it's wired correctly.", file=sys.stderr)
        return

    qwiicGPS.begin()

    while True:
        if qwiicGPS.get_nmea_data() is True:
            print("Latitude: {}, Longitude: {}, Time: {}".format(
                qwiicGPS.gnss_messages['Latitude'],
                qwiicGPS.gnss_messages['Longitude'],
                qwiicGPS.gnss_messages['Time']))

        sleep(1)


if __name__ == '__main__':
    try:
        run_example()
    except (KeyboardInterrupt, SystemExit) as exErr:
        print("Ending Basic Example.")
        sys.exit(0)
 ```

See the examples directory for more detailed use examples.

