import numpy as np
from pricing.common.enums import OptionType
from pricing.common.base import PricingModel
from pricing.common.exceptions import WrongOptionTypeException


class BinominalTreePricingModel(PricingModel):

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

        NOTE: European only
        """

        delta_t = t / n
        u = np.exp(v * np.sqrt(delta_t))
        d = np.exp(-v * np.sqrt(delta_t))
        p = (np.exp((r - q) * delta_t) - d) / (u - d)

        asset_price = [s * (u**j) * (d ** (n - j)) for j in range(n + 1)]

        if option_type == OptionType.Call:
            option_price = [max(s - k, 0) for s in asset_price]
        elif option_type == OptionType.Put:
            option_price = [max(k - s, 0) for s in asset_price]
        else:
            raise WrongOptionTypeException(user_input=option_type)

        option_tree = [[] for _ in range(n)]
        option_tree.append(option_price)

        for i in range(1, n + 1):
            last_level = option_tree[n - i + 1]

            for j in range(1, len(last_level)):
                down_price = last_level[j - 1]
                up_price = last_level[j]

                option_tree[n - i].append(
                    np.exp(-r * delta_t) * (up_price * p + down_price * (1 - p))
                )

        return option_tree[0][0]