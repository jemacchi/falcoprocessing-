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
MQTT_TOPIC = 'test/test1'
MQTT_REGEX = 'test/([^/]+)'
MQTT_CLIENT_ID = 'MQTTTestInfluxDBBridge'

influxdb_client = InfluxDBClient(INFLUXDB_ADDRESS, 8086, INFLUXDB_USER, INFLUXDB_PASSWORD, None)

class SampleData(NamedTuple):
    testnumber: str
    msg: str

def on_connect(client, userdata, flags, rc):
    """ The callback for when the client receives a CONNACK response from the server."""
    print('Connected with result code ' + str(rc))
    client.subscribe(MQTT_TOPIC)

def _parse_mqtt_message(topic, payload):
    match = re.match(MQTT_REGEX, topic)
    if match:
        testnumber = match.group(1)
        return SampleData(testnumber, payload)
    else:
        return None

def _send_sample_data_to_influxdb(sample_data):
    json_body = [
        {
            'measurement': sample_data.testnumber,
            'tags': {
                'testnumber': sample_data.testnumber
            },
            'fields': {
                'value': sample_data.msg
            }
        }
    ]
    influxdb_client.write_points(json_body)

def on_message(client, userdata, msg):
    """The callback for when a PUBLISH message is received from the server."""
    print(msg.topic + ' ' + str(msg.payload))
    sample_data = _parse_mqtt_message(msg.topic, msg.payload.decode('utf-8'))
    if sample_data is not None:
        _send_sample_data_to_influxdb(sample_data)

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
    print('MQTT Test topic to InfluxDB bridge')
    main()
