from http.server import BaseHTTPRequestHandler, HTTPServer
# imports for sensors
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
import time
import pigpio
import json
from adafruit_mcp3xxx.analog_in import AnalogIn
import threading
#from time import sleep

# create readouts for pi sensors
# create the spi bus
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
# create the cs (chip select)
cs = digitalio.DigitalInOut(board.D17)
# create the mcp object
mcp = MCP.MCP3008(spi, cs)
# create an analog input channel on pin 0
pH = AnalogIn(mcp, MCP.P2)
temp = AnalogIn(mcp, MCP.P1)
temp2 = AnalogIn(mcp, MCP.P0)
imp = AnalogIn(mcp, MCP.P4)

# pH value
dph = pH.voltage
# temperature value
dtp1 = temp.voltage
# impedance value
dip1 = imp.voltage

class MyHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        responsePh = {'pH': dph}
        responseTemp = {'temp': dtp1}
        responseImp = {'imp': dip1}
        self.wfile.write(json.dumps(responsePh).encode())
        self.wfile.write(json.dumps(responseTemp).encode())
        self.wfile.write(json.dumps(responseImp).encode())
        
        #self.wfile.write(str(dtp1).encode())
        #self.wfile.write(str(dip1).encode())
def run(server_class=HTTPServer, handler_class=MyHTTPRequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print('Starting server on port', port)
    httpd.serve_forever()

if __name__ == '__main__':
    run()
