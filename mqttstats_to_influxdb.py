import re
from typing import NamedTuple

import paho.mqtt.client as mqtt
from influxdb import InfluxDBClient

INFLUXDB_ADDRESS = '127.0.0.1'
INFLUXDB_USER = 'mqtt'
INFLUXDB_PASSWORD = 'mqtt'
INFLUXDB_DATABASE = 'test'

MQTT_ADDRESS = '127.0.0.1'
MQTT_USER = 'jemacchi'
MQTT_PASSWORD = 'jemacchi'
MQTT_TOPIC = [('$SYS/broker/bytes/received',0),('$SYS/broker/bytes/sent',0),('$SYS/broker/clients/connected',0),('$SYS/broker/publish/messages/dropped',0),('$SYS/broker/publish/messages/received',0),('$SYS/broker/publish/messages/sent',0),('$SYS/broker/messages/inflight',0),('$SYS/broker/messages/received',0),('$SYS/broker/messages/sent',0),('$SYS/broker/subscriptions/count',0) ];
MQTT_SPLIT = '$SYS/'
MQTT_CLIENT_ID = 'MQTTSysStatsInfluxDBBridge'

influxdb_client = InfluxDBClient(INFLUXDB_ADDRESS, 8086, INFLUXDB_USER, INFLUXDB_PASSWORD, None)

class StatData(NamedTuple):
    statname: str
    value: int

def on_connect(client, userdata, flags, rc):
    """ The callback for when the client receives a CONNACK response from the server."""
    print('Connected with result code ' + str(rc))
    client.subscribe(MQTT_TOPIC)

def _parse_mqtt_message(topic, payload):
    msg = topic.split(MQTT_SPLIT)
    statname = msg[1]
    if statname:
        return StatData(statname, int(payload))
    else:
        return None

def _send_stat_data_to_influxdb(stat_data):
    json_body = [
        {
            'measurement': 'mqtt_stats',
            'tags': {
                'statname': stat_data.statname
            },
            'fields': {
                'value': stat_data.value
            }
        }
    ]
    influxdb_client.write_points(json_body)

def on_message(client, userdata, msg):
    """The callback for when a PUBLISH message is received from the server."""
    print(msg.topic + ' ' + str(msg.payload))
    stat_data = _parse_mqtt_message(msg.topic, msg.payload.decode('utf-8'))
    if stat_data is not None:
        _send_stat_data_to_influxdb(stat_data)

def _init_influxdb_database():
    databases = influxdb_client.get_list_database()
    if len(list(filter(lambda x: x['name'] == INFLUXDB_DATABASE, databases))) == 0:
        influxdb_client.create_database(INFLUXDB_DATABASE)
    influxdb_client.switch_database(INFLUXDB_DATABASE)

def main():
    _init_influxdb_database()

    mqtt_client = mqtt.Client(MQTT_CLIENT_ID)
    mqtt_client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message

    mqtt_client.connect(MQTT_ADDRESS, 1883)
    mqtt_client.loop_forever()


if __name__ == '__main__':
    print('MQTT System Stats to InfluxDB bridge')
    main()
