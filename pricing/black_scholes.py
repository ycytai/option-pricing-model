import numpy as np
import scipy.stats as st

from common.enums import OptionType
from common.exceptions import WrongOptionTypeException
from common.utils import round_num
from obj.base import Option
from pricing.base import PricingModel


class BlackScholesPricingModel(PricingModel):
    @classmethod
    @round_num(digits=4)
    def calculate(cls, option: Option):
        """
        Parameter:
            option (`Option`): option object
        """
        s = option.spot
        k = option.strike
        v = option.volatility
        t = option.maturity
        r = option.rate
        q = option.yield_rate
        option_type = option.option_type

        d1 = (np.log(s / k) + (r - q + v**2 / 2) * t) / (v * t**0.5)
        d2 = d1 - v * t**0.5

        call = s * st.norm.cdf(d1) - k * np.exp(-r * t) * st.norm.cdf(d2)
        put = k * np.exp(-r * t) * st.norm.cdf(-d2) - s * st.norm.cdf(-d1)

        if option_type == OptionType.Call:
            return max(call, 0)
        elif option_type == OptionType.Put:
            return max(put, 0)
        else:
            raise WrongOptionTypeException(user_input=option_type)
