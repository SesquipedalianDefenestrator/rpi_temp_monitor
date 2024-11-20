#!/usr/bin/python3
# Simple script to collect data from a couple dht22 sensors on a Raspberry Pi and submit to Cloudwatch
# You'll need to set up AWS Cloudwatch and your AWS/boto credentials
# plus the CircuitPython adafruit_dht library
# substitute pin IDs as appropriate

import time
import boto3
import adafruit_dht
import board

cw_namespace = 'trailer'
RETRY_WAIT = 0.1


def submit_metrics(metrics):
    cw = boto3.client('cloudwatch')
    ret = cw.put_metric_data(Namespace=cw_namespace, MetricData=metrics)
    if ret['ResponseMetadata']['HTTPStatusCode'] != 200:
        print("Failed to submit metrics:")
        print(metrics)
        print("response:")
        print(ret)

def get_values_with_retry(pin_id):
# For a single-core rpi, pulseio doesn't work because it
# spawns a realtime busy-waiting process that starves
# everything else.  Disabling it may work, but in my
# experience has an extraordinarily high failure rate
# (hence the layers of retries)
    dhtDevice = adafruit_dht.DHT22(pin_id, use_pulseio=True)
    for i in range(1,10):
        try:
            temp_c = dhtDevice.temperature
            if temp_c == None:
                time.sleep(RETRY_WAIT)
                continue
            break
        except RuntimeError as e:
            if (i <= 9):
                time.sleep(RETRY_WAIT)
                continue
            else:
                raise e
    for i in range(1,10):
        try:
            humidity = dhtDevice.humidity
            if humidity == None:
                time.sleep(RETRY_WAIT)
                continue
            break
        except RuntimeError as e:
            if (i <= 9):
                time.sleep(RETRY_WAIT)
                continue
            else:
                raise e
    temp_f = 1.8 * temp_c + 32
    return (temp_f, humidity)
            
def dht_to_cw():
    MetricData = []
    for i in range(1,10):
        try:
            temp_f, humidity = get_values_with_retry(board.D17)
            break
        except TypeError:
            time.sleep(RETRY_WAIT)
            continue
    MetricData.append({'MetricName': 'trailerTemp', 'Value': temp_f})
    MetricData.append({'MetricName': 'trailerHumidity', 'Value': humidity})
    for i in range(1,10):
        try:
            tank_temp_f, tank_humidity = get_values_with_retry(board.D24)
            break
        except TypeError:
            time.sleep(RETRY_WAIT)
            continue
    MetricData.append({'MetricName': 'tankTemp', 'Value': tank_temp_f})
    MetricData.append({'MetricName': 'tankHumidity', 'Value': tank_humidity})
    submit_metrics(MetricData)

dht_to_cw()
