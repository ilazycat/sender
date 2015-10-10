
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Q
from grade.models import users
from django.contrib import auth
import datetime
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.models import User
from django import forms
from captcha.fields import CaptchaField
from captcha.models import CaptchaStore
class CaptchaTestForm(forms.Form):
    captcha = CaptchaField()





def current_datetime(request):
    now = datetime.datetime.now()
    return render_to_response('current_datetime.html',{'current_datetime':now})

def hours_ahead(request, offset):
    offset = int(offset)
    dt = datetime.datetime.now() + datetime.timedelta(hours = offset)
    html = "<html><body>In %s hour(s), it will be %s.</body></html>" % (offset, dt)
    return HttpResponse(html)

def search(request):
    query = request.GET.get('q','')
    if query:
        qset = (
            Q(username__contains=query) |
            Q(email__contains=query)
        )
        results = users.objects.filter(qset).distinct()
    else:
        results = []
    return render_to_response('search.html',{
        "results":results,
        "query":query
        })


def Index(request):
# the index page for all
    if request.user.is_authenticated:
        return render_to_response('index.html',{'title':'hello '+request.user.username})
    return render_to_response('index.html',{'title':'hello~~~~'})
def Register(request):
    # TODO:  vcode for same ip many times

    #filter the input
    ### POST > vcode > input
    messageType = 'danger'      # default
    if request.POST:
        form = CaptchaTestForm(request.POST)
        if form.is_valid():
            human = True
            errormessage = 'code was true, no input'
            if ('username' in request.POST and 'password' in request.POST and 'email' in request.POST):
                ##### TODO: test inpu
                username  = filterInput(request.POST['username'])
                password  = filterInput(request.POST['password'])
                email     = filterInput(request.POST['email'])
                try:
                    user = User.objects.create_user(username, email, password)
                    user.save()
                    messageType = 'success'
                    message = 'code was true,user can add'
                except:
                    message = 'code was true, user can not add'
        else:
            message = 'code was wrong'
    else:
        form = CaptchaTestForm()
        messageType = 'info'
        message = 'No input'

    return render_to_response('register.html', {'captcha':form,'messageType':messageType,'message':message},context_instance=RequestContext(request))



def Login(request):
    # assert False

    if ('username' in request.POST and 'password' in request.POST):
        username = request.POST.get('username','')
        password = request.POST.get('password','')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/home/')
            else:
                return render_to_response('login.html',{"errormessage":username+" is not active."}, context_instance=RequestContext(request))
        else:
            return render_to_response('login.html',{"errormessage":"username and password are not match.",'username':username}, context_instance=RequestContext(request))
    else:
        return render_to_response('login.html',context_instance=RequestContext(request))



def Logout(request):
    logout(request)
    return HttpResponseRedirect('/index/')


def Home(request):
    if request.user.is_authenticated:
        return render_to_response('home.html',{'title':request.user.username,'user':request.user.username},context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/index/')


def filterInput(inner):
    ## filter
    return inner