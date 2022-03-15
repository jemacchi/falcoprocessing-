#!/bin/bash
# se requiere un parametro de entrada en script, que indica cantidad de ciclos/mensajes que se enviaran
for (( c=1; c<=$1; c++ ))
do
	./send_data.sh "test-data"+$c
done

