import requests
import json
import argparse

parser = argparse.ArgumentParser(
	description = 'Get stream of instrument(s)'
)

parser.add_argument(
	'-i',
	'--instrument',
	type = str,
	default = 'EUR_HUF',
	help = 'The name of the instrument to be streamed'
)

parser.add_argument(
	'-a',
	'--availableInstruments',
	action = 'store_true',
	help = 'Getting available instruments'
)

instNS = parser.parse_args()

if instNS.availableInstruments:
	instruments = requests.get(
	'https://api-fxpractice.oanda.com/v3/accounts/101-004-12179526-002/instruments',
	headers = {
		"Authorization": "Bearer 368e6d4f7dd220c764ca398fe1292dcb-f2814012173473fd0feb1fe1d3233033"
	})
	instFormat = 'Name: {}, type: {}'
	instruments = instruments.json()
	for instrument in instruments['instruments']:
		print(instFormat.format(instrument['name'], instrument['type']))
		
if instNS.instrument:
	instNS.instrument = instNS.instrument.upper()
	if '_' not in instNS.instrument or instNS.instrument[0] == '_':
		msg = 'The instrument {} format doesn\'t match'
		print(msg.format(instNS.instrument))
	else:
		response = requests.get(
			'https://stream-fxpractice.oanda.com/v3/accounts/101-004-12179526-002/pricing/stream',
			headers = {
				"Authorization": "Bearer 368e6d4f7dd220c764ca398fe1292dcb-f2814012173473fd0feb1fe1d3233033"
			},
			params = {
				"instruments": instNS.instrument,
			},
			stream = True
		)
		
		for line in response.iter_lines():
			lineP = json.loads(line)
			print(json.dumps(lineP, indent = 4))