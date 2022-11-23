from scipy import stats
import pandas as pd
import numpy as np
import statsmodels as sm
from statsmodels.regression.rolling import RollingOLS

class Slope:
	def __init__(self, data_frame):
		self.df = data_frame
		self.statistics = None
		
		self.curve_slope = '_curve_slope'
		
	def addTrendSlopes(self, column, period, new_col_name, startFromFirst = False):

		print('add slope begin')
		
		if period > len(self.df.index):
			return
	#		
#		if startFromFirst:
#			start = 0
#			end = len(self.df) - period+1
#		else: 
#			start = period-1
#			end = len(self.df)
		
		#x = range(period)
#		col_index = self.df.columns.get_loc(column)
	
		#periodes = [self.df.iloc[i - period : i, [col_index]].values.reshape(period) for i in range(period, len(self.df) + 1)]
		
		#statistics = [self.getRegression(periodes[i], x) for i in range(len(periodes))]
		
		#statisticsDf = pd.DataFrame(statistics, index = range(start, end))
		
	#	slopes = pd.Series(slopes, index = range(period -1, len(self.df)))
		
		#self.df[new_col_name] = statisticsDf.slope
		#self.df[new_col_name + '_r'] = statisticsDf.rvalue
		
		## ROLLING ##
#		self.df[new_col_name + '_roll'] = self.df.iloc[ :, col_index].rolling(window = period).apply(self.getRegression, raw = True)
		
	#	self.df.info()
		
		model = RollingOLS.from_formula('year_float  ~ ' + column, data = self.df, window=period, eval_env=-1)
		
		reg = model.fit()
#		print(reg.rsquared)
		
	#	params = reg.params.copy()
	#	bid_cc = params['bid_c']
	
	#	bid_cc = reg.params.loc[ :,['bid_c']]
		
		self.df[new_col_name + '_roll_ols'] = reg.params.loc[ : , [column]]
		self.df[new_col_name + '_roll_ols_r'] = reg.rsquared
	#	print(bid_cc)
		
	#	self.df.join([coef])
		
	#	df3 = self.df.iloc[ :, col_index].rolling(window = period).apply(self.getRegression, raw = True)
	#	print(df)
		
		
#		self.df[new_col_name + '_roll_shift'] = self.df.shift(-2)[new_col_name + '_roll']
		
		if startFromFirst:
				self.df[new_col_name + '_roll_ols'] =  	self.df[new_col_name + '_roll_ols'].shift(-1 * period)
				self.df[new_col_name + '_roll_ols_r'] =  	self.df[new_col_name + '_roll_ols_r'].shift(-1 * period)
		
		print('add slope end')
		
		return self.df
		
		
	def addCurveSlopes(self, time_column, time_column_t_1,  column, new_col_name):
		self.df[column + self.curve_slope] = self.df[column].shift(-1)
		self.df[column + self.curve_slope] = (self.df[time_column_t_1] - self.df[time_column])  / (self.df[column + self.curve_slope] - self.df[column])
	#	self.df.rename(columns = {column + '_T+1': column + '_curve_slope'})
		return self.df
		
		
	def curveSlope(self, y):
		# step by one so delta x always 1.
		# calculatng the slope between the first two item of y, 
		# so rolling window must be 2 (higher length not affected)
		
		return 1 /( y[1] - y[0])
		
	#def getRegression(self, yp, xp = None):
#		former_xp = None
#		
#		if xp == None:
#			xp = range(0, len(yp))
#			former_xp = True
#		
#		stat = stats.linregress(xp, yp.astype(float))
#		
#		if former_xp == True:
#			return stat.slope
#			
#		return stat
		
#y = [5, 10, 15, 20, 25, 31, 37, 43, 49, 55]

#df = pd.DataFrame(y, columns=list('A'))

#sl = Slope(df)

#print(sl.addSlopes('A', 5, 'slope_200'))