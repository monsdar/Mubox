#!/usr/bin/env python3

'''
This AudioType is used to control the player. By placing a tag of this type a number of predefined actions
can be executed. Examples:
 * Setting the volume to a specific level
 * Shutdown the system
'''

import os
import time

from mpd import MPDClient
from audiotype.IAudioType import IAudioType

class ControlAudioType(IAudioType):
    def __init__(self):
        pass

    def IsResponsible(self, typeIdentifier):
        return typeIdentifier == "control"
        
    def PlayTag(self, tag, configuration):
        mpdClient = MPDClient() 
        mpdClient.connect("localhost", 6600)
        mpdClient.clear()
        mpdClient.add(configuration["media"])
        
        mpdClient.random(0)
        mpdClient.repeat(0)
        mpdClient.play(0)
        
        time.sleep(configuration["specific"]["waittime_sec"])
        os.system(configuration["specific"]["command"])
    
    def StopTag(self):
        pass #do nothing, let the sound effect play to its end...
