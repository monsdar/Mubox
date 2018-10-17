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

from random import randint
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

        #This will start random AFTER the first song of the playlist has been played
        mpdClient.random(1)
        mpdClient.repeat(1)
        #choose a random first song
        numSongs = mpdClient.status()["playlistlength"]
        print(numSongs)
        mpdClient.play(randint(0, int(numSongs)-1))
        print("Starting to play " + str(mpdClient.currentsong()))
    
    def StopTag(self):
        mpdClient = MPDClient() 
        mpdClient.connect("localhost", 6600)
        mpdClient.stop()
        mpdClient.clear()
