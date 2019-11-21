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
