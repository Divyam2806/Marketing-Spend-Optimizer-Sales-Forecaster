import pandas as pd

def simulate_scenarios(model, features, total_budget=700):
    """
    Simulates revenue predictions under different budget split scenarios.

    Parameters:
        model        : trained LinearRegression object
        features     : list of feature column names from training
        total_budget : total budget in $K to split across channels

    Returns:
        pd.DataFrame with scenario names, spend per channel, and predicted revenue
    """
    n = len(features)

    # Weights(ratio) per scenario — normalized so they always sum to 1
    # regardless of how many channels exist
    scenarios = {
        'Equal Split':    [1] * n,
        'First Heavy':    [3] + [1] * (n - 1),
        'Last Heavy':     [1] * (n - 1) + [3],
        'Middle Heavy':   [1 if i not in range(1, n-1) else 3 for i in range(n)],
        'Spread Evenly':  [i + 1 for i in range(n)],
    }

    results = []
    for name, weights in scenarios.items():
        total_weight = sum(weights)
        fractions = [w / total_weight for w in weights]
        spend = [f * total_budget for f in fractions]
        predicted_revenue =  model.predict(pd.DataFrame([spend], columns=features))[0]
        row = {'scenario': name}
        row.update(dict(zip(features, spend)))
        row['predicted_revenue'] = predicted_revenue
        results.append(row)

    return pd.DataFrame(results)