import os
import sys
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
import time
import json
from datetime import datetime

# create the spi bus
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

# create the cs (chip select)
cs = digitalio.DigitalInOut(board.D5)

# create the mcp object
mcp = MCP.MCP3008(spi, cs)

pins = sys.argv[1]
pins = list(pins)
pins = [int(x) for x in pins]

def choose_pin(p):
    global mcp
    if p == 0:
        return AnalogIn(mcp, MCP.P0)
    elif p == 1:
        return AnalogIn(mcp, MCP.P1)
    elif p == 2:
        return AnalogIn(mcp, MCP.P2)
    elif p == 3:
        return AnalogIn(mcp, MCP.P3)
    elif p == 4:
        return AnalogIn(mcp, MCP.P4)
    elif p == 5:
        return AnalogIn(mcp, MCP.P5)
    elif p == 6:
        return AnalogIn(mcp, MCP.P6)
    elif p == 7:
        return AnalogIn(mcp, MCP.P7)
    elif p == 8:
        return AnalogIn(mcp, MCP.P8)
    else:
        raise ValueError
    
pin_profiles = {}

for p in pins:
    
    print(f"\n[Starting Calibration for Pin]: {p}")
    dry_samples = []
    wet_samples = []
    # create an analog input channel
    chan = choose_pin(p)
    print("[Dry test. Please ensure the sensor is dry]")
    print("[10 samples will be taken]")
    input("[Press Enter to Continue...]")
    for i in range(10):
        d_val = chan.value
        print(f"[Dry ADC value]: {d_val}")
        dry_samples.append(d_val)
        time.sleep(0.5)
    os.system('cls||clear')    
    print("[Wet test. Please ensure the sensor is submerged]")
    print("[10 samples will be taken]")
    input("[Press Enter to Continue...]")
    for i in range(10):
        w_val = chan.value
        print(f"[Wet ADC value]: {w_val}")
        wet_samples.append(w_val)
        time.sleep(0.5)
    
    d_max = max(dry_samples)
    w_min = min(wet_samples)
    
    pin_profiles[p]={
        "max_value": d_max,
        "min_value": w_min
    }

dt = datetime.today().strftime('%d-%m-%Y--%H.%M.%S')
filename = "calibration_data" + dt +".json"
with open(filename, 'w') as fp:
    json.dump(pin_profiles, fp)