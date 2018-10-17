#!/usr/bin/env python3

'''
This AudioType is optimized to play music
 * Single Songs:
    * Song gets repeated forever
    * Replacing the same tag will continue the song from where it left off
      After a configurable amount of time the song will play from the start again
 * Playlists
    * Random song from the playlist is played
    * After the song ends the next random song gets started
    * Replacing the same tag will continue the song from where it left off
      After a configurable amount of time the song will play from the start again
'''

from mpd import MPDClient
from audiotype.IAudioType import IAudioType

class MusicAudioType(IAudioType):
    def __init__(self):
        pass

    def IsResponsible(self, typeIdentifier):
        return typeIdentifier == "music"
        
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
