# Home-automation-with-Google-assistant

This project uses a Raspberry Pi to create a home automation system that can be controlled using Google Assistant. It monitors power consumption for two loads and uses relays to control them. The system integrates sensors for current measurement and utilizes the Thingspeak API to log data and receive control commands remotely.

Features

Google Assistant Control: Control home appliances remotely using commands via the Thingspeak API.

Power Monitoring: Monitors real-time power consumption (in watts) for two loads.

Overload Protection: Automatically turns off relays when load exceeds a threshold.

Notifications: Buzzers alert when a condition is met (like overload or specific events).

Data Logging: Sends power usage data to Thingspeak for real-time tracking.

Components Used

Raspberry Pi: The central controller running the Python scripts.

MCP3208 ADC: Analog-to-digital converter to read sensor data.

Relays: Two relays used to control the two connected loads.

Sensors: Used to monitor current for both loads.

Buzzer: Alerts the user when an overload condition occurs.

Thingspeak API: Used for logging data and receiving commands from Google Assistant.

Circuit Setup

Raspberry Pi GPIO:

Relay 1: Connected to GPIO pin 2.

Relay 2: Connected to GPIO pin 3.

Buzzer: Connected to GPIO pin 26.

Current Sensors: Connected to MCP3208 ADC (channels 0 and 1).

Fridge Detection: Connected to GPIO pin 19.

Current Sensors:

MCP3208 is used to read analog data from the current sensors.

The sensors detect the current passing through each load and calculate the power consumption.

How the System Works

The Raspberry Pi continuously monitors current values from the two loads using the MCP3208 ADC.

The system calculates the power consumption of both loads and logs the data to the Thingspeak API.

Google Assistant sends control commands to the system via the Thingspeak API to turn devices ON or OFF.

When certain conditions are met (such as overloads or fridge detection), the system triggers a buzzer and shuts off the load to prevent damage.
