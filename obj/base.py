import numpy as np
import scipy.stats as st
from pydantic import BaseModel, Field

from common.enums import OptionType
from common.utils import round_num


class Option(BaseModel):

    spot: float = Field(title='spot price')
    strike: int | float = Field(title='strike price')
    volatility: float = Field(title='interest rate')
    maturity: float = Field(title='volatility')
    rate: float = Field(title='maturity (year)')
    yield_rate: float = Field(title='yield rate')
    option_type: OptionType = Field(title='option type')

    @property
    @round_num()
    def delta(self) -> float:
        if self.option_type == OptionType.Call:
            return st.norm.cdf(self.d1)
        if self.option_type == OptionType.Put:
            return st.norm.cdf(self.d1) - 1

    @property
    @round_num()
    def gamma(self) -> float:
        return st.norm.pdf(self.d1) / (
            self.spot * self.volatility * (self.maturity**0.5)
        )

    @property
    @round_num()
    def theta(self):
        if self.option_type == OptionType.Call:
            return -(self.spot * st.norm.pdf(self.d1) * self.volatility) / (
                2 * self.maturity**0.5
            ) - (
                self.rate
                * self.strike
                * np.exp(-self.rate * self.maturity)
                * st.norm.cdf(self.d2)
            )
        if self.option_type == OptionType.Put:
            return -(self.spot * st.norm.pdf(self.d1) * self.volatility) / (
                2 * self.maturity**0.5
            ) + (
                self.rate
                * self.strike
                * np.exp(-self.rate * self.maturity)
                * st.norm.cdf(-self.d2)
            )

    @property
    @round_num()
    def vega(self) -> float:
        return self.spot * self.maturity**0.5 * st.norm.pdf(self.d1)

    @property
    @round_num()
    def rho(self) -> float:
        if self.option_type == OptionType.Call:
            return (
                self.strike
                * self.maturity
                * np.exp(-self.rate * self.maturity)
                * st.norm.cdf(self.d2)
            )
        if self.option_type == OptionType.Put:
            return (
                -self.strike
                * self.maturity
                * np.exp(-self.rate * self.maturity)
                * st.norm.cdf(-self.d2)
            )

    @property
    @round_num(digits=6)
    def d1(self) -> float:
        var = self.rate - self.yield_rate if self.yield_rate else self.rate
        return (
            np.log(self.spot / self.strike)
            + ((var + self.volatility**2 / 2) * self.maturity)
        ) / (self.volatility * self.maturity**0.5)

    @property
    @round_num(digits=6)
    def d2(self) -> float:
        return self.d1 - (self.volatility * self.maturity**0.5)

    @property
    def greeks(self) -> dict[str, float]:
        return {
            'delta': self.delta,
            'gamma': self.gamma,
            'theta': self.theta,
            'vega': self.vega,
            'rho': self.rho,
        }
