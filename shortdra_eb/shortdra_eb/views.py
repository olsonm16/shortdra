from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from models import ShortLink, Post, Author
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
import django.middleware.csrf
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template.context_processors import csrf
import urllib
import requests
import json

from netflix import parse_netflix

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def get_client_location(ip):
	request = 'http://ipinfo.io/' + str(ip)
	r = requests.get(request)
	return r.json()

def city_state(json):
	try:
		text = "Thanks for visiting us from: " + str(json['city']) + ', ' + str(json['region']) + "!"
	except:
		text = "Unknown location"
	return text


def root(request):
	scheme = "http" if not request.is_secure() else "https"
	path = request.get_full_path()
	domain = request.META.get('HTTP_HOST') or request.META.get('SERVER_NAME')
	pieces = domain.split('.')
	r = city_state(get_client_location(get_client_ip(request)))
	if len(pieces) == 3:
		if "shortdra" in pieces:
			return creator(request)
		elif "flixdra" in pieces:
			return flixdra(request)
		elif "mail" in pieces:
			return HttpResponseRedirect("https://www.zoho.com/mail/login.html")
		elif "blog" in pieces:
			return blogger(request)
		elif "ip" in pieces:
			return HttpResponse(str(r))
		else:
			return dispatcher(request, pieces[0])
	
	return HttpResponseRedirect("http://hydras.slack.com")

def dispatcher(request, string):
	try:
		link = ShortLink.objects.get(string__exact=string)
	except ObjectDoesNotExist:
		redirect_url = "http://hydras.slack.com"
	else:
		redirect_url = link.get_url()
	return HttpResponseRedirect(redirect_url)

def blogger(request):
	posts = Post.objects.all()
	return HttpResponse(str(posts))
	
@ensure_csrf_cookie
def creator(request):
	c = {}
	c['csrftoken'] = csrf(request)
	print(c)
	return render(request, "create.html", c)

@csrf_exempt
def make_link(request):
	string = ""
	url = ""
	response_status = 200
	if request.method == 'POST':
		query_dict = request.POST.dict()
		try:
			string = str(query_dict[u'string'])
			url = str(query_dict[u'link'])
		except:
			response_status = 400
			response_text = "Malformed request: please make sure your request includes a string and url field in its body."

		if linkAvaliable(string):
			saveLink(string, url)
			response_text = "Link created!"
		else:
			response_status = 422
			response_text = "Sorry, that shortlink is already taken."

	else:
		response_status = 400
		response_text = "Please use a POST request."

	return JsonResponse(response_builder(response_status, response_text))

def response_builder(status, text):
	r = {}
	r['status_code'] = str(status)
	r['body'] = {}
	r['body']['message'] = text
	return r

def linkAvaliable(string):
	try:
		link = ShortLink.objects.get(string__exact=string)
	except ObjectDoesNotExist:
		return True
	return False

def saveLink(text, url):
	if ("http://" not in url) and ("https://" not in url):
		url = "http://" + url
	link = ShortLink(string=text, url=url)
	link.save(force_insert=True)


@ensure_csrf_cookie
def see_all(request):
	c = {}
	c['CSRF_TOKEN'] = csrf(request)
	links = ShortLink.objects.all()
	c['links'] = links
	return render(request, "see_all.html", c)

@csrf_exempt
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





