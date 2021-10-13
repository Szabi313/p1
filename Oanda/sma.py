import pandas as pd

class Sma:

	def __init__(self, data_frame):
		self.df = data_frame
	
	def getSma(self, period, source_col):
		self.source_col = source_col
		self.source_col_index = self.df.columns.get_loc(self.source_col)
		self.col_name = 'sma_{}_' + self.source_col
		self.col_name = self.col_name.format(period)
		self.smas = [self.df.iloc[i -period : i , [self.source_col_index]].mean(axis=0) for i in range(period, len(self.df) + 1)]
	
		self.smas = pd.Series(self.smas, index = range(period -1, len(self.df)))
	
		if self.col_name in self.df:
			pass
		else:
			self.df[self.col_name] = self.smas
			
		return self.df
		
		