import pandas as pd 
from pandas import DataFrame
import quandl as qdl
import datetime
import numpy as np
from datetime import date, timedelta
import matplotlib.colors as colors
import matplotlib.finance as finance
import matplotlib.dates as mdates
import matplotlib.ticker as mticker
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager


def main():
	auth_tok = "kz_8e2T7QchJBQ8z_VSi"

	#Number of days worth of data useable for charts or regression analysis
	num_days = 365
	#Pull data up to this point
	to_date = datetime.date.today()
	#List of currencies to pull data for
	currency_list = get_currency_list()

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

	Overbought_S = 80
	Oversold_S = 20

	max_lag = max(q, nslow, nfast, nema, ma_slow, ma_fast, n, d)

	#Pull this many days of data to return the amount of data user has requested
	pull_data_days = num_days + max_lag

	#Pull data from quandl
	currency_table = get_currency_data(currency_list, pull_data_days, auth_tok)

	# #Calculate RSI for all currency pairs in currency_table
	RSI = RSI_Calc(currency_table, q)

	# #Calculate simple moving averages
	ma_f = moving_average(currency_table, ma_fast, type='simple')
	ma_s = moving_average(currency_table, ma_slow, type='simple')

	#Calculate exponentially weighted moving averages and MACD
	emaslow, emafast, macd = get_MACD(currency_table, nslow= nslow, nfast = nfast)
	ema9 = moving_average(macd, nema, type = 'exponential')

	#Calculate stochastics
	fast_stochastic, slow_stochastic = get_stochastic(currency_table, n, d)

	RSI = drop_rows(RSI, max_lag)
	ma_f = drop_rows(ma_f, max_lag)
	ma_s = drop_rows(ma_s, max_lag)
	emaslow= drop_rows(emaslow, max_lag)
	emafast= drop_rows(emafast, max_lag)
	macd = drop_rows(macd, max_lag)
	ema9 = drop_rows(ema9, max_lag)
	fast_stochastic = drop_rows(fast_stochastic, max_lag)
	slow_stochastic = drop_rows(slow_stochastic, max_lag)
	currency_table = drop_rows(currency_table, max_lag)


	'''These plots will eventually be moved to produce_charts'''
	for currency in RSI:
		plt.rc('axes', grid=True)
		plt.rc('grid', color='0.75', linestyle='-', linewidth=0.5)

		textsize = 9
		left, width = 0.1, 0.8
		rect1 = [left, 0.6, width, 0.3]
		rect2 = [left, 0.45, width, 0.15]
		rect3 = [left, 0.3, width, 0.15]
		rect4 = [left, 0.15, width, 0.15]

		fig = plt.figure(facecolor='white')
		axescolor = '#f6f6f6'  # the axes background color

		ax1 = fig.add_axes(rect1, axisbg=axescolor)  # left, bottom, width, height
		ax2 = fig.add_axes(rect2, axisbg=axescolor, sharex=ax1)
		ax3 = fig.add_axes(rect3, axisbg=axescolor, sharex=ax1)
		ax4 = fig.add_axes(rect4, axisbg=axescolor, sharex=ax1)

		ax2.plot(RSI.index, RSI[currency], color='blue')
		ax2.axhline(Overbought, color='red')
		ax2.axhline(Oversold, color='green')
		ax2.text(0.6, 0.9, '>70 = overbought', va='top', transform=ax2.transAxes, fontsize=textsize)
		ax2.text(0.6, 0.1, '<30 = oversold', transform=ax2.transAxes, fontsize=textsize)
		ax2.set_ylim(0, 100)
		ax2.set_yticks([30, 70])
		ax2.text(0.025, 0.95, 'RSI (%s)' % q, va='top', transform=ax2.transAxes, fontsize=textsize)
		ax1.set_title('{0} Daily Chart'.format(currency))

		line = ax1.plot(currency_table.index, currency_table[currency], color='black', label='_nolegend_')

		linema20, = ax1.plot(ma_f.index, ma_f[currency], color='blue', lw=2, label='MA (%s)' % ma_fast)
		linema200 = ax1.plot(ma_s.index, ma_s[currency], color='red', lw=2, label='MA (%s)' % ma_slow)

		ax3.plot(macd.index, macd[currency], color='black', lw=2)
		ax3.plot(ema9.index, ema9[currency], color='blue', lw=1)
		ax3.fill_between(macd.index, macd[currency] - ema9[currency], 0, alpha=0.5, facecolor='red', edgecolor= 'maroon')
		ax3.text(0.025, 0.95, 'MACD (%d, %d, %d)' % (nfast, nslow, nema), va='top', transform=ax3.transAxes, fontsize=textsize)

		ax4.plot(fast_stochastic.index, fast_stochastic[currency], color='blue')
		ax4.plot(slow_stochastic.index, slow_stochastic[currency], color= 'yellow')
		ax4.axhline(Overbought_S, color='red')
		ax4.axhline(Oversold_S, color='green')
		ax4.text(0.6, 0.9, '>80 = overbought', va='top', transform=ax4.transAxes, fontsize=textsize)
		ax4.text(0.6, 0.1, '<20 = oversold', transform=ax4.transAxes, fontsize=textsize)
		ax4.set_ylim(0, 100)
		ax4.set_yticks([20, 80])
		ax4.text(0.025, 0.95, 'Stochastic (%s)' % n, va='top', transform=ax4.transAxes, fontsize=textsize)
		# turn off upper axis tick labels, rotate the lower ones, etc
		for ax in ax1, ax2, ax3, ax4:
			if ax != ax4:
				for label in ax.get_xticklabels():
					label.set_visible(False)
		else:
			for label in ax.get_xticklabels():
				label.set_rotation(30)
				label.set_horizontalalignment('right')

		ax.fmt_xdata = mdates.DateFormatter('%Y-%m-%d')


	plt.show()

def get_currency_list():
	currency_list = ['CURRFX/MXNUSD.1', 'CURRFX/USDCAD.1', 'CURRFX/NZDUSD.1', 'CURRFX/USDHKD.1', 'CURRFX/USDJPY.1', 'CURRFX/USDSGD.1', 'CURRFX/GBPUSD.1', 'CURRFX/USDZAR.1', 'CURRFX/AUDUSD.1', 'CURRFX/EURUSD.1']
	return currency_list

''' get_currency_data will be moved to pull_data'''
def get_currency_data(currency_list, num_days, api_key):
	# Calculate dates
	end_date = datetime.date.today()
	start_date = end_date - timedelta(num_days)

	# Initialize data table
	data_table = None
	# Run through currencies, first assignment is initialized
	# Anything past first currency is joined into table
	for currency in currency_list:
		current_column = qdl.get(currency, start_date= start_date, end_date= end_date, authtoken= api_key)
		if data_table is None:
			data_table = current_column
		else:
			data_table = data_table.join(current_column, how= 'left', rsuffix= ' ')

	data_table.columns = ['MXN/USD', 'USD/CAD', 'NZD/USD', 'USD/HKD', 'USD/JPY', 'USD/SGD', 'GBP/USD', 'USD/ZAR', 'AUD/USD', 'EUR/USD']

	return data_table 

def RSI_Calc(currency_data, q):
	delta = currency_data.diff()
	dUp, dDown = delta.copy(), delta.copy()
	dUp[dUp < 0] = 0
	dDown[dDown > 0] = 0

	RolUp = dUp.rolling(window= q, center= False).mean()
	RolDown = dDown.rolling(window = q, center= False).mean().abs()

	RS = RolUp / RolDown
	RSI = 100.0 - (100.0 / (1.0 + RS))
	return RSI

def moving_average(x, n, type='simple'):
	""" compute an n period moving average.
		type is 'simple' | 'exponential'
	"""
	if type == 'simple':
		ma = x.rolling(window = n, center= False).mean()

	else:
		ma = x.ewm(span = n).mean()
	return ma

def get_MACD(x, nslow=26, nfast=12):
	"""
	compute the MACD (Moving Average Convergence/Divergence) using a fast and slow exponential moving avg'
	return value is emaslow, emafast, macd which are len(x) arrays
	"""
	emaslow = moving_average(x, nslow, type='exponential')
	emafast = moving_average(x, nfast, type='exponential')
	macd = emafast - emaslow

	return emaslow, emafast, macd

def get_stochastic(prices, n, nma):
	#Change high and low so that they do not include current index
	print prices
	prices_shift = prices.shift(periods = 1)
	print prices_shift
	low = prices_shift.rolling(window = n, center= False).min()
	high = prices_shift.rolling(window= n, center= False).max()
	k = 100 * ((prices - low)/ (high - low))

	print k
	d = moving_average(k, nma, type = 'simple')

	return k, d

def drop_rows(data, max_val):
	data = data.ix[max_val:]

	return data


if __name__ == "__main__":
	main()
