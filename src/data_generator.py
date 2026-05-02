import numpy as np
import pandas as pd

def generate_dataset(n=200, seed=42):
    """
    Generates a synthetic marketing dataset with 4 channels and revenue.

    Parameters:
        n    : number of rows (campaigns)
        seed : random seed for reproducibility

    Returns:
        pd.DataFrame with columns:
        tv_spend, digital_spend, radio_spend, print_spend, revenue
    """

    np.random.seed(seed)

    tv = np.random.uniform(10, 300, n)
    digital = np.random.uniform(5, 200, n)
    radio = np.random.uniform(2, 50, n)
    print_ad = np.random.uniform(1, 80, n)

    revenue = (
        3.5 * tv +
        4.2 * digital +
        2.1 * radio +
        1.8 * print_ad +
        np.random.normal(0, 50, n)
    )

    return pd.DataFrame({
        'tv_spend': tv,
        'digital_spend': digital,
        'radio_spend': radio,
        'print_spend': print_ad,
        'revenue' : revenue
    })