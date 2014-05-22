import sys
import time
import redis
import yaml
import RPi.GPIO as GPIO


GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)


def handle_boiler(config):
    r = redis.Redis(config['redis']['host'])
    boiler = config['coffee']['outputs']['boiler']['pin']
    boiler_default = config['coffee']['outputs']['boiler']['default']
    try:
        GPIO.setup(boiler, GPIO.OUT)
        GPIO.output(boiler, boiler_default)
    except RuntimeWarning:
        pass
    r.set('boiler.auto', boiler_default)
    r.set('boiler.active_time', 0.0)
    while True:
        power = r.get('pid.output')
        if power and r.get('boiler.auto'):
            active_time = round((int(power) * 100.0) / 1023) / 100
            sleep_time = 1.0 - active_time
            print('active_time: %s' % active_time)
            r.set('boiler.active_time', active_time)
            if active_time > 0:
                GPIO.output(boiler, 1)
                time.sleep(active_time)
                GPIO.output(boiler, 0)
            time.sleep(sleep_time)
        else:
            r.set('boiler.active_time', 0)
            print('pid or boiler off')
            time.sleep(1)


if __name__ == '__main__':
    conf_file = '/etc/coffee.yaml'
    try:
        with open(conf_file, 'r') as yaml_conf:
            conf = yaml.load(yaml_conf)
    except:
        print('config error, check %s' % conf_file)
        sys.exit(1)
    handle_boiler(conf)
