""""ccpctl – Corsair Commader Pro dynamic control of fans
Usage:
  ccpctl [options]

Options:
  --interval <seconds>     Update interval in seconds [default: 2]
  -g, --debug              Show debug information on stderr
  -v, --verbose            Output additional information
Changelog:
  0.1  WIP
"""
import sys
import psutil
import time
import liquidctl
import logging
from docopt import docopt
import os

VERSION = '0.1'

LOGGER = logging.getLogger(__name__)


class Controller:
    def __init__(self):
        self.update_interval = 2  # Number of seconds
        self.cpu_sensor = 'k10temp.tctl'
        self.device_name = 'commander pro'
        self.devices = self.get_devices(self.device_name)
        if not self.devices:
            LOGGER.error('No devices found')
            raise SystemExit('No devices matches available drivers and selection criteria')

        self.channels = ['fan1', 'fan2', 'fan3', 'fan4', 'fan5', 'fan6']

        self.temp_change_threshold = 5
        self.last_sensor_temp = 100
        self.last_duty = 100

        try:
            status = {}
            for d in self.devices:
                d.connect()
                self.set_fan_led_fixed_colour(d)
            while True:
                for d in self.devices:
                    d.initialize()
                    status[d.description] = d.get_status()  # This gives fan speed
                    sensor_temp = self.get_sensor_temp(self.cpu_sensor)
                    self.set_fan_speed(d, int(sensor_temp))
                    time.sleep(args['--interval'])
        except KeyboardInterrupt:
            pass
        finally:
            for d in self.devices:
                d.disconnect()

    @staticmethod
    def get_devices(device_name):
        return list(liquidctl.find_liquidctl_devices(match=device_name))

    @staticmethod
    def get_sensor_temp(sensor):
        sensors = {}
        try:
            for m, li in psutil.sensors_temperatures().items():
                for label, current, _, _ in li:
                    sensor_name = label.lower().replace(' ', '_')
                    sensors[f'{m}.{sensor_name}'] = current

            if sensor in sensors:
                return sensors[sensor]
        except:
            pass

    @staticmethod
    def set_fan_led_fixed_colour(d):
        d.set_color('led1', 'fixed', colors=[[0x00, 0x00, 0xff]], start_led=1, maximum_leds=64)
        d.set_color('led2', 'fixed', colors=[[0x00, 0x00, 0xff]], start_led=1, maximum_leds=48)

    def set_fan_speed(self, device, sensor_temp):
        duty = 100
        if sensor_temp > 80:
            duty = 100
        elif sensor_temp > 75:
            duty = 95
        elif sensor_temp > 70:
            duty = 85
        elif sensor_temp > 65:
            duty = 75
        elif sensor_temp > 60:
            duty = 65
        elif sensor_temp > 55:
            duty = 55
        elif sensor_temp > 50:
            duty = 45
        elif sensor_temp > 45:
            duty = 40
        elif sensor_temp > 40:
            duty = 35
        elif sensor_temp > 35:
            duty = 30
        elif sensor_temp > 30:
            duty = 25
        elif sensor_temp > 0:
            duty = 20
        change = abs(((sensor_temp - self.last_sensor_temp) / self.last_sensor_temp) * 100)
        if int(self.last_sensor_temp) != int(sensor_temp):
            LOGGER.info('Temperature change from {} to {}'.format(self.last_sensor_temp, sensor_temp))
        self.last_sensor_temp = sensor_temp
        if (change > self.temp_change_threshold) and (duty != self.last_duty):
            self.last_duty = duty
            LOGGER.info('Temp change threshold exceeded, current temp is {} so speed set at {}'.format(sensor_temp,
                                                                                                       str(duty)))
            for c in self.channels:
                device.set_fixed_speed(channel=c, duty=duty)



if __name__ == "__main__":
    args = docopt(__doc__)
    logfile = os.path.dirname(os.path.realpath(__file__)) + '/ccpctl.log'
    if args['--debug']:
        logging.basicConfig(level=logging.DEBUG, filename=logfile, format='[%(levelname)s] %(name)s: %(message)s')
    elif args['--verbose']:
        logging.basicConfig(level=logging.WARNING, filename=logfile, format='%(levelname)s: %(message)s')
        LOGGER.setLevel(logging.INFO)
    else:
        LOGGER.setLevel(logging.WARNING)
        logging.basicConfig(level=logging.WARNING, filename=logfile, format='%(levelname)s: %(message)s')
        sys.tracebacklimit = 0

    controller = Controller()
