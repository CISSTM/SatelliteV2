import argparse
import logging

from rpi_rf import RFDevice

rfdevice = RFDevice(17)
def send(code):
    rfdevice.enable_tx()
    rfdevice.tx_code(code, 1, 350, 24)
    rfdevice.cleanup()