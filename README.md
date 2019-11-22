Qwiic_GPS Breakout XA110
----
![SparkFun GPS Breakout - XA1110
(Qwiic)](https://cdn.sparkfun.com/r/500-500/assets/parts/1/2/3/4/0/14414-02.jpg)

This is a Python module for the SparkFun GPS Breakout - XA110. 

This package should be used in conjunction with the overall [SparkFun qwiic Python Package](https://github.com/sparkfun/Qwiic_Py). New to qwiic? Take a look at the entire [SparkFun qwiic ecosystem](https://www.sparkfun.com/qwiic).

## Contents
* [Supported Platforms](#supported-platforms)
* [Dependencies](#dependencies)
* [Installation](#installation)
* [Documentation](#documentation)
* [Example Use](#example-use)

Supported Platforms
--------------------
The qwiic titan gps Python package current supports the following platforms:
* [Raspberry Pi](https://www.sparkfun.com/search/results?term=raspberry+pi)
<!-- Platforms to be tested
* [NVidia Jetson Nano](https://www.sparkfun.com/products/15297)
* [Google Coral Development Board](https://www.sparkfun.com/products/15318)
-->

Dependencies 
---------------
This package depends on the qwiic I2C driver: [Qwiic_I2C_Py](https://github.com/sparkfun/Qwiic_I2C_Py)

Documentation
-------------
The SparkFun qwiic titan gps module documentation is hosted at [ReadTheDocs](https://qwiic-pca9685-py.readthedocs.io/en/latest/?)

Installation
-------------

### PyPi Installation
This repository is hosted on PyPi as the [sparkfun-qwiic-pca9685](https://pypi.org/project/sparkfun-qwiic-pca9685/) package. On systems that support PyPi installation via pip, this library is installed using the following commands

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
A package file is built and placed in a subdirectory called dist. This package file can be installed using pip.
```sh
cd dist
pip install sparkfun_qwiic_titan_gps-<version>.tar.gz
  
```
Example Use
---------------

```python
if __name__ == '__main__':
    try:
        run_example()
    except (KeyboardInterrupt, SystemExit) as exErr:
        print("Ending Basic Example.")
        sys.exit(0)
 ```

See the examples directory for more detailed use examples.
