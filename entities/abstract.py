from abc import ABC, abstractmethod

class Abstract(ABC):
    @abstractmethod
    def describe(self) -> str: ...
    @abstractmethod
    def record(self) -> str: ...