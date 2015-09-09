from django.shortcuts import render_to_response
from blog.models import Employee
class Person(object):
    def __init__(self,name,age):
        self.name = name
        self.age = age
    def say(self):
        return self.name


def index(req):
    # user = {'name':'lc4t','age':'21'}
    # user = Person('lc4t','20')
    # book_list = ['python','java','c','php']
    # return render_to_response('index.html',{'title':'blog','user':user,'book_list':book_list})
    emps = Employee.objects.all()
    return render_to_response('index.html',{'emps',emps})