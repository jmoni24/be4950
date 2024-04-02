import bluetooth
import time
from adafruit_mcp3xxx.mcp3008 import MCP3008
import busio
import digitalio
import board

# Initialize SPI bus
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

# Initialize CS (chip select)
cs = digitalio.DigitalInOut(board.D17)

# Initialize MCP3008 ADC
mcp = MCP3008(spi, cs)

# Create a Bluetooth server socket
server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
server_sock.bind(("", bluetooth.PORT_ANY))
server_sock.listen(1)

# UUID for the Bluetooth service
UUID = "00001101-0000-1000-8000-00805F9B34FB"

# Advertise Bluetooth service
bluetooth.advertise_service(server_sock, "RPiServer", service_id=UUID)

print("Waiting for connection...")
client_sock, client_address = server_sock.accept()
print("Accepted connection from", client_address)

try:
    while True:
        # Read sensor data
        dph = pH.voltage
        dtp1 = temp.voltage
        dip1 = imp.voltage

        # Send sensor data over Bluetooth
        client_sock.send(f"pH:{dph},temp:{dtp1},imp:{dip1}\n")

        # Sleep for a while
        time.sleep(1)
except KeyboardInterrupt:
    print("Closing connection...")
    client_sock.close()
    server_sock.close()
