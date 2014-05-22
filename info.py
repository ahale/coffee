import time
import redis


r = redis.Redis('127.0.0.1')


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
    info['pid.auto'] = r.get('pid.auto')

    print(info)
    time.sleep(1)
