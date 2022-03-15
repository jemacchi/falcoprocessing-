#!/bin/bash
while true
do
	echo "Send data emulator - Press [CTRL+C] to stop.."
        messages=$(( ( RANDOM % 100 )  + 1 ))
        echo "Sending "$messages"  messages"
        ./send_bulk_data.sh $messages
	sleep 5
done
