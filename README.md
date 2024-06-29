# option-pricing-model

Aim to provide pricing models of European option.

- [Black-Scholes](https://en.wikipedia.org/wiki/Black%E2%80%93Scholes_model)
- [Binominal Tree](https://en.wikipedia.org/wiki/Binomial_options_pricing_model)
- [Trinomial Tree](https://en.wikipedia.org/wiki/Trinomial_tree)
- [Monte Carlo](https://en.wikipedia.org/wiki/Monte_Carlo_methods_for_option_pricing)

## Usage

### Clone the project
```
git clone ...
```

### Install packages
```
poetry shell
poetry install
```

### Examples
```python
from obj.base import Option
from pricing import (
    BlackScholesPricingModel,
    TrinomialTreePricingModel,
    BinominalTreePricingModel,
    MonteCarloPricingModel
)


option = Option(
    spot=42,
    strike=40,
    maturity=0.4,
    volatility=0.2,
    rate=0.1,
    yield_rate=0,
    option_type='C'
)


option.greeks
# output: {'delta': 0.7779, 'gamma': 0.056, 'theta': -4.815, 'vega': 7.9076, 'rho': 11.3526}

BlackScholesPricingModel.calculate(option=option)
# output: 4.2913

TrinomialTreePricingModel.calculate(option=option)
# output: 4.2908

BinominalTreePricingModel.calculate(option=option)
# output: 4.2893

MonteCarloPricingModel.calculate(option=option, mu=0.1)
# output: 4.5847
```
