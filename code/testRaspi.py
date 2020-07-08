import raspi

v = '0.3'

raspi.init()

temp = raspi.getTemp()

print('Temperatura: ' + temp)

throttled = raspi.getThrottled()

print('Throtted: ' + throttled)