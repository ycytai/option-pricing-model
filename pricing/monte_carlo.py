import numpy as np

from common.enums import OptionType
from common.exceptions import WrongOptionTypeException
from common.utils import round_num
from obj.base import Option
from pricing.base import PricingModel


class MonteCarloPricingModel(PricingModel):
    @classmethod
    @round_num(digits=4)
    def calculate(
        cls,
        option: Option,
        mu: float = 0,
        m: int = 100,
        n: int = 1_000,
    ) -> float:
        """
        Parameters:
            option (`Option`): option object
            mu (`int`): mean of underlying asset price return
            m (`int`): simulation times
            n (`int`): periods
        """

        s = option.spot
        k = option.strike
        t = option.maturity
        r = option.rate
        option_type = option.option_type
        sigma = option.volatility

        delta_t = t / n
        simulation_results = []
        for _ in range(m):
            price_path = [s]
            current_price = s

            for _ in range(n):

                epsilon = np.random.standard_normal()
                change = (mu * current_price * delta_t) + (
                    sigma * current_price * epsilon * delta_t**0.5
                )
                current_price += change
                price_path.append(current_price)

            simulation_results.append(price_path[-1])

        if option_type == OptionType.Call:
            option_price = (
                sum(
                    [
                        max(simulation_price - k, 0)
                        for simulation_price in simulation_results
                    ]
                )
                / m
            )

        elif option_type == OptionType.Put:
            option_price = (
                sum(
                    [
                        max(k - simulation_price, 0)
                        for simulation_price in simulation_results
                    ]
                )
                / m
            )

        else:
            raise WrongOptionTypeException(user_input=option_type)

        option_price = option_price * np.exp(-r * t)
        return option_price
