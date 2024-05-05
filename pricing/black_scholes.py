import numpy as np
import scipy.stats as st
from pricing.common.enums import OptionType
from pricing.common.base import PricingModel
from pricing.common.exceptions import WrongOptionTypeException


class BlackScholesPricingModel(PricingModel):

    @classmethod
    def calculate(
        cls,
        s: float, 
        k: float, 
        t: float,
        r: float, 
        v: float, 
        q: float, 
        option_type: str
    ):

        """
        Parameters:
            s: spot price
            k: strike price
            t: maturity (year)
            r: interest rate
            v: volatility
            q: yield rate
            option_type: option type, use 'C' or 'P'
        """

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
