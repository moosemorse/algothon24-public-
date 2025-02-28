import cryptpandas
import pandas as pd
import numpy as np
from scipy.optimize import minimize
from dictionary_generation import get_dict
# from passwords import SLACK_TOKEN

# List of encrypted files and passwords
files = get_dict()

# Function to load and clean data
def load_and_clean_data(files):
    all_data = []
    for file in files:
        data = cryptpandas.read_encrypted(path=file["path"], password=file["password"])
        # Convert all columns to numeric, coerce errors to NaN
        data = data.apply(pd.to_numeric, errors='coerce')
        all_data.append(data)
    combined_data = pd.concat(all_data, ignore_index=True)
    return combined_data

# Load and clean data
combined_data = load_and_clean_data(files)

# Replace infinite values with NaN
combined_data.replace([np.inf, -np.inf], np.nan, inplace=True)

# Fill NaN values with zeros
combined_data.fillna(0, inplace=True)

# Ensure all data is numeric
combined_data = combined_data.apply(pd.to_numeric, errors='coerce')

# Drop columns with zero standard deviation
volatility = combined_data.std()
zero_volatility = volatility[volatility == 0].index
combined_data.drop(columns=zero_volatility, inplace=True)

# Recalculate mean returns and volatility
mean_returns = combined_data.mean()
volatility = combined_data.std()

# Calculate Sharpe Ratios
risk_free_rate = 0  # Assuming no risk-free return
sharpe_ratios = (mean_returns - risk_free_rate) / volatility

# Remove any infinite or NaN Sharpe Ratios
sharpe_ratios.replace([np.inf, -np.inf], np.nan, inplace=True)
sharpe_ratios.dropna(inplace=True)

# Update combined_data to include only valid strategies
combined_data = combined_data[sharpe_ratios.index]

# Number of strategies
num_strategies = len(sharpe_ratios)

# Compute the covariance matrix Sigma
Sigma = combined_data.cov()

# Assume equal market weights
w_mkt = np.array([1 / num_strategies] * num_strategies)

# Risk aversion coefficient
delta = 2.5

# Compute equilibrium returns Pi
Pi = delta * Sigma.dot(w_mkt)

# Define investor's views
# Get strategy names
strategies = sharpe_ratios.index.tolist()
n = num_strategies

# Example Views:
# View 1: Strategy S1 will have an expected return of 5%
# View 2: Strategy S2 will outperform Strategy S3 by 1%
P = np.zeros((2, n))
Q = np.zeros(2)

# Map strategies to indices for readability
strategy_indices = {strategy: idx for idx, strategy in enumerate(strategies)}

# View 1
P[0, strategy_indices[strategies[0]]] = 1  # S1
Q[0] = 0.05  # Expected return of 5%

# View 2
P[1, strategy_indices[strategies[1]]] = 1   # S2
P[1, strategy_indices[strategies[2]]] = -1  # S3
Q[1] = 0.01  # S2 expected to outperform S3 by 1%

# Tau - scaling factor for the prior
tau = 0.05  # Small value

# Omega - uncertainty in the views
Omega = np.diag(np.diag(tau * P.dot(Sigma).dot(P.T)))

# Compute the posterior expected returns E(r)
# Compute inverse of (tau * Sigma)
inv_tau_Sigma = np.linalg.inv(tau * Sigma)

# Compute M = inv(tau_Sigma) + P.T * inv(Omega) * P
M = inv_tau_Sigma + P.T.dot(np.linalg.inv(Omega)).dot(P)

# Compute RHS = inv_tau_Sigma * Pi + P.T * inv(Omega) * Q
RHS = inv_tau_Sigma.dot(Pi) + P.T.dot(np.linalg.inv(Omega)).dot(Q)

# Solve for posterior expected returns E(r)
E_r = np.linalg.inv(M).dot(RHS)

# Update the mean returns to be E(r)
posterior_returns = pd.Series(E_r, index=strategies)

# Constraints and bounds
bounds = [(0, 1) for _ in range(num_strategies)]  # Max weight = 100%
constraints = ({'type': 'eq', 'fun': lambda weights: np.sum(weights) - 1})  # Weights sum to 1


# Optimization function
def objective_function(weights, expected_returns, cov_matrix, risk_aversion):
    portfolio_return = np.dot(weights, expected_returns)
    portfolio_variance = weights.T.dot(cov_matrix).dot(weights)
    return - (portfolio_return - risk_aversion * portfolio_variance)

# Initial guess: Equal weights
initial_guess = np.array([1 / num_strategies] * num_strategies)

# Optimize weights
risk_aversion = 0.5  # Adjust as necessary

result = minimize(
    objective_function,
    initial_guess,
    args=(E_r, Sigma, risk_aversion),
    method='SLSQP',
    bounds=bounds,
    constraints=constraints,
    options={'ftol': 1e-9}
)

# Check optimizer success
if not result.success:
    print("Optimization failed:", result.message)

# Extract weights
optimized_weights = result.x

# Set negligible weights to zero
threshold = 1e-5
optimized_weights[optimized_weights < threshold] = 0

# Verify constraints are still satisfied
weight_sum = np.sum(optimized_weights)
if weight_sum != 1:
    # Adjust weights proportionally to sum to 1 without exceeding 0.1
    scaling_factor = 1 / weight_sum
    optimized_weights = np.minimum(optimized_weights * scaling_factor, 0.1)

# Create a dictionary for results
portfolio_dict = {strategy: weight for strategy, weight in zip(strategies, optimized_weights)}

# Add team_name and passcode
portfolio_dict['team_name'] = 'algothoners123'
portfolio_dict['passcode'] = 'RagingMartians'

# Print the portfolio dictionary
print(portfolio_dict)
