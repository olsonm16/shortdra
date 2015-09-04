import plotly.plotly as py
from plotly.graph_objs import *

def plot_history(history, name, awesome_content):
	py.sign_in('mitchhydras','wi2qaykd8l')
	days = []
	times = []

	for date in history.keys():
		days.append(str(date).split(" ")[0])
		times.append(history[date].get_mins()/60)

	trace0 = Bar(x=days,
	    y=times
	)

	data = [trace0]

	layout = Layout(
		    title='Netflix Data for ' + name,
		    xaxis=XAxis(
		        title='Date',
		        titlefont=Font(
		            family='Courier New, monospace',
		            size=18,
		            color='#7f7f7f'
		        )
		    ),
		    yaxis=YAxis(
		        title='Hours of Content Viewed',
		        titlefont=Font(
		            family='Courier New, monospace',
		            size=18,
		            color='#7f7f7f'
		        )
		    )
		)

	fig = Figure(data=data, layout=layout)

	unique_url = py.plot(fig, filename = name + " netflix-history")

	return unique_url, awesome_content