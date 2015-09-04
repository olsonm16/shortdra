class NetflixDay(object):

	def __init__(self, date):
		self.date = date
		self.mins = 0
		self.content = []

	def update_mins(self, mins):
		self.mins += mins

	def add_content(self, content):
		self.content.append(content)

	def get_mins(self):
		return self.mins

	def get_date(self):
		return self.date

	def get_content(self):
		return self.content

	def __str__(self):
		s = "On " + str(self.date).split(" ")[0] + ", you watched: " + str(self.mins) + " minutes of Netflix."
		return s

	def most_freq_content(self):
		d = {}
		if len(self.content) > 0:
			for item in self.content:
				if item.seriesName != None:
					if item.seriesName in d:
						d[item.seriesName] += 1
					else:
						d[item.seriesName] = 1
			
			max = 0
			name = None
			for elem in d.keys():
				if d[elem] > max:
					name = elem
					max = d[elem]

			if name != None:
				return "You viewed " + name + " the most, at a count of: " + str(max) + "."
			else:
				return "No content viewed on that day"
		else:
			return "No content viewed on that day"

class NetflixContent(object):
	
	def __init__(self, title, type, length, seriesName=None):
		self.title = title
		self.type = type
		self.length = length
		self.seriesName = seriesName

	def __str__(self):
		s = ""
		if self.seriesName != None:
			s = "Content: " + self.seriesName + ": " + self.title + " | Runtime: " + str(self.length) + " mins."
		else:
			s = "Content: " + self.title + " | Runtime: " + str(self.length) + " mins."
		return s

	def update_length(self, length):
		self.length += length
