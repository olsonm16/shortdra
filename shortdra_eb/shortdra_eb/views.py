from django.http import HttpResponse, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from models import ShortLink
from django.views.decorators.csrf import ensure_csrf_cookie
import django.middleware.csrf
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template.context_processors import csrf
import urllib

def root(request):
	return HttpResponseRedirect("http://hydras.slack.com")

def dispatcher(request, string):
	try:
		link = ShortLink.objects.get(string__exact=string)
	except ObjectDoesNotExist:
		redirect_url = "http://hydras.slack.com"
	else:
		redirect_url = link.get_url()
	return HttpResponseRedirect(redirect_url)

@ensure_csrf_cookie
def creator(request):
	c = {}
	c['CSRF_TOKEN'] = csrf(request)
	return render(request, "create.html", c)

def transact(request):
	split = request.body.split("&")
	text = split[0].split("=")[1]
	raw_url = split[1].split("=")[1]
	url = urllib.unquote(raw_url).decode('utf8') 
	if ("http://" not in url) and ("https://" not in url):
		url = "http://" + url
	try:
		link = ShortLink.objects.get(string__exact=text)
	except ObjectDoesNotExist:
		link = ShortLink(string=text, url=url)
		link.save(force_insert=True)
	else:
		 link.url = url
		 link.save()

	return HttpResponse("Success!")

def see_all(request):
	return HttpResponse(str(ShortLink.objects.all()))