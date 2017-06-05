from abc import ABCMeta, abstractmethod


class CommitHash(object):
    __metaclass__ = ABCMeta

    def __init__(self, directory: str) -> None:
        self.directory = ''

    @abstractmethod
    def __str__(self) -> str:
        return ''
