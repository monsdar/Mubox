#!/usr/bin/env python3

'''
This AudioType only prints some info onto the console
'''

from audiotype.IAudioType import IAudioType

class MockAudioType(IAudioType):
    def __init__(self):
        self.currentTag = ""
        self.currentConfig = None
        
    def IsResponsible(self, typeIdentifier): #this type can handle any typestrings
        return True
        
    def PlayTag(self, tag, configuration):
        self.currentTag = tag
        self.currentConfig = configuration
        print("Playing tag '" + tag + "' with config: " + configuration)
    
    def StopTag(self):
        print("Stopping to play tag '" + self.currentTag + "'")