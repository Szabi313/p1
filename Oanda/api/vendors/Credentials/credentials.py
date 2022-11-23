import json

class Credentials:
	credentials = ''
	def __init__ (self):
		try:
			with open('api/vendors/Credentials/credentials.json') as file:
				self.credentials = json.loads(file.read())
		except:
			print('Failed to load credentials')
	
	def getToken(self):
		if self.credentials['token']:
			return self.credentials['token']
		else:
			return False
		
	def getAccountNo(self):
	#	print(self.credentials)
		if self.credentials['accountNo']:
			return self.credentials['accountNo']
		else:
			return False
		
	def setToken(self, token):
		self.token = token
