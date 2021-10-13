from scipy import stats
import pandas as pd
import numpy as np

class Slope:
	def __init__(self, data_frame):
		self.df = data_frame
		self.statistics = None
		
	def addSlopes(self, column, period, new_col_name, startFromFirst = False):
		if period > len(self.df.index):
			return
			
		if startFromFirst:
			start = 0
			end = len(self.df) - period+1
		else: 
			start = period-1
			end = len(self.df)
		
		x = range(period)
		col_index = self.df.columns.get_loc(column)
	
		periodes = [self.df.iloc[i - period : i, [col_index]].values.reshape(period) for i in range(period, len(self.df) + 1)]
		
		statistics = [self.getRegression(x, periodes[i]) for i in range(len(periodes))]
		
		statisticsDf = pd.DataFrame(statistics, index = range(start, end))
		
	#	slopes = pd.Series(slopes, index = range(period -1, len(self.df)))
		
		self.df[new_col_name] = statisticsDf.slope
		self.df[new_col_name + '_r'] = statisticsDf.rvalue
		
		return self.df
		
	def getRegression(self, xp, yp):
		stat = stats.linregress(xp, yp.astype(float))
			
		return stat
		
y = [5, 10, 15, 20, 25, 31, 37, 43, 49, 55]

df = pd.DataFrame(y, columns=list('A'))

sl = Slope(df)

print(sl.addSlopes('A', 5, 'slope_200'))