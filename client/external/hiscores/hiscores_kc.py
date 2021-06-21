import http.client

name = "hiscores2v"

class Hiscores2V(object):
	response = None
	status = None
	errorMsg = None
	counter = 96 #constant
	data = None

	bossList = {'data': []}

	def __init__(self, username: str, list1, list2, actype='N',):
		self.username = username
		self.accountType = actype
		self.boss = list1
		self.pre = list2
		self.getHTTPResponse()

	def getHTTPResponse(self):
		conn = http.client.HTTPSConnection('secure.runescape.com')
		if self.accountType == 'N':
			conn.request("GET", "/m=hiscore_oldschool/index_lite.ws?player={}".format(self.username))
			self.response = conn.getresponse()
			self.status = self.response.status
		elif self.accountType == 'IM':
			conn.request("GET", "/m=hiscore_oldschool_ironman/index_lite.ws?player={}".format(self.username))
			self.response = conn.getresponse()
			self.status = self.response.status
		elif self.accountType == "UIM":
			conn.request("GET", "/m=hiscore_oldschool_ultimate/index_lite.ws?player={}".format(self.username))
			self.response = conn.getresponse()
			self.status = self.response.status
		elif self.accountType == "HIM":
			conn.request("GET", "/m=hiscore_oldschool_hardcore_ironman/index_lite.ws?player={}".format(self.username))
			self.response = conn.getresponse()
			self.status = self.response.status
		self.processResponse()
		conn.close()

	def processResponse(self):
		if self.status != 200:
			self.errorMsg = "Player name given not found in account type provided.  Valid account types are, 'N' (Normal), 'IM' (Iron Man), 'UIM' (Ultimate Iron Man), 'HIC' (Hardcore Iron Man)"
		else:
			self.data = self.response.read().decode('ascii')
			self.parseData()

	def parseData(self):
		self.data = self.data.replace('\n', ',')
		self.data = self.data.split(',')

		boss = self.boss
		pre = self.pre

		self.data = self.data[self.counter:len(self.data) - 1]
		index = 0
		indexx = 1

		self.bossList['data'].clear()

		while index < 46:
			self.bossList['data'].append({'rank': 0 if int(self.data[indexx - 1]) == -1 else int(self.data[indexx - 1]), 'boss': boss[index], 'pre': pre[index], 'kc': 0 if int(self.data[indexx]) == -1 else self.data[indexx]})
			index += 1
			indexx += 2

	def getKc(self, bossName):
		for data in self.bossList['data']:
			if str(data['boss']).lower() == str(bossName).lower():
				return data

			if str(data['pre']).lower() == str(bossName).lower():
				return data
		return False






