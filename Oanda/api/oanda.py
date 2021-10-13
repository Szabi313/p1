import requests
from bunch import Bunch
from api.vendors.Credentials.credentials import Credentials
import json
from api.api import ApiInterface

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

class oaRequest(ApiInterface):
	credentials = Credentials()
	response = ''
	order = ''
	stream = ''
	
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
		
		
	##
	# TRADE RELATED FUNCTIONS
	#	
	
	def getTrades(self, instrument):
		self.trades = requests.get(
			'https://api-fxpractice.oanda.com/v3/accounts/' + self.credentials.getAccountNo() + '/trades?instrument=' + instrument,
			headers = self.credentials.getToken()
		)
		return self.trades	
		
				
	def makeOrder(self, instrument):
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
		
		
	def getPriceStream(self, currency):	
		stream = self.get(
			{
				endPoints.pricing: '',
				endPoints.stream: ''
			},
			instruments = currency,
			stream = True
		)	
		return stream
		
		
	def closePosition(self, positionId, volume):
		close = self.put(
		{
			endPoints.trades: positionId,
			endPoints.close: ''
		},
		data = json.dumps({ 'units': volume})
		)
		return close


		
#c = oaRequest()
				
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