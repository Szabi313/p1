#from bunch import Bunch
from abc import ABC, abstractmethod, ABCMeta
from enum import Enum
#from typing_extensions import Literal
#from .. api.api import ApiInterface

#BuyOrSell2 = Bunch(
#	SELL = 'SELL',
#	BUY = 'BUY',
#	NO_ACTION = 'NO_ACTION'
#)

class Direction(Enum):
	SELL = 'sell'
	BUY = 'buy'
	HOLD = 'hold'
	
class StrategyInterface(metaclass = ABCMeta):
	
	@classmethod
	def __subclasshook__(cls, subclass):
		return (hasattr(subclass, 'openPosition') and
			callable(subclass.openPosition) or
			NotImplemented)
		
	@abstractmethod
	def openPosition(self, currentPrice: float) -> Direction:
		pass

class CloseStrategyInterface(ABC):
	@abstractmethod
	def close(self, currentPrice: float, openPrice: float) -> bool:
		pass