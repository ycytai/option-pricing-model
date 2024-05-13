import abc


class PricingModel(abc.ABC):
    @abc.abstractmethod
    def calculate(cls):
        raise NotImplementedError()
