#!/usr/bin/env python3

'''
Interface to define how tags are provided to the system
'''

from abc import ABCMeta, abstractmethod

class ITagProvider:
    @abstractmethod
    def SubscribeTagRecognized(self, onTagRecognized):
        raise NotImplementedError
        
    @abstractmethod
    def SubscribeTagRemoved(self, onTagRemoved):
        raise NotImplementedError
        
    @abstractmethod
    def Start(self):
        raise NotImplementedError
        
    @abstractmethod
    def Stop(self):
        raise NotImplementedError