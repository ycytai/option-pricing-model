# option-pricing-model

Aim to provide pricing models of European option. 

- [Black-Scholes](https://en.wikipedia.org/wiki/Black%E2%80%93Scholes_model)
- [Binominal Tree](https://en.wikipedia.org/wiki/Binomial_options_pricing_model)
- [Trinomial Tree](https://en.wikipedia.org/wiki/Trinomial_tree)
- [Monte Carlo](https://en.wikipedia.org/wiki/Monte_Carlo_methods_for_option_pricing)

## Demo

```python
>>> from pricing import (
...     BlackScholesPricingModel,
...     BinominalTreePricingModel,
...     TrinomialTreePricingModel,
...     MonteCarloPricingModel
... )
>>> params = {'s': 42, 'k': 40, 't': 0.5, 'r': 0.1, 'option_type': 'C'}
>>> BlackScholesPricingModel.calculate(**params, v=0.2, q=0)
4.759422392871532
>>> BinominalTreePricingModel.calculate(**params, v=0.2, q=0, n=2)
4.799241115251898
>>> TrinomialTreePricingModel.calculate(**params, v=0.2, q=0, n=2)
4.69696892351171
>>> MonteCarloPricingModel.calculate(**params, mu=0.1, sigma=0.2, m=100, n=1000)
4.225544304112851
```