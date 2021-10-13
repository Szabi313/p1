from strategy import StrategyInterface
from strategy import Direction

class Scalping(StrategyInterface):
	def openPosition(self, currentPrice: float):
		return 4
		
c = Scalping()
print(c.openPosition(2))
print(issubclass(Scalping, StrategyInterface))