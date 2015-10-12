
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Q
from django.contrib import auth
import datetime
import re
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
    # TODO:  Bootstrap Validator

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
    ### this is beauty the captcha input

    # img_src = captcha['pic']['src']
    # input1_value = captcha['input1']['value']
    # 'img_src':img_src, 'input1_value':input1_value,
    '''<div class="form-group">
      <label for="id_captcha_1">Captcha:</label>
      <img src="{{img_src}}" alt="captcha" class="captcha" />
      {% if errorlist_content %}
      <div class="alert alert-danger" role="alert">{{errorlist_content}}</div>
      {% endif %}
      <input id="id_captcha_0" name="captcha_0" type="hidden" value="{{input1_value}}" />
      <input autocomplete="off" id="id_captcha_1" type="text" class="form-control" name="captcha_1" placeholder="code">
    </div>'''
    return render_to_response('register.html', {'captcha':form, 'messageType':messageType,'message':message},context_instance=RequestContext(request))



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


def captchaFormat(str_form):
    # print (str(str_form))
    label = re.findall(r'<label for="([_a-z0-9A-Z]*)">([:a-zA-Z0-9]*)</label>',str(str_form))
    label = {'for':label[0][0],'content':label[0][1]}

    errorlist = re.findall(r'<ul class="([a-z0-9A-Z]*)"><li>([\s0-9A-Za-z]*)</li>',str(str_form))
    try:
        errorlist = {'class':errorlist[0][0],'content':errorlist[0][1]}
    except:
        errorlist = None

    pic = re.findall(r'<img src="([/a-z0-9A-Z]*)" alt="([a-zA-Z0-9]*)" class="([a-zA-Z0-9]*)" />',str(str_form))
    pic = {'src':pic[0][0],'alt':pic[0][1],'class':pic[0][2]}

    input1 = re.findall(r'<input id="([_a-z0-9A-Z]*)" name="([_a-zA-Z0-9]*)" type="([a-zA-Z0-9]*)" value="([a-zA-Z0-9]*)" />',str(str_form))
    input1 = {'id':input1[0][0],'name':input1[0][1],'type':input1[0][2],'value':input1[0][3]}

    input2 = re.findall(r'<input autocomplete="([a-z0-9A-Z]*)" id="([_a-zA-Z0-9]*)" name="([_a-zA-Z0-9]*)" type="([a-zA-Z0-9]*)" />',str(str_form))
    input2 = {'autocomplete':input2[0][0],'id':input2[0][1],'name':input2[0][2],'type':input2[0][3]}
    str_form = {'label':label,'errorlist':errorlist,'pic':pic,'input1':input1,'input2':input2}
    # print (str_form)
    return str_form


## TODO: HOME PAGE, USER filter