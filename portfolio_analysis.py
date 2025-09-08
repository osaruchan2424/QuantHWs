import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Read the Excel file
df = pd.read_excel('Problem_Set1_2025.xlsx')

# The data starts from row 4 (index 4), with the first column being dates
# and columns 1-50 being the stock returns
# Let's extract the data properly

# Skip the header rows and get the actual data
data = df.iloc[4:, :].copy()

# Set the first column as the date index
data = data.set_index(data.columns[0])

# Rename columns to be more meaningful
# We have 50 stocks (columns 1-50) plus market index (column 52)
stock_columns = [f'Stock_{i+1}' for i in range(50)]  # 50 stocks
data.columns = ['date'] + stock_columns + ['market_index']

# Convert date column to proper format if needed
data['date'] = pd.to_datetime(data['date'], format='%Y%m', errors='coerce')

# Convert all stock return columns to numeric
for col in stock_columns:
    data[col] = pd.to_numeric(data[col], errors='coerce')

# Remove any rows with all NaN values
data = data.dropna(how='all')

print("Data shape:", data.shape)
print("Date range:", data['date'].min(), "to", data['date'].max())
print("First few rows:")
print(data.head())

# Calculate returns for each stock (they should already be in percentage)
# Let's check if we need to convert from percentage to decimal
print("\nSample returns (first 5 stocks, first 5 periods):")
print(data[stock_columns[:5]].head())

# Create equal-weight portfolios
def create_equal_weight_portfolio(stock_indices, returns_data):
    """Create an equal-weight portfolio from selected stocks"""
    selected_stocks = [stock_columns[i] for i in stock_indices]
    portfolio_returns = returns_data[selected_stocks].mean(axis=1)
    return portfolio_returns

# Create portfolios with different numbers of stocks
portfolio_5 = create_equal_weight_portfolio(range(5), data)
portfolio_10 = create_equal_weight_portfolio(range(10), data)
portfolio_25 = create_equal_weight_portfolio(range(25), data)
portfolio_50 = create_equal_weight_portfolio(range(50), data)

# Calculate statistics for each portfolio
portfolios = {
    '5 stocks': portfolio_5,
    '10 stocks': portfolio_10,
    '25 stocks': portfolio_25,
    '50 stocks': portfolio_50
}

results = {}
for name, returns in portfolios.items():
    mean_return = returns.mean()
    std_return = returns.std()
    results[name] = {'mean': mean_return, 'std': std_return}
    print(f"\n{name}:")
    print(f"  Mean return: {mean_return:.4f}%")
    print(f"  Standard deviation: {std_return:.4f}%")

# Create the plot
num_stocks = [5, 10, 25, 50]
std_deviations = [results[f'{n} stocks']['std'] for n in num_stocks]

plt.figure(figsize=(10, 6))
plt.plot(num_stocks, std_deviations, 'bo-', linewidth=2, markersize=8)
plt.xlabel('Number of Stocks in Portfolio')
plt.ylabel('Standard Deviation of Returns (%)')
plt.title('Portfolio Standard Deviation vs Number of Stocks')
plt.grid(True, alpha=0.3)
plt.xticks(num_stocks)

# Add value labels on points
for i, (x, y) in enumerate(zip(num_stocks, std_deviations)):
    plt.annotate(f'{y:.2f}%', (x, y), textcoords="offset points", 
                xytext=(0,10), ha='center')

plt.tight_layout()
plt.savefig('/workspace/portfolio_diversification.png', dpi=300, bbox_inches='tight')
plt.show()

print("\n" + "="*50)
print("ANALYSIS SUMMARY")
print("="*50)
print(f"Portfolio with 5 stocks:  Mean = {results['5 stocks']['mean']:.4f}%, Std = {results['5 stocks']['std']:.4f}%")
print(f"Portfolio with 10 stocks: Mean = {results['10 stocks']['mean']:.4f}%, Std = {results['10 stocks']['std']:.4f}%")
print(f"Portfolio with 25 stocks: Mean = {results['25 stocks']['mean']:.4f}%, Std = {results['25 stocks']['std']:.4f}%")
print(f"Portfolio with 50 stocks: Mean = {results['50 stocks']['mean']:.4f}%, Std = {results['50 stocks']['std']:.4f}%")

print(f"\nReduction in standard deviation from 5 to 50 stocks: {((results['5 stocks']['std'] - results['50 stocks']['std']) / results['5 stocks']['std'] * 100):.2f}%")