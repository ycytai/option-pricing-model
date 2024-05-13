import math

import pytest

from obj.base import Option
from pricing import (
    BinominalTreePricingModel,
    BlackScholesPricingModel,
    TrinomialTreePricingModel,
)

call_option_1 = Option(
    spot=42,
    strike=40,
    maturity=0.5,
    rate=0.1,
    volatility=0.2,
    yield_rate=0,
    option_type='C',
)

call_option_2 = Option(
    spot=810,
    strike=800,
    maturity=0.5,
    rate=0.05,
    volatility=0.2,
    yield_rate=0.02,
    option_type='C',
)

put_option_1 = Option(
    spot=42,
    strike=40,
    maturity=0.5,
    rate=0.1,
    volatility=0.2,
    yield_rate=0,
    option_type='P',
)

put_option_2 = Option(
    spot=50,
    strike=50,
    maturity=5 / 12,
    rate=0.1,
    volatility=0.4,
    yield_rate=0,
    option_type='P',
)


@pytest.mark.parametrize(
    ['option', 'expected_result'],
    argvalues=[
        pytest.param(call_option_1, 4.76),
        pytest.param(put_option_1, 0.81),
    ],
)
def test_black_scholes_model(
    option: Option,
    expected_result: float,
):
    price = BlackScholesPricingModel.calculate(option=option)
    assert math.isclose(round(price, 2), expected_result)


@pytest.mark.parametrize(
    ['option', 'expected_result'],
    argvalues=[pytest.param(call_option_2, 53.39)],
)
def test_binominal_tree_model(
    option: Option,
    expected_result: float,
):
    price = BinominalTreePricingModel.calculate(option=option, n=2)
    assert math.isclose(round(price, 2), expected_result)


@pytest.mark.parametrize(
    ['option', 'simulation_times', 'expected_result'],
    argvalues=[
        pytest.param(call_option_2, 2, 51.96),
        pytest.param(put_option_2, 5, 3.81),
    ],
)
def test_trinomial_tree_model(
    option: Option,
    simulation_times: int,
    expected_result: float,
):
    price = TrinomialTreePricingModel.calculate(option=option, n=simulation_times)
    assert math.isclose(round(price, 2), expected_result)
