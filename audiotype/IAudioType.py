#!/usr/bin/env python3

'''
Interface for all AudioTypes

Each audio type has a basic config that contains the following fields:
 * Type - The exact type that should be used to play this tag
 * Audio - The audio file that should be played. Could be either a single file or a playlist
 * Custom - Configuration that is specific for the selected AudioType
'''

from abc import ABCMeta, abstractmethod

class IAudioType:
    @abstractmethod
    def IsResponsible(self, typeIdentifier):
        raise NotImplementedError
    @abstractmethod
    def PlayTag(self, tag, configuration):
        raise NotImplementedError
    @abstractmethod
    def StopTag(self):
        raise NotImplementedError