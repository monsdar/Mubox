
import codecs
import fnmatch
import json
import logging
import os

from audiotype.ControlAudioType import ControlAudioType
from audiotype.EffectAudioType import EffectAudioType
from audiotype.MusicAudioType import MusicAudioType

from tagprovider.NfcTagProvider import NfcTagProvider

def main():
    #initing logging from https://docs.python.org/3/howto/logging-cookbook.html
    logger = logging.getLogger('mubox')
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler('/tmp/mubox.log')
    fh.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    logger.addHandler(fh)
    logger.addHandler(ch)

    logger.info("Starting MuBox...")
    try:
        mubox = Mubox()
    except:
        logger.error("Error occured: " + traceback.format_exc())

class Mubox:
    def __init__(self):
        self.logger = logging.getLogger("mubox.Mubox")
        self.currentAudioType = None #this is the currently active AudioType
        
        #Load up all the AudioTypes we want to use
        self.logger.debug("Initing AudioTypes...")
        self.audioTypes = []
        controlAudioType   = ControlAudioType()
        effectAudioType    = EffectAudioType()
        musicAudioType     = MusicAudioType(1, "musicState.json", "music")
        audiobookAudioType = MusicAudioType(0, "audiobookState.json", "audiobook")
        self.audioTypes.append(controlAudioType)
        self.audioTypes.append(effectAudioType)
        self.audioTypes.append(musicAudioType)
        self.audioTypes.append(audiobookAudioType)
        self.logger.debug("...inited " + str(len(self.audioTypes)) + " AudioTypes")
    
        #Init and start TagProvider, subscribe onTagRecognized and onTagRemoved
        self.logger.debug("Initing TagProvider...")
        self.tagProvider = NfcTagProvider()
        self.tagProvider.SubscribeTagRecognized(self.onTagRecognized)
        self.tagProvider.SubscribeTagRemoved(self.onTagRemoved)
        self.logger.debug("...inited TagProvider with " + str(self.tagProvider))
        
        self.logger.debug("Starting TagProvider")
        self.tagProvider.Start()
    
    def onTagRecognized(self, tagContent):
        #check if there is no audiotype active... this should never happen
        if self.currentAudioType:
            self.logger.warning("There should be no active AudioType!")
            return
        
        #load the configs
        tagConfigs = {}
        scriptDir = os.path.dirname(os.path.realpath(__file__))
        matches = []
        for root, dirnames, filenames in os.walk(scriptDir + '/media'):
            for filename in fnmatch.filter(filenames, '*.json'):
                matches.append(os.path.join(root, filename))
        for filepath in matches:
            tagName = os.path.basename(filepath)[:-5]
            self.logger.debug("Loading config for " + tagName)
            tagConfigs[tagName] = json.load(codecs.open(filepath, encoding='utf-8'))
            
        if not tagContent in tagConfigs:
            self.logger.warning("Config for tag " + tagContent + " not found")
            return
        
        #Check which AudioType is responsible
        typeToSearchFor = tagConfigs[tagContent]["type"]
        for type in self.audioTypes:
            if(type.IsResponsible(typeToSearchFor)):
                self.logger.info("Handling '" + tagContent + "' with " + str(type))
                self.currentAudioType = type
                break
        
        if not self.currentAudioType:
            self.logger.warning("Cannot find a fitting AudioType for " + typeToSearchFor)
            return
        
        #Forward config to the AudioType, start its action
        self.currentAudioType.PlayTag(tagContent, tagConfigs[tagContent])
        
    def onTagRemoved(self):
        #Call current AudioType, let it know that the tag has been removed
        if not self.currentAudioType:
            self.logger.error("No active AudioType, cannot stop anything...")
        else:
            self.logger.info("Stopping " + str(self.currentAudioType))
            self.currentAudioType.StopTag()
            self.currentAudioType = None

if __name__ == "__main__":
    main()