# RaspiZeroLapse

Ejemplo de programa sencillo en python para hacer timeLapses controlados desde telegram en una Raspberry Pi Zero W


![Licencia CC](./images/Licencia_CC_peque.png) by @javacasm

Basado en https://github.com/javacasm/RiegoRaspberryArduino

Comandos:

* **/foto** Captura una imagen
* **/last** Envía la última tomada
* **/T100** Periodo entre fotos (en milisegundos)
* **/NnumImagen** Envía la imagen numImagen
* **/imageName** enviña la imagen pedida

TODO:

* Trabajar la reconexión a la red
* Controlar Excepciones
* Añadir fecha o contador ([Ejemplo1](https://raspberrypi.stackexchange.com/questions/54930/possible-to-display-current-time-in-pi-camera-recording) [Ejemplo2](https://www.raspberrypi.org/forums/viewtopic.php?t=187773))  
* Comandos:
    * Comando D para borrar: algunos o todos
    * Comando G para generar gif [Ejemplo](https://projects.raspberrypi.org/en/projects/timelapse-setup/5)
    * **/fecha:YYYYMMDDHHmmss** envía la anterior y posterior de la fecha indicada (opción a dar un rango y enviar todas las que lo cumplan, por ejemplo hora o día)
    * **/voltaje** Nos dice como va la batería (usa throttled)
    * **/temp** Nos da la temperatura de la raspberry
    * Crear directorio para el timelapse
    * Descargar todas las imagenes
    * **/TL:Nombre,TiempoEntreFotos** Crea un nuevo directorio para ese proyecto y toma fotos cada TiempoEntreFotos
