import requests
from bunch import Bunch
from oanda.Credentials.credentials import Credentials
import json

endPoints = Bunch(
	trades = 'trades',
	orders = 'orders',
	pricing = 'pricing',
	instruments = 'instruments',
	candles = 'candles',
	stream = 'stream',
	close = 'close',
	transactions = 'transactions',
	idrange = 'idrange',
	sinceid = 'sinceid'
)

	
urlUtil = Bunch(
	SLASH = '/',
	HTTPS = 'https://',
	BASE_URL = 'api-fxpractice.oanda.com/v3/',
	BASE_STREAM_URL = 'stream-fxpractice.oanda.com/v3/',
	ACCOUNTS = 'accounts/'
)

class oaRequest:
	credentials = Credentials()
	response = ''
	order = ''
	
	def buildUrl(self, pathParams, needAccountNo, stream):
		if stream:
			baseUrl = urlUtil.BASE_STREAM_URL
		else:
			baseUrl = urlUtil.BASE_URL
		url = urlUtil.HTTPS + baseUrl 
		if needAccountNo:
			url += urlUtil.ACCOUNTS + self.credentials.getAccountNo()
		url += urlUtil.SLASH 		
		if type(pathParams) is str:
			url += endPoints[pathParams]
		elif type(pathParams) is dict:
			pathParamString = ''
			for key, value in pathParams.items():
				pathParamString += key + urlUtil.SLASH
				if value != '':
					pathParamString += value + urlUtil.SLASH
			pathParamString = pathParamString[:-1]
			url += pathParamString
			return url
	
	def get(self, pathParams, needAccountNo = True, stream = False, **queryParams):
			url = self.buildUrl(pathParams, needAccountNo, stream)
			print(url)
			self.response = requests.get(
				url,
				headers = self.credentials.getToken(),
				params = queryParams,
				stream = stream
			)
			return self.response
			
	def post(self, pathParams, data = '', needAccountNo = True, stream = False, **queryParams):
		header = self.credentials.getToken()
		header['Content-Type'] = 'application/json'
		url = self.buildUrl(pathParams, needAccountNo, stream)
		self.response = requests.post(
			url,
			data = data,
			headers = header,
			params = queryParams,
			stream = stream
		)
		return self.response
				
	
	def getTrades(self):
		self.trades = requests.get(
			'https://api-fxpractice.oanda.com/v3/accounts/' + self.credentials.getAccountNo() + '/trades?instrument=EUR_HUF',
			headers = self.credentials.getToken()
		)
		return self.trades
	
	def put(self, pathParams, data = '', needAccountNo = True, stream = False, **queryParams):
		header = self.credentials.getToken()
		header['Content-Type'] = 'application/json'
		url = self.buildUrl(pathParams, needAccountNo, stream)
		self.response = requests.put(
			url,
			data = data,
			headers = header,
			params = queryParams,
			stream = stream
		)
		return self.response	
		
		
		
				
	def makeOrder(self):
		self.order = self.post(
		{
			endPoints.orders: ''
		},
		data = json.dumps({
						"order": {
							"units": "1",
							"instrument": "EUR_HUF",
							"timeInForce": "FOK",
							"type": "MARKET",
							"positionFill": "DEFAULT"
						}
					}),
		)
		return self.order
		
		
				
	#def makeOrder(self):
#		self.order = requests.post(
#			'https://api-fxpractice.oanda.com/v3/accounts/' + self.credentials.getAccountNo() + '/orders',
#				data = json.dumps({
#				"order": {
#					"units": "1",
#					"instrument": "EUR_HUF",
#					"timeInForce": "FOK",
#					"type": "MARKET",
#					"positionFill": "DEFAULT"
#				}
#			}),
#			headers = self.credentials.getToken()
#		)
#		return self.order