import json
import requests

TOKEN_FILE = "api_token.txt"
MAX_PINS = 25 #maximum number of pins that can be returned by the API


class pinterest_request:
	def __init__(self):
		self.base_url = "https://api.pinterest.com/v1/"
		self.boardExtension = "boards/"
		self.pinExtension = "pins"
		self.getToken()

	#gets the API token
	def getToken(self):
		with open(TOKEN_FILE, "rb") as f:
			for line in f: 
				self.api_token = line

	def makeRequest_pins(self, board_id, params = {}):
		params["access_token"] = self.api_token
		params["cursor"] = None
		params["limit"] = MAX_PINS
		params["fields"] = ["image", "id"]

		url = "%s%s%s%s" %(self.base_url, self.boardExtension, board_id + "/", self.pinExtension)
		responseList = []
		hasNextPins = True

		try:
			while hasNextPins:
				response = requests.get(url, params = params)

				#there was a 404 error
				if response.status_code == 404:
					return True, responseList

				json_response = response.json()
				#adding pins and metadata to a list that will be returned
				responseList.append(json_response)
				hasNextPins = json_response["page"]["next"] is not None
				url = json_response["page"]["next"]

			return True, responseList

		except requests.exceptions.RequestException as e:
			return False, None



def main():
	pinterest_request() #runs pinterest request

if __name__ == "__main__":
	main()