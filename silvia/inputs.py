import sys
import time
import yaml
import redis
import RPi.GPIO as GPIO


power_states = {1: "off", 0: "on"}
GPIO.setmode(GPIO.BOARD)
r = redis.Redis('127.0.0.1')


def input_event(channel):
    time.sleep(0.1)
    pub = '%s_switch' % channels[channel]
    val = power_states[GPIO.input(channel)]
    r.publish(pub, val)
    r.set(pub, val)
    print('%s turned %s' % (pub, val))


def handle_inputs(config):
    global channels
    channels = {}
    for _input in config:
        channels[config[_input]['pin']] = _input
        GPIO.setup(config[_input]['pin'], GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(config[_input]['pin'], GPIO.BOTH,
                              callback=input_event, bouncetime=110)
    while True:
        time.sleep(1)


if __name__ == '__main__':
    conf_file = '/etc/coffee.yaml'
    try:
        with open(conf_file, 'r') as yaml_conf:
            conf = yaml.load(yaml_conf)
            handle_inputs(conf['coffee']['inputs'])
    except:
        print('config error, check %s' % conf_file)
        sys.exit(1)
