from abc import ABCMeta, abstractmethod

class JFunction:

    @abstractmethod
    def joint(self, query):
        """

        :param query: nodes to joint
        """
        pass