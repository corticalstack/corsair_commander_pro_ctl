# 🌬️ Corsair Commander Pro Controller (ccpctl)

A Python utility for dynamic control of Corsair Commander Pro fan speeds based on CPU temperature.

## 📝 Description

`ccpctl` is a lightweight command-line tool that automatically adjusts Corsair Commander Pro fan speeds based on real-time CPU temperature readings. It provides a simple way to implement dynamic fan curves without relying on proprietary software, giving you better control over your system's cooling and noise levels.

## ✨ Features

- 🔄 Dynamic fan speed adjustment based on CPU temperature thresholds
- 🌡️ Real-time temperature monitoring using system sensors
- 💡 Fixed LED color control for connected fans
- 📊 Configurable update intervals and temperature change thresholds
- 📝 Detailed logging with multiple verbosity levels

## 🔧 Prerequisites

- Python 3.x
- Corsair Commander Pro device connected to your system
- Linux operating system with temperature sensors configured

## 📦 Dependencies

The following Python packages are required:
```
docopt
psutil
liquidctl
```

## 🚀 Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/corsair_commander_pro_ctl.git
cd corsair_commander_pro_ctl
```

2. Install the required dependencies:
```bash
pip install docopt psutil liquidctl
```

3. Ensure your user has appropriate permissions to access the USB device:
```bash
sudo chmod a+rw /dev/hidraw*
```
Or add a udev rule for more permanent access.

## 📋 Usage

Run the script with:

```bash
python ccpctl.py
```

### Command-line Options

```
Usage:
  ccpctl [options]

Options:
  --interval <seconds>     Update interval in seconds [default: 2]
  -g, --debug              Show debug information on stderr
  -v, --verbose            Output additional information
```

## ⚙️ How It Works

1. The script connects to your Corsair Commander Pro device
2. It continuously monitors the CPU temperature using system sensors
3. Based on temperature thresholds, it adjusts the fan speeds:
   - Higher temperatures (>80°C) → 100% fan speed
   - Lower temperatures (<30°C) → 25% fan speed
   - Various steps in between
4. It sets a fixed blue color for the LEDs on connected fans
5. A temperature change threshold prevents constant speed adjustments for minor fluctuations

## 🔍 Customization

You can modify the following parameters in the code:

- `update_interval`: How often to check temperatures (in seconds)
- `cpu_sensor`: The specific temperature sensor to monitor
- `temp_change_threshold`: Minimum temperature change percentage to trigger fan speed adjustment
- Fan speed thresholds in the `set_fan_speed` method
- LED colors in the `set_fan_led_fixed_colour` method

## 📝 Logging

Logs are saved to `ccpctl.log` in the same directory as the script. Use the `--debug` or `--verbose` flags to increase logging detail.

## 🛠️ Troubleshooting

- If no devices are found, ensure the Commander Pro is properly connected and recognized by the system
- Check that you have the correct permissions to access USB devices
- Verify that your system's temperature sensors are properly configured and accessible

## 📄 License

This project is available as open source under the terms of the [MIT License](https://opensource.org/licenses/MIT).

## 📚 Resources

- [liquidctl Documentation](https://github.com/liquidctl/liquidctl)
- [Corsair Commander Pro Manual](https://www.corsair.com/us/en/Categories/Products/Accessories-%7C-Parts/iCUE-CONTROLLERS/iCUE-COMMANDER-PRO-Smart-RGB-Lighting-and-Fan-Speed-Controller/p/CL-9011110-WW)
