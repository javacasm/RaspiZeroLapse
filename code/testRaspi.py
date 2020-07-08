import raspi

v = '0.1'

raspi.init()

temp = raspi.getTemp()

print('Temperatura: ' + temp)