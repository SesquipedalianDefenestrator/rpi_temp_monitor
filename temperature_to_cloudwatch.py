# Simple script to collect data from a 1wire sensor on a Raspberry Pi and submit to Cloudwatch
# You'll need to set up AWS Cloudwatch and your AWS/boto credentials
# and probably modify the device path.

#!/usr/bin/python
import time
import boto3

def submit_to_cw(temperature):
    cw = boto3.client('cloudwatch')
    ret = cw.put_metric_data(Namespace='trailer', MetricData=[{'MetricName': 'trailerTemp', 'Value': temperature }])
    if ret['ResponseMetadata']['HTTPStatusCode'] != 200:
        print("Failed")
        print(ret)

def runit():
    f = open('/sys/devices/w1_bus_master1/28-0416b364e8ff/w1_slave', 'r')
    lines = f.readlines()
    f.close()
    if lines[0].strip()[-3:] != 'YES':
        exit(1)
    raw_temp_val = lines[1].split('=')[1]
    temp_c = float(raw_temp_val) / 1000.0
    temp_f = 1.8 * temp_c + 32
    #print(str(temp_c) + ' degrees C')
    print(str(temp_f) + ' degrees F')
    print("submitting... ")
    submit_to_cw(temp_f)

runit()
