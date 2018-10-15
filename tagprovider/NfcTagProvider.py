
'''
This TagProvider uses NFC to provide tagging events
'''

import Adafruit_PN532 as PN532
import binascii
import re
import time
from tagprovider.ITagProvider import ITagProvider

# Setup how the PN532 is connected to the Raspbery Pi
# It is recommended to use a software SPI connection with 4 digital GPIO pins.
# Configuration for a Raspberry Pi:
CS   = 22
MOSI = 23
MISO = 24
SCLK = 25

class NfcTagProvider(ITagProvider):
    def __init__(self):
        self.onTagRecognized = None
        self.onTagRemoved = None
        self.uid = None #this is the unique ID of the current tag that is present. None if no tag is present
        self.isRunning = False
        self.pn532 = self.initNfcReader()

    def SubscribeTagRecognized(self, onTagRecognized):
        self.onTagRecognized = onTagRecognized
        
    def SubscribeTagRemoved(self, onTagRemoved):
        self.onTagRemoved = onTagRemoved
        
    def Start(self):
        self.isRunning = True
        while(self.isRunning):
            cycleRead(self.pn532)
            
    def Stop(self):
        self.isRunning = False

    def initNfcReader(self):
        # Note: By using the NTAG203 compatible version of Adafruit_PN532 we do not need auth
        # See: https://github.com/laricchia/Adafruit_Python_PN532/
        pn532 = PN532.PN532(cs=CS, sclk=SCLK, mosi=MOSI, miso=MISO)
        pn532.SAM_configuration()
        pn532.begin()
        ic, ver, rev, support = pn532.get_firmware_version()
        print('...found PN532 with firmware version: {0}.{1}'.format(ver, rev))
        return pn532
    
    def cycleRead(self, givenReader):
        self.uid = getNfcTagBlocking(givenReader)
        text = readTextFromTag(givenReader)
        if not text:
            return
        
        self.onTagRecognized(text)
        
        while(getNfcTag(givenReader) == uid): #calling getNfcTag will block for the duration of timeout
            pass #immediately query for the next nfc tag again. No time to waste through waiting...
        
        #when we land here the tag has been removed
        self.onTagRemoved()
    
    def readTextFromTag(self, givenReader):
        # This is a quite complicated way to read from an NTAG203... Probably it's much easier
        # to just change how data is read from the tag and then use the specification to figure out
        # which part contains the content.
        # Last but not least converting the actual content from bytearray to the readable string
        # should also be much easier
        # ...but whatever works -\_(o.o)_/-
        try:
            dataByteStr = ""
            for frame in [0,4,8]:
                data = givenReader.mifare_classic_read_block(frame)
                if not data:
                    print("Cannot read data!")
                    continue
                dataByteStr += binascii.hexlify(data)
            reResult = re.search('.*5402....(.*)fe', dataByteStr)
            contentAsByteString = reResult.group(1)
            return binascii.unhexlify(contentAsByteString)
        except:
            return None
        
    def getNfcTag(self, givenReader, timeout=.2):
        return givenReader.read_passive_target(timeout_sec=timeout)
    
    def getNfcTagBlocking(self, givenReader):
        uid = None
        while not uid:
            uid = givenReader.read_passive_target(timeout_sec=1)
        return uid