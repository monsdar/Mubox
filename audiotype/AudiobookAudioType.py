#!/usr/bin/env python3

'''
This AudioType is optimized for playing audiobooks

 * It will start to play the given playlist in order of their configuration
 * If the tag is replaced it will continue to play from where it left off
 * After a configurable amount of time the audiobook will start to play from the beginning again
'''

from mpd import MPDClient
from audiotype.IAudioType import IAudioType

class AudiobookAudioType(IAudioType):
    def __init__(self):
        pass

    def IsResponsible(self, typeIdentifier):
        return typeIdentifier == "audiobook"
        
    def PlayTag(self, tag, configuration):
        mpdClient = MPDClient() 
        mpdClient.connect("localhost", 6600)
        mpdClient.clear()
        
        filename = configuration["media"]
        if filename.endswith(".m3u"): #playlists need to be added via .load()
            mpdClient.load(filename)
        else:                         #single audio files need to be added via add()
            mpdClient.add(filename)
        mpdClient.play(0)
    
    def StopTag(self):
        mpdClient = MPDClient() 
        mpdClient.connect("localhost", 6600)
        mpdClient.stop()
        mpdClient.clear()
