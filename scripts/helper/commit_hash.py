from abc import ABCMeta, abstractmethod


class CommitHash(object):
    __metaclass__ = ABCMeta

    def __init__(self, directory):
        self.directory = directory

    @abstractmethod
    def __str__(self):
        return ''
