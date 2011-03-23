from django.http import HttpResponseRedirect, HttpResponseNotFound, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from django.conf import settings
from talkcode.models import *
from talkcode.forms import *

from django.template.context import RequestContext
from django.core.xheaders import populate_xheaders

from nltk import pos_tag, word_tokenize, RegexpParser

key_words = ["function", "class", "to", "do", "comment", "method", "variable", "integer", "string", "double", "float", "constructor", "destructor", "create"]

def choose_best_phrase(matches):
	max = 0
	best = word_tokenize(matches[0])
	
	for match in matches:	
		words = word_tokenize(match)
		count = 0
		for word in words:
			if word in key_words:
				count += 1
		
		if find_todo(words) >= 0:
			count += 2		
		
		if count > max:
			max = count
			best = words
	return best


def find_todo(phrase):
	for i in range(len(phrase)-2):
		if phrase[i] == "to" and phrase[i+1] == "do":
			return i
	return -1

def find_comment(phrase):
	for i in range(len(phrase)-2):
		if phrase[i].endswith("omen") or phrase[i] == "comment":
			return i
		elif phrase[i] == "call" and phrase[i+1] == "maine":
			return i+1
	return -1

def process_voice(phrase):
	res = ""
	
	# find TODO
	i = find_todo(phrase)
	if i >= 0:
		for k in range(i+2, len(phrase)):
			res += phrase[k]
			res += " "
		return "{todo:%s}" % res
	
	i = find_comment(phrase)
	if i >= 0:
		for k in range(i+1, len(phrase)):
			res += phrase[k]
			res += " "
		return "{comment:%s}" % res
	
	res = ""
	for k in range(len(phrase)):
		res += phrase[k]
		res += " "
	return "{error:%s}" % res


def render(request, template, context={}):
    """Render helper method"""
    return render_to_response(template, context, context_instance=RequestContext(request))

def index(request):
	return render(request, 'index.html')

def register(request):
    """Register a new account/user"""
    
    if request.method == 'POST':
        form = AccountProfileForm(request.POST, request.FILES)
        user_form = UserCreationForm(request.POST, request.FILES)
        
        if user_form.is_valid():
        	account = form.save()
        	account.create_user(user_form)
        	return HttpResponseRedirect('/')
    else:
        user_form = UserCreationForm()
    return render(request, 'accounts/register.html', {'user_form':user_form})

def add(request):
	
	if request.method == 'GET':
	
		username = request.GET["user"]
		password = request.GET["pass"]
    	
		user = authenticate(username=username, password=password)
		if user == None:
			return HttpResponse("error: authentication")
    	
		# get sentences sended by the client
		sentences = request.GET["matches"]
		phrases = sentences.split("|")
		
		
		
		
		best = choose_best_phrase(phrases)
		# TODO process sentences here
		
		res = process_voice(best)
		
		operation = CodeOperation(user=user, code=res)
		operation.save()
		
		response = "ok"
	else:
		response = "error: method not supported! use GET"
	return HttpResponse(response)


def get(request):
	
	
	if not request.method == 'GET':
		return HttpResponse("{error: method not supported! use GET}")
	username = request.GET["user"]
	password = request.GET["pass"]
	
	user = authenticate(username=username, password=password)
	
	if user == None:
		return HttpResponse("{error:authentication}")

	operations = CodeOperation.objects.filter(user=user)
	if len(operations) > 0:
		result = operations[0].code
		operations[0].delete()
	else:
		result = "{}"
		
	return HttpResponse(result)
   

