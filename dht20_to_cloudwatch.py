#!/usr/bin/python3
# Simple script to collect data from a dht20/aht20 sensor on a Raspberry Pi and submit to Cloudwatch
# You'll need to set up AWS Cloudwatch and your AWS/boto credentials
# plus the CircuitPython adafruit_ahtx0 library

import adafruit_ahtx0
import board
import boto3

sensor = adafruit_ahtx0.AHTx0(board.I2C())

temp_f = ( sensor.temperature * 9/5) + 32


def submit_metrics(metrics):
    cw = boto3.client('cloudwatch')
    ret = cw.put_metric_data(Namespace='house', MetricData=metrics)
    if ret['ResponseMetadata']['HTTPStatusCode'] != 200:
        print("Failed to submit metrics:")
        print(metrics)
        print("response:")
        print(ret)

def main():
    MetricData = []
    MetricData.append({'MetricName': 'garageBRTemp', 'Value': temp_f})
    MetricData.append({'MetricName': 'garageBRHumidity', 'Value': sensor.relative_humidity})
    submit_metrics(MetricData)

main()