

import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
import time
import pigpio
from adafruit_mcp3xxx.analog_in import AnalogIn
from time import sleep
# create the spi bus
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

# create the cs (chip select)
cs = digitalio.DigitalInOut(board.D17)

# create the mcp object
mcp = MCP.MCP3008(spi, cs)

# create an analog input channel on pin 0
pH = AnalogIn(mcp, MCP.P2)
temp = AnalogIn(mcp,MCP.P1)
temp2 = AnalogIn(mcp,MCP.P0)
imp = AnalogIn(mcp, MCP.P4)



while True:
	print("ADC Voltage 3: " + str(pH.voltage))
	sleep(1)

pi.stop()
