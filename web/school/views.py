# -*- coding:UTF-8 -*-
__author__ = 'lc4t'
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
import datetime
import re
import os
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.template import RequestContext
from school.models import grades,userinfo,information
from django import forms
from django.contrib.auth.models import User
from captcha.fields import CaptchaField
from captcha.models import CaptchaStore
import subprocess
# from functions.Uestc import Exec
# from functions.Uestc2db import DB_uestc
from functions.school_uestc_grade_check_api import API as uestc
import json
class CaptchaTestForm(forms.Form):
    captcha = CaptchaField()

def filterUsername(raw_username):
    # special permit map: _
    username = re.findall(r'^[a-zA-Z0-9_-]{4,18}$',raw_username)
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


def Index(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/home/')
    function = [
    {
        'author': 'lc4t',
        'descript': 'uestc成绩更新通知',
        'submit': '2015.1.22'
    }
    ]
    return render(request, 'index.html',{'title':'Welcome', 'user': False, 'function': function})


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
            message = 'code was true, no input'
            if ('username' in request.POST and 'password' in request.POST and 'email' in request.POST):
                username = filterUsername(request.POST.get('username',''))
                password = filterPassword(request.POST.get('password',''))
                email    = filterEmail(request.POST.get('email',''))
                try:
                    if (username and password and email):
                        user = User.objects.create_user(username, email, password)
                        messageType = 'success'
                        message = 'code was true,user can add'
                        user = authenticate(username=username, password=password)
                        login(request, user)
                        return HttpResponseRedirect('/home/')
                    else:
                        # print (username,password,email)
                        message = 'Please check your input,May not in permission'
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
    return render(request, 'register.html', {'captcha':form, 'messageType':messageType,'message':message})



def Login(request):
    message = None
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
                        message = 'username' + ' is not active.'
                else:#password wrong
                    message = 'username and password are not match.'
            else:#no username,password value
                message = 'What are you doing?'
    else:# GET
        form = CaptchaTestForm()
    return render(request, 'login.html',{'captcha':form,'message':message})



def Logout(request):
    logout(request)
    return HttpResponseRedirect('/index/')


def Home(request):
    # @login_required
    if request.user.is_authenticated():
        return render(request, 'home.html',{'title':request.user.username+'\'s home page','user':request.user.username, 'active_home':'active'})
    else:
        return HttpResponseRedirect('/index/')


def Manage(request):
    if request.user.is_authenticated():
        userinfoList = userinfo.objects.filter(belongs_id = request.user.id)
        return render(request, 'manage.html',{'user':request.user.username, 'active_manage':'active', 'userinfoList':userinfoList})
    else:
        return HttpResponseRedirect('/login/')



def Grade(request):

    if request.user.is_authenticated():
        userinfoList = userinfo.objects.filter(belongs_id = request.user.id)
        return render(request, 'grade.html',{'user':request.user.username, 'active_manage':'active', 'userinfoList':userinfoList})
    else:
        return HttpResponseRedirect('/login/')
#TODO : NO function to this

def Userinfo(request, userinfoID):
    #TODO: select what user wants, check the grades here
    if request.user.is_authenticated():
        userinfoList = userinfo.objects.filter(id = userinfoID)
        gradeList = grades.objects.filter(belongs_id = userinfoID)
        return render(request, 'userinfo.html',{'user':request.user.username, 'active_manage':'active', 'userinfoList':userinfoList, 'gradeList':gradeList,'oneDay':((datetime.datetime.now() - datetime.timedelta(days = 1))).strftime("%Y-%m-%d %H:%M:%S")})
    else:
        return HttpResponseRedirect('/login/')

def userInfoAddGrade_Ajax(request, userinfoID = 0):
    if request.user.is_authenticated():
        user = userinfo.objects.filter(id = userinfoID)[0]
        if user.verify == True:
            _ = uestc()
            loginer = _.login(request.user.id, user.username, user.password, user.cookies)
            if loginer:
                li = _.get_list_course()
                _.update_db(request.user.id, li)
                result= {'status':'1','message':'sync done'}
            else:
                result= {'status':'0','message':'error'}
        else:
            result= {'status':'0','message':'Not Verify Account'}
    else:
        result= {'status':'0','message':'You are not login'}
    result = json.dumps(result)
    return HttpResponse(result)


def Add(request):   #add an account for manage
    if not request.user.is_authenticated(): # user is login
        return HttpResponseRedirect('/login/')
    ####EDITING
    username   = ''
    password   = ''
    email      = ''
    cookies     = ''
    message = None
    if request.POST:
        form = CaptchaTestForm(request.POST)
        if form.is_valid():
            human = True
            if ('username' in request.POST and 'password' in request.POST  and 'cookies' in request.POST and 'school' in request.POST):
                belongs_id = request.user.id
                username   = request.POST.get('username','')
                password   = request.POST.get('password','')
                cookies     = request.POST.get('cookies','')
                email      = request.POST.get('email','')
                school     = request.POST.get('school','')
                if(not userinfo.objects.filter(belongs_id = belongs_id, username = username, school = school)):### verify repeat
                    try:#userinfo add
                        adder = userinfo.objects.create(belongs_id=belongs_id , username=username, password=password, cookies=cookies, email=email, school = school, verify = False)
                        return HttpResponseRedirect('/manage/')
                    except:# error?
                        message = 'This user cannot add.'
                else:#had added
                    message = 'You had added this account.'
            else:#no username,password value
                message = 'What are you doing?'
        else:
            message = 'code was wrong'
    else:# GET
        form = CaptchaTestForm()
    return render(request, 'add.html',{'captcha':form,'message':message, 'username':username, 'password':password, 'cookies': cookies, 'email':email, 'active_add':'active'})

def userInfoverifyOne(belongs_id, username, password, school):
    users = userinfo.objects.filter(belongs_id = belongs_id, username = username, school = school, verify = False)
    for user in users:
        if (school == 'uestc'):
            try:
                _ = uestc()
                status = _.login(belongs_id, username, password, cookie)
            except Exception as e:
                status = e
            if status:
                user = userinfo.objects.filter(username = username, password = password, school = school).update(verify = True)
                return True
            else:
                return status
        ### elif other school
        else:
            return 'No this school'

def userInfoVerifyFull_Ajax(request):
    # there should return an alert to user: reload
    if request.user.is_authenticated():
        message = userInfoverifyFull(request.user.id)
        result= {'status':'1','message':str(message)}
    else:
        result= {'status':'0','message':'You are not login'}
    result = json.dumps(result)
    return HttpResponse(result)


def userInfoverifyFull(belongs_id = 0):
    #this is verify by login_user,not decided by post
    users = userinfo.objects.filter(belongs_id = belongs_id)
    result = []
    for user in users:
        # print (user)
        if user.verify:
            result.append(True)
        else:
            # print ('verify:'+user.username)
            result.append(userInfoverifyOne(belongs_id, user.username, user.password, user.school))
    return result



def userInfoChange(request, userinfoID):
    if not request.user.is_authenticated(): # user is login
        return HttpResponseRedirect('/login/')
    ####EDITING
    message = None
    users = userinfo.objects.filter(id = userinfoID)[0]

    try:
        if (request.user.id == users.belongs_id):
            username = users.username
            password = users.password
            email = users.email
            school = users.school
        else:
            # NO permission
            result= {'status':'-1', 'message':'No permission' }
            result = json.dumps(result)
            return HttpResponse(result)
    except Exception as e:
        result= {'status':'-1', 'message':'something was wrong' }
        result = json.dumps(result)
        return HttpResponse(result)



    if request.POST:
        form = CaptchaTestForm(request.POST)
        if form.is_valid():
            human = True
            if ('username' in request.POST and 'password' in request.POST  and 'school' in request.POST):
                username   = request.POST.get('username','')
                password   = request.POST.get('password','')
                email      = request.POST.get('email','')
                school     = request.POST.get('school','')
                try:#userinfo change
                    users.username = username
                    users.password = password
                    users.email = email
                    users.school = school
                    users.save()
                    return HttpResponseRedirect('/manage/')
                except:# error?
                    message = 'This user cannot change.'
            else:#no username,password value
                message = 'What are you doing?'
        else:
            message = 'code was wrong'
    else:# GET
        form = CaptchaTestForm()
    return render(request, 'change.html',{'username':username, 'password':password, 'email':email, 'school':school, 'captcha':form,'message':message, 'active_add':'active'})


def userInfoDelete(request, userinfoID):
    if not request.user.is_authenticated(): # user is login
        return HttpResponseRedirect('/login/')
    else:
        userinfo.objects.filter(id = userinfoID).delete()
        result= {'status':'0', 'message':'delete ' + userinfoID}
        result = json.dumps(result)
        return HttpResponse(result)
