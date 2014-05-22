import time
import redis
import socket


def send_stat(metric, value):
    try:
        now = int(time.time())
        data = "%s %s %d\n" % (metric, value, now)
        sock = socket.socket()
        sock.connect(("127.0.0.1", 2003))
        sock.sendall(data)
        sock.close()
    except:
        pass


r = redis.Redis('127.0.0.1')
pubsub = r.pubsub()
pubsub.subscribe(["temperature"])
while True:
    info = {}
    info['power'] = r.get('pid.output')
    info['boiler_auto'] = r.get('boiler.auto')
    info['boiler_active_time'] = r.get('boiler.active_time')
    info['temperature'] = r.get("temperature")
    info['power_switch'] = r.get("power_switch")
    info['brew_switch'] = r.get("brew_switch")
    info['pump_switch'] = r.get("pump_switch")
    info['steam_switch'] = r.get("steam_switch")
    info['setpoint'] = r.get("pid.setpoint")
    # send_stat("coffee.temperature", item["data"])
    send_stat("coffee.temperature", info['temperature'])
    send_stat("coffee.setpoint", info['setpoint'])
    send_stat("coffee.dutycycle", info['boiler_active_time'])
    send_stat("inputs.power", info['power_switch'])
    send_stat("inputs.brew", info['brew_switch'])
    send_stat("inputs.pump", info['pump_switch'])
    send_stat("inputs.steam", info['steam_switch'])
    time.sleep(1)
