from scipy.optimize import minimize
import pandas as pd

def optimize_budget(model, features, total_budget=700):
    """
    Finds the optimal budget allocation across channels to maximize revenue.

    Parameters:
        model        : trained LinearRegression object
        features     : list of feature column names
        total_budget : total budget in $K

    Returns:
        dict with channel names as keys and optimal spend as values
        optimal_revenue : predicted revenue at optimal allocation
    """
    n = len(features)

    def negative_revenue(spend):
        return -model.predict(pd.DataFrame([spend], columns=features))[0]

    constraints = {'type': 'eq', 'fun': lambda x: sum(x) - total_budget}
    bounds = [(10, total_budget)] * n
    x0 = [total_budget / n] * n

    result = minimize(negative_revenue, x0, bounds=bounds, constraints=constraints)

    optimal_spend = dict(zip(features, result.x))
    optimal_revenue = -result.fun

    return optimal_spend, optimal_revenue