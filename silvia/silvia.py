import yaml
import redis
import threading
import RPi.GPIO as GPIO


GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)


class Silvia(threading.Thread):
    def __init__(self, r, config):
        threading.Thread.__init__(self)
        self.config = config
        self.r = r
        self.pubsub = self.r.pubsub()
        channels = ['temperature']
        for _input in config['coffee']['inputs']:
            channels.append('%s_switch' % _input)
        self.pubsub.subscribe(channels)
        self.power = False
        self.pump = config['coffee']['outputs']['pump']['pin']
        self.valve = config['coffee']['outputs']['valve']['pin']
        self.arduino = config['coffee']['outputs']['arduino']['pin']
        pump_default = config['coffee']['outputs']['pump']['default']
        valve_default = config['coffee']['outputs']['valve']['default']
        arduino_default = config['coffee']['outputs']['arduino']['default']
        try:
            GPIO.setup(self.pump, GPIO.OUT)
            GPIO.setup(self.valve, GPIO.OUT)
            GPIO.setup(self.arduino, GPIO.OUT)
            GPIO.output(self.pump, pump_default)
            GPIO.output(self.valve, valve_default)
            GPIO.output(self.arduino, arduino_default)
        except RuntimeWarning:
            pass

    def handle(self, item):
        if item['channel'] == 'brew_switch':
            if item['data'] == 'on':
                GPIO.output(12, 1)  # pump  todo: fix why this wasnt working
                GPIO.output(10, 1)  # valve
            elif item['data'] == 'off':
                GPIO.output(12, 0)
                GPIO.output(10, 0)
        elif item['channel'] == 'pump_switch':
            if item['data'] == 'on':
                GPIO.output(12, 1)
            elif item['data'] == 'off':
                GPIO.output(12, 0)

    def work(self, item):
        if item['channel'] == 'power_switch':
            if item['data'] == 'on':
                self.r.set('boiler.auto', 1)
                self.r.set('pid.auto', 1)
                self.power = True
            elif item['data'] == 'off':
                self.r.set('boiler.auto', 0)
                self.r.set('pid.auto', 0)
                GPIO.output(12, 0)
                GPIO.output(10, 0)
                self.power = False
        else:
            if self.power:
                self.handle(item)

    def run(self):
        for item in self.pubsub.listen():
            self.work(item)


def handle_silvia(config):
    r = redis.Redis(config['redis']['host'])
    s = Silvia(r, config)
    s.start()


if __name__ == '__main__':
    conf_file = '/etc/coffee.yaml'
    with open(conf_file, 'r') as yaml_conf:
        conf = yaml.load(yaml_conf)
        handle_silvia(conf)
