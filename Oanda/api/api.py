from abc import ABC, abstractmethod, ABCMeta
#from vendors import oanda

class ApiInterface(metaclass = ABCMeta):
	@classmethod
	def __subclasshook__(cls, subclass):
		return (
			hasattr(subclass, 'makeOrder') and
			callable(subclass.makeOrder) and
			hasattr(subclass, 'getTrades') and
			callable(subclass.getTrades) and
			hasAttr(subclass, 'getPriceStream') and
			callable(subclass.getPriceStream) and
			hasAttr(subclass, 'closePosition') and
			callable(subclass.closePosition) or
			NotImplemented
		)
	
	@abstractmethod
	def makeOrder(self) -> str:
		pass
		
	@abstractmethod
	def getTrades(self) -> str:
		pass
		
	@abstractmethod
	def getPriceStream(self) -> str:
		pass
		
	@abstractmethod
	def closePosition(self) -> str:
		pass
		
#if (hasattr(vendors, 'oanda')):
#	print('ok')
#else:
#	print('not ok')