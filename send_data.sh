#!/bin/bash
mosquitto_pub -d -h localhost -u jemacchi -P jemacchi -q 0 -t test/test1 -m "$1"

