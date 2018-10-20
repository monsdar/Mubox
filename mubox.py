
import codecs
import fnmatch
import json
import os

from audiotype.ControlAudioType import ControlAudioType
from audiotype.EffectAudioType import EffectAudioType
from audiotype.MusicAudioType import MusicAudioType

from tagprovider.NfcTagProvider import NfcTagProvider

def main():
    mubox = Mubox()

class Mubox:
    def __init__(self):
        self.currentAudioType = None #this is the currently active AudioType
        
        #Load up all the AudioTypes we want to use
        self.audioTypes = []
        controlAudioType   = ControlAudioType()
        effectAudioType    = EffectAudioType()
        musicAudioType     = MusicAudioType(1, "musicState.json", "music")
        audiobookAudioType = MusicAudioType(0, "audiobookState.json", "audiobook")
        
        self.audioTypes.append(controlAudioType)
        self.audioTypes.append(effectAudioType)
        self.audioTypes.append(musicAudioType)
        self.audioTypes.append(audiobookAudioType)
    
        #Init and start TagProvider, subscribe onTagRecognized and onTagRemoved
        self.tagProvider = NfcTagProvider()
        self.tagProvider.SubscribeTagRecognized(self.onTagRecognized)
        self.tagProvider.SubscribeTagRemoved(self.onTagRemoved)
        self.tagProvider.Start()
    
    def onTagRecognized(self, tagContent):
        #check if there is no audiotype active... this should never happen
        if self.currentAudioType:
            print("Error! There should be no active AudioType!")
            return
        
        #load the configs
        tagConfigs = {}
        scriptDir = os.path.dirname(os.path.realpath(__file__))
        matches = []
        for root, dirnames, filenames in os.walk('media'):
            for filename in fnmatch.filter(filenames, '*.json'):
                matches.append(os.path.join(root, filename))
        for filepath in matches:
            tagName = os.path.basename(filepath)[:-5]
            print("Loading config for " + tagName)
            tagConfigs[tagName] = json.load(codecs.open(filepath, encoding='utf-8'))
            
        if not tagContent in tagConfigs:
            print("Config for tag " + tagContent + " not found")
            return
        
        #Check which AudioType is responsible
        typeToSearchFor = tagConfigs[tagContent]["type"]
        for type in self.audioTypes:
            if(type.IsResponsible(typeToSearchFor)):
                print("Handling '" + tagContent + "' with " + str(type))
                self.currentAudioType = type
                break
        
        if not self.currentAudioType:
            print("Cannot find a fitting AudioType for " + typeToSearchFor)
            return
        
        #Forward config to the AudioType, start its action
        self.currentAudioType.PlayTag(tagContent, tagConfigs[tagContent])
        
    def onTagRemoved(self):
        #Call current AudioType, let it know that the tag has been removed
        if not self.currentAudioType:
            print("Error! No active AudioType, cannot stop anything...")
        else:
            print("Stopping " + str(self.currentAudioType))
            self.currentAudioType.StopTag()
            self.currentAudioType = None

if __name__ == "__main__":
    main()