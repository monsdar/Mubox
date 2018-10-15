#!/usr/bin/env python3

'''
This TagProvider plays a predefined scenario of tags being added/removed for testing purposes
'''

import time
from tagprovider.ITagProvider import ITagProvider

class MockTagProvider(ITagProvider):
    def __init__(self):
        self.onTagRecognized = None
        self.onTagRemoved = None

    def SubscribeTagRecognized(self, onTagRecognized):
        self.onTagRecognized = onTagRecognized
        
    def SubscribeTagRemoved(self, onTagRemoved):
        self.onTagRemoved = onTagRemoved
        
    def Start(self):
        self.onTagRecognized("Test")
        time.sleep(1.0)
        self.onTagRemoved()
        time.sleep(1.0)
        self.onTagRecognized("Test")
        time.sleep(1.0)
        self.onTagRemoved()
        
    def Stop(self):
        pass