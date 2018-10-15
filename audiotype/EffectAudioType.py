#!/usr/bin/env python3

'''
This AudioType plays a given sound effect once. The effect does not stop when removing the tag
'''

from mpd import MPDClient
from audiotype.IAudioType import IAudioType

class EffectAudioType(IAudioType):
    def __init__(self):
        pass

    def IsResponsible(self, typeIdentifier):
        return typeIdentifier == "effect"
        
    def PlayTag(self, tag, configuration):
        print("Playing effect for " + configuration["media"])
        mpdClient = MPDClient() 
        mpdClient.connect("localhost", 6600)
        mpdClient.clear()
        mpdClient.add(configuration["media"])
        mpdClient.play(0)
    
    def StopTag(self):
        mpdClient = MPDClient() 
        mpdClient.connect("localhost", 6600)
        mpdClient.clear()