#!/usr/bin/python3
# Simple script to collect data from a couple dht22 sensors on a Raspberry Pi and submit to Cloudwatch
# You'll need to set up AWS Cloudwatch and your AWS/boto credentials
# plus the Adafruit_DHT library
# metrics and sensors are hard-coded, but the 2nd param to read_retry() is the GIO pin #

import time
import boto3
import Adafruit_DHT

def submit_metric(cw, name, value):
    ret = cw.put_metric_data(Namespace='trailer', MetricData=[{'MetricName': name, 'Value': value }])
    if ret['ResponseMetadata']['HTTPStatusCode'] != 200:
        print("Failed to submit %s." % name)
        print(ret)


def dht_to_cw():
    cw = boto3.client('cloudwatch')
    humidity, temp_c = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, 4)
    temp_f = 1.8 * temp_c + 32
    submit_metric(cw, 'trailerTemp', temp_f)
    submit_metric(cw, 'trailerHumidity', humidity)
    tank_humidity, tank_temp_c = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, 24)
    tank_temp_f = 1.8 * tank_temp_c + 32
    submit_metric(cw, 'tankTemp', tank_temp_f)
    submit_metric(cw, 'tankHumidity', tank_humidity)

dht_to_cw()
