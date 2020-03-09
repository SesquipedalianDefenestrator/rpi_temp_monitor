# Raspberry Pi temperature monitoring


In my case, I used a Raspberry Pi Zero W for low power consumption and small size, but probably any Pi would do, or any similar device with GPIO type capabilities.  I also wanted Bluetooth to talk to Victron devices, but that didn't work out (their stuff is good about speaking Modbus-over-TCP via wifi/ethernet if you buy their GX gear, but they haven't standardized any of their bluetooth protocols.

There's example scripts for each of the different sensor types.  You probably shouldn't use them as an example of great Python, but they work.

### Sensors
There's a couple of different sensor types that will work.  I initially used a DS18B20.  They're dirt cheap and come in waterproof form-factors for almost as cheap, but in retrospect I'd suggest spending the extra couple of bucks for a DHT22 unless you're planning on using a bunch of different 1-wire sensors.  In both cases you'll need a pull-up resistor, but a lot of the time you can buy them with one already integrated for another couple bucks.  There's a ton of roughly equivalent options in both cases, but I'll link the ones I used:
The specific DS18B20 I used initially:  https://www.amazon.com/gp/product/B013GB27HS/
The DHT22 I ordered:  https://www.amazon.com/gp/product/B073F472JL/

### Wiring
In both cases, you'll need to connect the sensor to a 3.3V pin for power (pin 1 or 17 on RPI Zero W), a ground pin (I used pin6, but there are several), and a GPIO pin (I used 4, then when I switched to a pair of DHT22 used 4 and 24)
If you don't buy one with a buit-in pull-up resistor, you'll need to connect a 4.7KOhm or 10KOhm (there seems to be some question as to which is better, but the details are beyond my circuit design experience) between the GPIO wire and the power wire.  If you're doing a longer wiring run and having trouble, you can try switching to the 5V power output (both sensors can do 3.3V-5V power input).

### Reading the sensors
For the DS18B20, you'll have to add a line in /boot/config.txt to enable 1-wire:
dtoverlay=w1-gpio
This defaults to GPIO4 (pin 7), but you can also specify:
dtoverlay=w1-gpio,gpiopin=24
Then load the w1-gpio and w1-therm modules (with modprobe, then put them in /etc/modules for future boots)
Then you can scrape the file at /sys/devices/w1_bus_master1/<id>>/w1_slave to get the data.

For the DHT22, it's a bit simpler:  you'll use the Adafruit_DHT22 library in Python to get the temperature and humidity data.  No separate kernel modules or boot parameters.

### Viewing the data
In my case, I set up a free AWS account and ran the script out of /etc/cron.d/ every minute.  The script submits the data to AWS Cloudwatch.  So far with a single metric being submitted every minute and just me viewing, I've stayed below the free threshold.  With four metrics per minute, I should still be within the free tier. 

Then for the actual graphing, I set up a free-tier account at grafana.com.  It would have been simpler to just submit directly to Grafana and skip AWS Cloudwatch, but the free account only graphs metrics and doesn't store them and the Grafana Cloud accounts start at $50/month for about 100x as many metrics as I need.  The free account lets me configure AWS Cloudwatch as a data store and create graphs from there.
