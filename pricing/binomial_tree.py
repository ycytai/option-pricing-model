import numpy as np

from common.enums import OptionType
from common.exceptions import WrongOptionTypeException
from common.utils import round_num
from obj.base import Option
from pricing.base import PricingModel


class BinominalTreePricingModel(PricingModel):
    @classmethod
    @round_num(digits=4)
    def calculate(
        cls,
        option: Option,
        n: int = 100,
    ) -> float:
        """
        Parameters:
            option (`Option`): option object
            n (`int`): periods
        """

        s = option.spot
        k = option.strike
        v = option.volatility
        t = option.maturity
        r = option.rate
        q = option.yield_rate
        option_type = option.option_type

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
