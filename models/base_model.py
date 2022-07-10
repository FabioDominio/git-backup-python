from abc import ABC, abstractmethod

class BaseModel(ABC):

    @abstractmethod
    def getNamespaces(self):
        # Retrieve the namespaces
        pass

    @abstractmethod
    def getNamespaceRepositories(self, id: str):
        # Retrieve the namespaces
        pass