# mosquitto-influxdb-grafana

PoC para testear mosquitto+influxdb+grafana.

## Instalación 


## Ejecución

En la PoC tenemos:

1. Mosquitto. Debe estar corriendo y escuchando en puerto segun configuracion (en nuestro caso localhost:1883). Se puede validar revisando con:

   `sudo systemctl status mosquitto` 

   o en su defecto 

   `netstat -nape | grep 1883` 

   para lo cual se deberá observar que esté andando como corresponde.

2. En una consola, ejecutar script python para escuchar el topico $SYS. 

   `python ./check_sys_data.py`

3. En una consola, ejecutar script python para escuchar el topico de testing (test/test1). 

   `python ./check_data.py`

4. En una consola, ejecutar script bash send_data.sh para enviar un mensaje al topico de testing (test/test1).  

  `./send_data "mensaje prueba"`

  Al ejecutar el punto 4, en las pantallas correspondientes a suscriptores definidos en punto 2 y 3, se podrán observar los mensajes del topico de prueba, y los eventos del sistema.

