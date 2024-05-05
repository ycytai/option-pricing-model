from pricing import BlackScholesPricingModel, BinominalTreePricingModel, TrinomialTreePricingModel, MonteCarloPricingModel
import pytest
import math



@pytest.mark.parametrize(
    ['s', 'k', 't', 'r', 'v', 'q', 'option_type', 'expected_result'],
    argvalues=[
        pytest.param(42, 40, 0.5, 0.1, 0.2, 0, 'C', 4.76),
        pytest.param(42, 40, 0.5, 0.1, 0.2, 0, 'P', 0.81),
    ]
)
def test_black_scholes_model(
    s: float, k: float, t: float, r: float, 
    v: float, q: float, option_type: str, expected_result: float
):
    price = BlackScholesPricingModel.calculate(
        s, k, t, r, v, q, option_type
    )
    assert math.isclose(round(price, 2), expected_result)


@pytest.mark.parametrize(
    ['s', 'k', 't', 'r', 'v', 'q', 'n', 'option_type', 'expected_result'],
    argvalues=[
        pytest.param(810, 800, 0.5, 0.05, 0.2, 0.02, 2, 'C', 53.39)
    ]
)
def test_binominal_tree_model(
    s: float, k: float, t: float, r: float, 
    v: float, q: float, n:int, option_type: str, expected_result: float
):
    price = BinominalTreePricingModel.calculate(
        s, k, t, r, v, q, n, option_type
    )
    assert math.isclose(round(price, 2), expected_result)


@pytest.mark.parametrize(
    ['s', 'k', 't', 'r', 'v', 'q', 'n', 'option_type', 'expected_result'],
    argvalues=[
        pytest.param(810, 800, 0.5, 0.05, 0.2, 0.02, 2, 'C', 51.96),
        pytest.param(50, 50, 5/12, 0.1, 0.4, 0, 5, 'P', 3.81)
    ]
)
def test_binominal_tree_model(
    s: float, k: float, t: float, r: float, 
    v: float, q: float, n:int, option_type: str, expected_result: float
):
    price = TrinomialTreePricingModel.calculate(
        s, k, t, r, v, q, n, option_type
    )
    assert math.isclose(round(price, 2), expected_result)
