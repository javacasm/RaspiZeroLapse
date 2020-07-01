# RaspiZeroLapse

Ejemplo de programa sencillo en python para hacer timeLapses controlados desde telegram en una Raspberry Pi Zero W

Basado en https://github.com/javacasm/RiegoRaspberryArduino

Comandos:

* **/image** Captura una imagen
* **/last** Envía la última tomada
* **/fecha:YYYYMMDDHHmmss** envía la anterior y posterior de la fecha indicada (opción a dar un rango y enviar todas las que lo cumplan, por ejemplo hora o día)
* **/voltaje** Nos dice como va la batería (usa throttled)
* **/T100s** Periodo entre fotos

TODO:

* Trabajar la reconexión a la red
* Controlar Excepciones
