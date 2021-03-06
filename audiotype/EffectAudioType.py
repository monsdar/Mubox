#!/usr/bin/env python3

'''
This AudioType plays a given sound effect once. The effect does not stop when removing the tag
'''

import logging
from mpd import MPDClient
from audiotype.IAudioType import IAudioType

class EffectAudioType(IAudioType):
    def __init__(self):
        self.logger = logging.getLogger("mubox.EffectAudioType")

    def IsResponsible(self, typeIdentifier):
        return typeIdentifier == "effect"
        
    def PlayTag(self, tag, configuration):
        self.logger.info("Playing effect for " + configuration["media"])
        mpdClient = MPDClient() 
        mpdClient.connect("localhost", 6600)
        mpdClient.clear()
        mpdClient.add(configuration["media"])
        
        mpdClient.random(0)
        mpdClient.repeat(0)
        mpdClient.play(0)
    
    def StopTag(self):
        mpdClient = MPDClient() 
        mpdClient.connect("localhost", 6600)
        mpdClient.clear()