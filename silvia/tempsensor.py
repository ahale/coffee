import smbus
import sys
import time
import redis
import yaml


class Arduino(object):
    def __init__(self):
        self.bus = smbus.SMBus(0)
        self.address = 0x04

    def get_temperature(self):
        """
        grabs 16 bytes of i2c input, the max temp length is 6 bytes
        with a \x00 terminator so a random sampling of this much
        should have the data required.

        returns temperature as float or False if no reading ready.
        """
        data = ''
        temperature = 0.0
        try:
            for i in xrange(16):
                try:
                    data += chr(self.bus.read_byte(self.address))
                    temperature = float(data.split('\x00')[1].lstrip())
                except IOError:
                    return False
                except ValueError:
                    temperature = False
            return temperature
        except IndexError:
            return False


def handle_arduino(config):
    r = redis.Redis('127.0.0.1')
    arduino = Arduino()
    while True:
        temperature = arduino.get_temperature()
        if temperature:
            r.publish('temperature', temperature)
            r.set("temperature", temperature)
            print("temperature: %s" % temperature)
        time.sleep(0.1)

if __name__ == '__main__':
    conf_file = '/etc/coffee.yaml'
    try:
        with open(conf_file, 'r') as yaml_conf:
            conf = yaml.load(yaml_conf)
            handle_arduino(conf)
    except:
        print('config error, check %s' % conf_file)
        sys.exit(1)