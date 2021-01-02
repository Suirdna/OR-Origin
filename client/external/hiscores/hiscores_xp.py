import http.client
import math

name = "hiscores"

class Hiscores(object):

	username = None
	accountType = None
	response = None
	status = None
	data = None
	info = None
	subset = None
	level = None
	stats = None

	def __init__(self, username: str, actype='N'):
		self.username = username
		self.accountType = actype
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
			pass
		else:
			self.data = self.response.read().decode('ascii')
			self.parseData()

	def parseData(self):
		self.data = self.data.replace('\n', ',')
		self.data = self.data.split(',')
		self.subset = {}

		self.info = {}
		self.info['rank'] = self.data[0]
		self.info['level'] = self.data[1]
		self.info['experience'] = self.data[2]
		self.subset['total'] = self.info

		skills = [
			'attack',
			'defense',
			'strength',
			'hitpoints',
			'ranged',
			'prayer',
			'magic',
			'cooking',
			'woodcutting',
			'fletching',
			'fishing',
			'firemaking',
			'crafting',
			'smithing',
			'mining',
			'herblore',
			'agility',
			'thieving',
			'slayer',
			'farming',
			'runecrafting',
			'hunter',
			'construction'
		]
		counter = 0
		for i in range(len(skills)):
			self.info = {}
			self.info['rank'] = int(self.data[counter+3])
			self.info['level'] = int(self.data[counter+4])
			self.info['experience'] = int(self.data[counter+5])
			self.level = int(self.info['level']+1)
			self.info['next_level_exp'] = math.floor(sum((math.floor(self.level + 300 * (2 ** (self.level / 7.0))) for self.level in range(1, self.level)))/4)
			self.info['exp_to_next_level'] = int(self.info['next_level_exp'] - self.info['experience'])
			self.subset[skills[i]] = self.info
			counter += 3

		self.stats = self.subset

	def skill(self, skill, stype: str = 'level'):
		try:
			if stype.lower() not in ['rank', 'level', 'experience', 'next_level_exp', 'exp_to_next_level']:
				pass
			else:
				return self.stats[skill.lower()][stype.lower()]
			self.reset()
		except KeyError as KE:
			pass

	def reset(self):
		self.username = None
		self.accountType = None
		self.response = None
		self.status = None
		self.data = None
		self.info = None
		self.subset = None
		self.level = None
		self.stats = None

