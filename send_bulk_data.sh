#!/bin/bash
for (( c=1; c<=$1; c++ ))
do
	./send_data.sh "hi"+$c
done

