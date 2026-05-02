import os
from src.data_generator import generate_dataset
from src.database import save_data, run_queries
from src.model import train_model
from src.simulator import simulate_scenarios
from src.optimizer import optimize_budget
from src import visualizer

os.makedirs('outputs', exist_ok=True)
os.makedirs('data', exist_ok=True)

print("\n" + "═"*55)
print("  MARKETING SPEND OPTIMIZER & SALES FORECASTER")
print("═"*55)

# 1. Generate data
print("\nGenerating dataset...")
df = generate_dataset(n=200)
df.to_csv('data/marketing_data.csv', index=False)
print(f"   {df.shape[0]} rows × {df.shape[1]} columns")

# 2. Database
print("\nSaving to database & running queries...")
save_data(df)
spend_by_channel, revenue_stats, high_performers = run_queries()
print("\nTotal Spend by Channel:")
print(spend_by_channel.to_string(index=False))
print("\nRevenue Stats:")
print(revenue_stats.to_string(index=False))
print("\nHigh-Performing Campaigns:")
print(high_performers.to_string(index=False))

# 3. EDA
print("\nRunning EDA...")
fig_eda = visualizer.plot_eda(df)
fig_eda.savefig('outputs/01_eda.png', dpi=150, bbox_inches='tight')
print("   Saved to outputs/01_eda.png")

# 4. Model
print("\nTraining model...")
model, features, metrics, test_data = train_model(df)
print(f"   R²  : {metrics['r2']:.4f}")
print(f"   MAE : ${metrics['mae']:.2f}K")
print("\n   Coefficients:")
for channel, coef in metrics['coefficients'].items():
    print(f"   {channel:<20} → ${coef:.2f}K revenue per $1K spend")
fig_model = visualizer.plot_model_performance(*test_data, metrics['r2'])
fig_model.savefig('outputs/02_model_performance.png', dpi=150, bbox_inches='tight')
print("   Saved to outputs/02_model_performance.png")

# 5. Simulate
print("\nSimulating scenarios...")
scenarios_df = simulate_scenarios(model, features, total_budget=700)
print(scenarios_df[['scenario', 'predicted_revenue']].to_string(index=False))
fig_scenarios = visualizer.plot_scenarios(scenarios_df)
fig_scenarios.savefig('outputs/03_scenarios.png', dpi=150, bbox_inches='tight')
print("   Saved to outputs/03_scenarios.png")

# 6. Optimize
print("\nOptimizing budget allocation...")
optimal_spend, optimal_revenue = optimize_budget(model, features, total_budget=700)
for channel, spend in optimal_spend.items():
    print(f"   {channel:<20} → ${spend:,.1f}K")
print(f"\n   Predicted Revenue : ${optimal_revenue:,.0f}K")
print(f"   Predicted ROI     : {(optimal_revenue - 700) / 700 * 100:.1f}%")
fig_opt = visualizer.plot_optimization(optimal_spend, optimal_revenue)
fig_opt.savefig('outputs/04_optimal_allocation.png', dpi=150, bbox_inches='tight')
print("   Saved to outputs/04_optimal_allocation.png")

print("\n" + "═"*55)
print(" PIPELINE COMPLETE — Check outputs/ folder")
print("═"*55)