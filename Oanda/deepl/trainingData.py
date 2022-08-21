from sma import Sma
from slope import Slope
from oanda.oaResponse import oaResponse

class TrainingData:

	def makeTrainingData(self, trading_data, periods = [200, 50, 20], column = 'bid_c'):
		sma = Sma(trading_data)
		slope = Slope(trading_data)	
		
		for i in periods:
			self.training_data = sma.getSma(i, column)
			#self.training_data = slope.addSlopes('sma_' + str(i) + '_' + column, 30, 'slope_' +str(i))
			self.training_data = slope.addSlopes('sma_' + str(i) + '_' + column, 20, 'slope_' +str(i))
			
		#self.training_data = slope.addSlopes(column, 30, 'priceSlope', startFromFirst = True)
		self.training_data = slope.addSlopes(column, 10, 'priceSlope', startFromFirst = True)
		
		return self.training_data