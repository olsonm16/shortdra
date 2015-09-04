from django.http import HttpResponse, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from models import ShortLink
from django.views.decorators.csrf import ensure_csrf_cookie
import django.middleware.csrf
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template.context_processors import csrf
import urllib

from netflix import parse_netflix

def root(request):
	scheme = "http" if not request.is_secure() else "https"
	path = request.get_full_path()
	domain = request.META.get('HTTP_HOST') or request.META.get('SERVER_NAME')
	pieces = domain.split('.')
	if "shortdra" in pieces:
		return creator(request)
	elif "flixdra" in pieces:
		return flixdra(request)
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
	raw_text = split[0].split("=")[1]
	raw_url = split[1].split("=")[1]
	url = urllib.unquote(raw_url).decode('utf8') 
	text = urllib.unquote(raw_text).decode('utf8') 
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

@ensure_csrf_cookie
def see_all(request):
	c = {}
	c['CSRF_TOKEN'] = csrf(request)
	links = ShortLink.objects.all()
	c['links'] = links
	return render(request, "see_all.html", c)

def delete(request):

	raw_string = request.body.split("=")[1]
	string = urllib.unquote(raw_string).decode('utf8') 

	try:
		link = ShortLink.objects.get(string__exact=string)
	except ObjectDoesNotExist:
		return HttpResponse("The object does not exist")
	else:
		ShortLink.objects.get(string__exact=string).delete()
		return HttpResponse("The link for " + string + " was deleted")

@ensure_csrf_cookie
def flixdra(request):
	c = {}
	c['CSRF_TOKEN'] = csrf(request)
	if request.method == 'POST':
		file = request.FILES['myfile']
		url, awesome_content =  parse_netflix(file.read())
		c['graph_link'] = url
		c['awesome_content'] = awesome_content
		return render(request, "flixdra_results.html", c)
	else:
		return render(request, "flixdra.html", c)





