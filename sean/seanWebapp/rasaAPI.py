import json
import requests

RASA = "http://localhost:5005"
RASA_API = RASA + "/webhooks/rest/webhook"


def helloworld():
	response = requests.request("GET", RASA)
	return response.text

def version():
	headers = {
		'Content-Type':"application/json",
	}

	response = requests.request("GET", RASA +"/version", headers=headers)

	return response.text

def message(message, sender="TheLegend27", debug=0):
	data = {
		"sender":sender,
		"message":str(message)
	}

	headers = {
		'Content-Type':"application/json",
    	'X-Requested-With': 'XMLHttpRequest',
    	'Connection': 'keep-alive',
	}

	try:
		response = requests.post(RASA_API, data=json.dumps(data), headers=headers)
	except:
		# no response from rasa server, is it running?
		return {"text":"ERROR 1"}
		
	if (debug == 1):
		print(response.status_code)
		print(response.content)
		print(json.loads(response.text))

	try:
		return json.loads(response.text)
	except:
		# something wrong with rasa server, it's running, but not working
		return {"text":"ERROR 0"}