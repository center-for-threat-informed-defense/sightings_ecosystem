import abc


class TransformInterface(abc.ABC):
    @abc.abstractmethod
    def transform(self, model):
        pass  # pragma: no covers
