#!/usr/bin/python3
# Simple script to collect data from a couple dht22 sensors on a Raspberry Pi and submit to Cloudwatch
# You'll need to set up AWS Cloudwatch and your AWS/boto credentials
# plus the Adafruit_DHT library
# metrics and sensors are hard-coded, but the 2nd param to read_retry() is the GIO pin #

import time
import boto3
import Adafruit_DHT

cw_namespace = 'trailer'


def submit_metrics(metrics):
    cw = boto3.client('cloudwatch')
    ret = cw.put_metric_data(Namespace=cw_namespace, MetricData=metrics)
    if ret['ResponseMetadata']['HTTPStatusCode'] != 200:
        print("Failed to submit metrics:")
        print(metrics)
        print("response:")
        print(ret)


def dht_to_cw():
    MetricData = []
    humidity, temp_c = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, 4)
    temp_f = 1.8 * temp_c + 32
    MetricData.append({'MetricName': 'trailerTemp', 'Value': temp_f})
    MetricData.append({'MetricName': 'trailerHumidity', 'Value': humidity})
    tank_humidity, tank_temp_c = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, 24)
    tank_temp_f = 1.8 * tank_temp_c + 32
    MetricData.append({'MetricName': 'tankTemp', 'Value': tank_temp_f})
    MetricData.append({'MetricName': 'tankHumidity', 'Value': tank_humidity})
    submit_metrics(MetricData)

dht_to_cw()
