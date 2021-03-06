#Set variables
import datetime
from datetime import date, timedelta
# authorization key for quandl data 
auth_tok = "kz_8e2T7QchJBQ8z_VSi"
# Input last day to get returns data for (default is today)
end_date = datetime.date.today() - timedelta(3)
# Input original portfolio value, used for VaR calculations
portfolio_value = 1000
# Input number of days to calculate back returns
num_days_optimal_portfolio = 200
#Compute returns with shift percentage change delay (daily = 1)
shift = 1
# Input Leverage
leverage = 10
# Input Rolling Period for moving averages
rolling_period = 50
# Input minimum desired return for portfolio optimization
rminimum = 100/float(252)
# Input risk free interest rate
interest_rate = 2/ float(365)
# Input interval for displaying changes in the weight distribution over time for distribution chart (daily=1, weekly=5)
distribution_interval = 5

# Number of days to pull data for 
# ** this num_days is a different value than that used in other files **
num_days_regression = 720
# ** Before this date, daily high/low data is unreliable and therefore the Stochastic calculation is unreliable **
stoch_date = datetime.date(2016, 7, 15)
# Number of random portfolios in Optimize_FX_Portfolio
n_portfolios = 5000

#Number of days worth of data useable for charts or regression analysis
num_days_charts = 100
#q = avg. periods for gain/loss
q = 14
# On the scale from 0-100, this level is considered to be "overbought" by RSI, typical value is 70
Overbought = 70
#On the scale from 0-100, this level is considered to be "oversold" by RSI, typical value is 30
Oversold = 30
#Determine the moving average windows for MACD, moving average convergence divergence, as measured by
#the difference between slow and fast exponentially weighted moving averages compared to the fastest of 
#the three.  Levels are typically 26 for slow, 12 for fast, and 9 for fastest
nslow = 26
nfast = 12
nema = 9
#Determine windows for simple moving averages to be overlayed on the exchange rate chart.  Levels vary, but widely-used
#rolling averages include 10, 20, 50, 100, and 200 day averages
ma_slow = 100
ma_fast = 20
#Determine windows for stochastics.  A typical window is 14 periods.  N is the number of windows.  D is the "slow" stochastic window
#typically a 3- period moving average of the fast stochastic
n = 14
d = 3
# RSI overbought or oversold
Overbought_S = 80
Oversold_S = 20
# Number of bins for VaR histogram in Daily_Reports
num_bins = 25