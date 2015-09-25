from lxml import html
import datetime
import requests
from netflix_models import NetflixContent, NetflixDay
from plot_netflix import plot_history

def parse_netflix(text):

	tree = html.fromstring(text)
	lyst = tree.find_class("retableRow")
	history = {}
	format = '%m/%d/%Y'

	name = tree.find_class("name")[0].text_content()
	#name = 'beta2_tester'

	#n = 10

	for elem in lyst:
	#for i in range(n):
		x = elem.text_content().encode('utf-8').strip()
		#x = lyst[i].text_content().encode('utf-8').strip()
		y = x.split("Report")[0]
		z = y.split("/")

		month = z[0]
		day = z[1]
		year = '20' + z[2][0:2]
		title = z[2][2:]

		if "Season" in title or "Series" in title:
			terms = title.split(":")
			show_name = terms[0]
			if " (" in show_name:
				show_name = show_name.split(" (")[0]
			episode = terms[2].replace('"', "").replace("\\", "")

			this_content = NetflixContent(episode, "tvEpisode", 0, show_name)
			request = 'http://itunes.apple.com/search?term=' + episode + " " + show_name + '&artistName=' + show_name + '&entity=tvEpisode'

		else:
			show_name = title.replace("\\", "")
			this_content = NetflixContent(show_name, "movie", 0)
			request = 'http://itunes.apple.com/search?term=' + title + '&entity=movie'

		r = requests.get(request)

		try:
			content_length = 0
			for result in r.json()['results']:
				if result['artistName'] == show_name:
					content_length += round(float(r.json()['results'][0]['trackTimeMillis'])/60000, 0)
					this_content.update_length(content_length)
					break
		except:
			content_length = 0

		if content_length == 0:

			wiki_req = "http://en.wikipedia.org/wiki/" + show_name.replace(" ", "_")

			page = requests.get(wiki_req)
			if page.status_code == 200:
				tree = html.fromstring(page.text)
				try:
					info = tree.find_class('infobox vevent')[0]
					for elem in info:
						if "Running time" in elem.text_content().encode('utf-8').strip():
							array = elem.text_content().split("\n")
							for elem in array:
								if "minutes" in elem:
									x = str(elem.encode('utf-8').strip()).split("\xe2\x80\x93")
									if len(x) > 1:
										lower = float(x[0])
										upper = float(x[1].split("minutes")[0])
										content_length = (upper + lower) / 2
										this_content.update_length(content_length)
									else:
										content_length = float(elem.split(" ")[0])
										this_content.update_length(content_length)
				except:
					content_length += 0

		date_string = month + "/" + day + "/" + year

		date = datetime.datetime.strptime(date_string, format)

		if date not in history:
			history[date] = NetflixDay(date)
			history[date].add_content(this_content)
			history[date].update_mins(content_length)
		else:
			history[date].add_content(this_content)
			history[date].update_mins(content_length)

	awesome_content = []
	for date in history.keys():
		awesome_content.append(str(history[date]))
		for content in history[date].get_content():
			awesome_content.append(str(content))
		awesome_content.append(str(history[date].most_freq_content()))

	return plot_history(history, name, awesome_content)

	#return history






