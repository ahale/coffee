from flask import Flask
import redis
app = Flask(__name__)
r = redis.Redis('127.0.0.1')

index_content = """
<a href='/'><h1>coffee</h1></a>
  <ul>
    <li> <a href='power_on'>power on</a> <a href='power_off'>power off</a>
    <li> <a href='brew_on'>brew on</a> <a href='brew_off'>brew off</a>
    <li> <a href='pump_on'>pump on</a> <a href='pump_off'>pump off</a>
    <li> <a href='steam_on'>steam on</a> <a href='steam_off'>steam off</a>
  </ul>
  <img src='http://192.168.1.104:8080/render/?width=600&height=400&from=-4hours&tz=Europe/London&yMaxRight=1&yAxisSide=left&yMaxLeft=120&yMinRight=0&yMinLeft=0&target=coffee.temperature&target=coffee.setpoint&target=secondYAxis%28coffee.dutycycle%29'></img>
"""


@app.route('/')
def index():
    return index_content


@app.route('/power_on')
def power_on():
    r.publish('power_switch', 'on')
    r.set('power_switch', 'on')
    return index_content


@app.route('/power_off')
def power_off():
    r.publish('power_switch', 'off')
    r.set('power_switch', 'off')
    return index_content


@app.route('/brew_on')
def brew_on():
    r.publish('brew_switch', 'on')
    r.set('brew_switch', 'on')
    return index_content


@app.route('/brew_off')
def brew_off():
    r.publish('brew_switch', 'off')
    r.set('brew_switch', 'off')
    return index_content


@app.route('/pump_on')
def pump_on():
    r.publish('pump_switch', 'on')
    r.set('pump_switch', 'on')
    return index_content


@app.route('/pump_off')
def pump_off():
    r.publish('pump_switch', 'off')
    r.set('pump_switch', 'off')
    return index_content


@app.route('/steam_on')
def steam_on():
    r.publish('steam_switch', 'on')
    r.set('steam_switch', 'on')
    return index_content


@app.route('/steam_off')
def steam_off():
    r.publish('steam_switch', 'off')
    r.set('steam_switch', 'off')
    return index_content


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
