import pandas as pd

class Sma:

	def __init__(self, data_frame):
		self.df = data_frame
		self.source_col:str
		self.source_col_index:int
		self.col_name: str = 'sma_{}_'
		self.col_name_percent:str = '_%'
		self.smas: pd.array
		self.smas_percent: pd.array
	
	def getSma(self, period, source_col):
		print('sma begin')
		self.source_col = source_col
		self.source_col_index = self.df.columns.get_loc(self.source_col)
		self.col_name = 'sma_{}_' + self.source_col
		self.col_name = self.col_name.format(period)
		self.col_name_percent = self.col_name + self.col_name_percent
		
	##	self.smas = [self.df.iloc[i -period : i , [self.source_col_index]].mean(axis=0) for i in range(period, len(self.df) + 1)]
	#	self.smas_percent = self.smas / self.df['c']
	
	##	self.smas = pd.Series(self.smas, index = range(period -1, len(self.df)))
	#	self.smas_percent = pd.Series(self.smas_percent, index=range(period-1, len(self.df)))
	
		if self.col_name in self.df:
			pass
		else:
		#	self.df[self.col_name] = self.smas
			self.df[self.col_name] = self.df.iloc[:, self.source_col_index].rolling(window = period).mean()
			
	#	self.smas_percent = self.df[self.col_name] / self.df['c']
			
	#	self.df[self.col_name_percent] = self.smas_percent
			
		print('sma end')
		return self.df
		
		