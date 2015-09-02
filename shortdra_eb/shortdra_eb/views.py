from django.http import HttpResponse, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from models import ShortLink
from django.shortcuts import render

def root(request):
	return HttpResponseRedirect("http://hydras.slack.com")

def dispatcher(request, string):
	if string == "create":
		return render(request, "create.html")
	try:
		link = ShortLink.objects.get(string__exact=string)
	except ObjectDoesNotExist:
		redirect_url = "http://hydras.slack.com"
	else:
		redirect_url = link.get_url()
	return HttpResponseRedirect(redirect_url)

def creator(request):
	return render(request, "create.html")