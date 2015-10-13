
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
import datetime
import re
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from grade.models import grades,userinfo
from django import forms
from django.contrib.auth.models import User # 创建用户
from captcha.fields import CaptchaField
from captcha.models import CaptchaStore
class CaptchaTestForm(forms.Form):
    captcha = CaptchaField()

def filterUsername(raw_username):
    # special permit map: _
    username = re.findall(r'^[a-zA-Z0-9_-]{5,18}$',raw_username)
    if (username):
        return username[0]
    else:
        return False

def filterPassword(raw_password):
    # special permit map: !@$&*,.?_
    password = re.findall(r'^[a-zA-Z0-9!@$&*,.?_-]{6,18}$',raw_password)
    if (password):
        return password[0]
    else:
        return False

def filterEmail(raw_email):
    # special permit map: !@$&*,.?_
    email = re.findall(r'^[a-zA-Z0-9._-]+\@[a-zA-Z0-9_-]+\.[a-zA-Z0-9._-]+$',raw_email)
    if (email):
        return email[0]
    else:
        return False

def query(table):
    return eval(table+'.objects')


def current_datetime(request):
    now = datetime.datetime.now()
    return render_to_response('current_datetime.html',{'current_datetime':now})

def hours_ahead(request, offset):
    offset = int(offset)
    dt = datetime.datetime.now() + datetime.timedelta(hours = offset)
    html = "<html><body>In %s hour(s), it will be %s.</body></html>" % (offset, dt)
    return HttpResponse(html)



def Index(request):
# the index page for all
    if request.user.is_authenticated():
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
                username = filterUsername(request.POST.get('username',''))
                password = filterPassword(request.POST.get('password',''))
                email    = filterEmail(request.POST.get('email',''))
                try:
                    if (username and password and email):
                        user = User.objects.create_user(username, email, password)
                        user.save()
                        messageType = 'success'
                        message = 'code was true,user can add'
                        return HttpResponseRedirect('/login/')
                    else:
                        # print (username,password,email)
                        message = 'Please check your input'
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
    return render_to_response('register.html', {'captcha':form, 'messageType':messageType,'message':message},context_instance=RequestContext(request))



def Login(request):
    errormessage = None
    if request.user.is_authenticated():# had login
        return HttpResponseRedirect('/home/')
    if request.POST:
        form = CaptchaTestForm(request.POST)
        if form.is_valid():
            human = True
            if ('username' in request.POST and 'password' in request.POST):
                username = filterUsername(request.POST.get('username',''))
                password = filterPassword(request.POST.get('password',''))
                user = authenticate(username=username, password=password)
                if user is not None:# no this user
                    if user.is_active:
                        login(request, user)
                        return HttpResponseRedirect('/home/') #login success
                    else:# user not active
                        errormessage = 'username' + ' is not active.'
                else:#password wrong
                    errormessage = 'username and password are not match.'
            else:#no username,password value
                errormessage = 'What are you doing?'
    else:# GET
        form = CaptchaTestForm()
    return render_to_response('login.html',{'captcha':form,'errormessage':errormessage},context_instance=RequestContext(request))



def Logout(request):
    logout(request)
    return HttpResponseRedirect('/index/')


def Home(request):
    # @login_required
    if request.user.is_authenticated():
        return render_to_response('home.html',{'title':request.user.username+'\'s home page','user':request.user.username},context_instance=RequestContext(request))
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



def Manage(request):
    if request.user.is_authenticated():
        return render_to_response('manage.html',{'user':request.user.username})

    else:
        return HttpResponseRedirect('/login/')

## TODO: manage