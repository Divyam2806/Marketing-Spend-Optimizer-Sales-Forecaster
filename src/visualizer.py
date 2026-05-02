import matplotlib.pyplot as plt
import seaborn as sns

COLORS = ['#00d4ff', '#ff6b35', '#7fff00', '#ff00ff']

plt.rcParams['figure.facecolor'] = '#0f0f0f'
plt.rcParams['axes.facecolor'] = '#1a1a1a'
plt.rcParams['axes.labelcolor'] = 'white'
plt.rcParams['xtick.color'] = 'white'
plt.rcParams['ytick.color'] = 'white'
plt.rcParams['text.color'] = 'white'
plt.rcParams['axes.titlecolor'] = 'white'


def plot_eda(df):
    """
    Generates EDA charts — correlation heatmap and spend by channel.

    Parameters:
        df : marketing dataframe

    Returns:
        matplotlib Figure object
    """
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    fig.suptitle('Exploratory Data Analysis', fontsize=16, fontweight='bold')

    # Correlation heatmap
    corr = df.corr()
    sns.heatmap(corr, annot=True, fmt='.2f', cmap='coolwarm',
                ax=axes[0], linewidths=0.5, linecolor='#333')
    axes[0].set_title('Correlation Matrix', fontsize=13)

    # Total spend by channel
    spend_cols = [col for col in df.columns if col.endswith('_spend')]
    spend_totals = df[spend_cols].sum()
    labels = [col.replace('_spend', '').capitalize() for col in spend_cols]
    axes[1].bar(spend_totals.index, spend_totals.values,
                color=COLORS, edgecolor='#333', linewidth=0.8)
    axes[1].set_title('Total Spend by Channel', fontsize=13)
    axes[1].set_ylabel('Total Spend ($K)')
    axes[1].set_xticks(range(len(labels)))
    axes[1].set_xticklabels(labels, rotation=0)

    plt.tight_layout()
    return fig

def plot_model_performance(y_test, y_pred, r2):
    """
    Plots actual vs predicted revenue.

    Returns:
        matplotlib Figure object
    """
    fig, ax = plt.subplots(figsize=(8, 5))

    ax.scatter(y_test, y_pred, color='#00d4ff', alpha=0.6,
               edgecolors='white', linewidth=0.3)
    ax.plot([y_test.min(), y_test.max()],
            [y_test.min(), y_test.max()],
            color='#ff6b35', linewidth=2, linestyle='--',
            label='Perfect Prediction')
    ax.set_xlabel('Actual Revenue ($K)')
    ax.set_ylabel('Predicted Revenue ($K)')
    ax.set_title(f'Actual vs Predicted Revenue  |  R² = {r2:.3f}', fontsize=13)
    ax.legend()

    plt.tight_layout()
    return fig

def plot_scenarios(scenarios_df):
    """
    Plots predicted revenue for each budget scenario.

    Parameters:
        scenarios_df : DataFrame returned by simulate_scenarios()

    Returns:
        matplotlib Figure object
    """
    fig, ax = plt.subplots(figsize=(10, 5))

    bars = ax.barh(
        scenarios_df['scenario'],
        scenarios_df['predicted_revenue'],
        color=COLORS * (len(scenarios_df) // len(COLORS) + 1),
        edgecolor='#333',
        linewidth=0.8
    )

    ax.set_xlabel('Predicted Revenue ($K)')
    ax.set_title('Revenue Forecast by Scenario', fontsize=13)

    for bar, val in zip(bars, scenarios_df['predicted_revenue']):
        ax.text(val + 5, bar.get_y() + bar.get_height() / 2,
                f'${val:,.0f}K', va='center', color='white', fontsize=9)

    plt.tight_layout()
    return fig

def plot_optimization(optimal_spend, optimal_revenue):
    """
    Plots optimal budget allocation as a pie chart.

    Parameters:
        optimal_spend   : dict with channel names and spend values
        optimal_revenue : predicted revenue at optimal allocation

    Returns:
        matplotlib Figure object
    """
    labels = [col.replace('_spend', '').capitalize() for col in optimal_spend.keys()]
    values = list(optimal_spend.values())

    fig, ax = plt.subplots(figsize=(7, 7))

    wedges, texts, autotexts = ax.pie(
        values,
        labels=labels,
        autopct='%1.1f%%',
        colors=COLORS * (len(values) // len(COLORS) + 1),
        startangle=140,
        wedgeprops={'edgecolor': '#0f0f0f', 'linewidth': 2}
    )

    for text in texts + autotexts:
        text.set_color('white')

    ax.set_title(
        f'Optimal Budget Allocation\nPredicted Revenue: ${optimal_revenue:,.0f}K',
        fontsize=13
    )

    plt.tight_layout()
    return fig