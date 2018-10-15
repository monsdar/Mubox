
import glob
import os

from audiotype.ControlAudioType import ControlAudioType
from audiotype.EffectAudioType import EffectAudioType
from audiotype.AudiobookAudioType import AudiobookAudioType
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
        audiobookAudioType = AudiobookAudioType()
        musicAudioType     = MusicAudioType()
        self.audioTypes.append(controlAudioType)
        self.audioTypes.append(effectAudioType)
        self.audioTypes.append(audiobookAudioType)
        self.audioTypes.append(musicAudioType)
    
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
        for filepath in glob.glob(scriptDir + '/media/*.json'):
            tagName = os.path.filename(filepath)
            tagConfigs[tagName] = json.load(filepath)
            
        if not tagContent in tagConfigs:
            print("Config for tag " + tagContent + " not found")
            return
        
        #Check which AudioType is responsible
        typeToSearchFor = tagConfigs[tagContent]
        for type in self.audioTypes:
            if(type.IsResponsible(typeToSearchFor)):
                self.currentAudioType = type
                break
        
        #Forward config to the AudioType, start its action
        self.currentAudioType.PlayTag(tagContent, tagConfigs[tagContent["specific"]])
        
    def onTagRemoved(self):
        #Call current AudioType, let it know that the tag has been removed
        if not self.currentAudioType:
            print("Error! No active AudioType, cannot stop anything...")
        else:
            self.currentAudioType.StopTag()
            self.currentAudioType = None

if __name__ == "__main__":
    main()