import numpy as np
from pricing.common.enums import OptionType
from pricing.common.base import PricingModel
from pricing.common.exceptions import WrongOptionTypeException


class MonteCarloPricingModel(PricingModel):

    @classmethod
    def calculate(
        cls,
        s: float,
        k: float,
        t: float,
        r: float,
        mu: float,
        sigma: float,
        m: int,
        n: int,
        option_type: OptionType,
    ) -> float:
        """
        Parameters:
            s: spot price
            k: strike price
            t: maturity (year)
            r: interest rate
            mu: mean of underlying asset price return 
            sigma: volatility of underlying asset price return
            m: simulation times
            n: periods
            option_type: option type, use 'C' or 'P'
        """

        delta_t = t / n
        simulation_results = []
        for _ in range(m):
            price_path = [s]
            current_price = s

            for _ in range(n):

                epsilon = np.random.standard_normal()
                change = (mu * current_price * delta_t) + (sigma * current_price * epsilon * delta_t**0.5)
                current_price += change
                price_path.append(current_price)

            simulation_results.append(price_path[-1])

        if option_type == OptionType.Call:
            option_price = sum([max(simulation_price - k, 0) for simulation_price in simulation_results]) / m

        elif option_type == OptionType.Put:
            option_price = sum([max(k - simulation_price, 0) for simulation_price in simulation_results]) / m

        else:
            raise WrongOptionTypeException(user_input=option_type)

        option_price = option_price*np.exp(-r*t)
        return option_price
