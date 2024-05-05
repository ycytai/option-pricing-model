import numpy as np
from pricing.common.enums import OptionType
from pricing.common.base import PricingModel
from pricing.common.exceptions import WrongOptionTypeException


class TrinomialTreePricingModel(PricingModel):

    @classmethod
    def calculate(
        cls,
        s: float,
        k: float,
        t: float,
        r: float,
        v: float,
        q: float,
        n: int,
        option_type: OptionType,
    ) -> float:
        """
        Parameters:
            s: spot price
            k: strike price
            t: maturity (year)
            r: interest rate
            v: volatility
            q: yield rate
            n: periods
            option_type: option type, use 'C' or 'P'
        """

        delta_t = t / n
        u = np.exp(v*np.sqrt(3*delta_t))
        d = 1 / u
        p_d = -np.sqrt(delta_t/(12*v**2))*(r-q-v**2/2) + 1/6
        p_u = np.sqrt(delta_t/(12*v**2))*(r-q-v**2/2) + 1/6
        p_m = 2/3

        asset_price =  [s*d**(n-i) for i in range(n)] + [s] + [s*u**(i) for i in range(1, n+1)]

        if option_type == OptionType.Call:
            option_price = [max(s - k, 0) for s in asset_price]
        elif option_type == OptionType.Put:
            option_price = [max(k - s, 0) for s in asset_price]
        else:
            raise WrongOptionTypeException(user_input=option_type)

        option_tree = [[] for _ in range(n)]
        option_tree.append(option_price)
        for i in range(1, n+1):
            last_level = option_tree[n-i+1]

            for j in range(2, len(last_level)):
                down_price = last_level[j-2]
                middle_price = last_level[j-1]
                up_price = last_level[j]

                option_tree[n-i].append(
                    np.exp(-r*delta_t)*(up_price*p_u + middle_price*p_m + down_price*p_d)
                )

        return option_tree[0][0]
