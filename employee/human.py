from abc import ABC, abstractmethod

class Human:
    
    def __init__(self, config):
        self.config = config


    @abstractmethod
    def work():
        pass