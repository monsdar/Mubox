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

import codecs
import json
import logging
import os
import datetime
from random import randint
from mpd import MPDClient
from audiotype.IAudioType import IAudioType

class MusicAudioType(IAudioType):
    def __init__(self, isRandom, statefile, myType):
        self.isRandom = isRandom #0 = not random, 1 = random
        self.statefile = statefile
        self.myType = myType
        self.currentTag = ""
        self.logger = logging.getLogger("mubox.MusicAudioType")

    def IsResponsible(self, typeIdentifier):
        return typeIdentifier == self.myType
        
    def PlayTag(self, tag, configuration):
        self.currentTag = tag
    
        mpdClient = MPDClient() 
        mpdClient.connect("localhost", 6600)
        mpdClient.clear()
        
        filename = configuration["media"]
        if filename.endswith(".m3u"): #playlists need to be added via .load()
            mpdClient.load(filename)
        else:                         #single audio files need to be added via add()
            mpdClient.add(filename)

        #This will start random AFTER the first song of the playlist has been played
        mpdClient.random(self.isRandom)
        mpdClient.repeat(self.isRandom)
            
        #check if we should continue the music or start random
        if self.ContinuePlaying(tag):
            status = self.GetStatus()
            mpdClient.seek(status["currentSong"], status["currentTime"])
        else:
            if self.isRandom == 0:
                mpdClient.play(0)
            else:
                numSongs = mpdClient.status()["playlistlength"]
                mpdClient.play(randint(0, int(numSongs)-1))
        self.logger.info("Starting to play " + str(mpdClient.currentsong()))
    
    def StopTag(self):
        mpdClient = MPDClient() 
        mpdClient.connect("localhost", 6600)
        
        #store the current song and its position
        self.StoreStatus(mpdClient)
        self.currentTag = ""
        
        #stop and clear mpd
        #we usually do not need to have repeat and random enabled, so turn it off when the tag is being removed
        mpdClient.stop()
        mpdClient.clear()
        mpdClient.repeat(0)
        mpdClient.random(0)
    
    def StoreStatus(self, mpdClient):
        mpdClient.pause(1)
        mpdStatus = mpdClient.status()
        status = {}
        status["currentTag"] = self.currentTag
        status["currentSong"] = mpdStatus["song"]
        status["currentTime"] = mpdStatus["elapsed"]
        status["currentTimestamp"] = self.GetDaysSince1970()
        with open(self.statefile, 'w') as outfile:
            json.dump(status, outfile, ensure_ascii=False)
    
    def HasStatus(self):
        if os.path.isfile(self.statefile):
            return True
        return False
    
    def GetStatus(self):
        if self.HasStatus():
            return json.load(codecs.open(self.statefile, encoding='utf-8'))
            
    def ContinuePlaying(self, givenTag):
        if self.HasStatus():
            state = self.GetStatus()
            isTagEqual = state["currentTag"] == givenTag
            isInTimeframe = (self.GetDaysSince1970() - state["currentTimestamp"]) < 1
            if(isTagEqual and isInTimeframe):
                return True
        return False
        
    def GetDaysSince1970(self):
        return (datetime.datetime.utcnow() - datetime.datetime(1970,1,1)).days
