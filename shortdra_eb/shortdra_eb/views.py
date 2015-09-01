from django.http import HttpResponse, HttpResponseRedirect

def root(request):
	return HttpResponseRedirect("http://hydras.slack.com")

def dispatcher(request, string):
	urls = {'default':"http://apple.com", 'awesome':"http://reddit.com"}
	if string in urls:
		return HttpResponseRedirect(urls[string])
	else:
		return HttpResponseRedirect("http://www.google.com")