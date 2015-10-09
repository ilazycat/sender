from django.db import models
from django.contrib import admin
from django.contrib import auth

class users(models.Model):
#The website user info

    username        = models.CharField(max_length = 18)
    password        = models.CharField(max_length = 30)
    email           = models.EmailField()

    def __str__(self):
        return "%s, %s, %s" % (self.username, self.password, self.email)

    class Admin:
        list_display = ("username" ,"password", "email")

    class Meta:
        ordering = ["username"]

class userinfo(models.Model):
#the school protal infomation,for login the school website

    username        = models.CharField(max_length = 18)
    name            = models.TextField(max_length = 20)
    password        = models.CharField(max_length = 30)
    email           = models.EmailField()
    school          = models.TextField(max_length = 100)
    def __str__(self):
        return "%s, %s, %s, %s, %s" % (self.username, self.password, self.name, self.email, self.school)
    class Admin:
        list_display = ("username", "password", "email", "school")
        # pass
    class Meta:
        ordering = ["username"]


class infomation(models.Model):
#The schoo:url information

    school          = models.TextField(max_length = 255)
    url             = models.CharField(max_length = 255)\

    def __str__(self):
        return "%s, %s" % (self.school,self.url)

    class Admin:
        list_display = ("school", "url")

    class Meta:
        ordering = ["school"]


class grades(models.Model):
#the grade, one column match one grade :), username is for website
#Please sort by username > school > academisc > semester

    username        = models.CharField(max_length = 18) # website_username
    academisc       = models.CharField(max_length = 9)
    semester        = models.IntegerField()
    courseCode      = models.CharField(max_length = 18)
    number          = models.CharField(max_length = 18)
    courseName      = models.TextField(max_length = 100)
    courseType      = models.TextField(max_length = 100)
    credit          = models.IntegerField()
    totalGrade      = models.TextField(max_length = 10)
    makeupGrade     = models.TextField(max_length = 10, null=True)
    finalGrade      = models.TextField(max_length = 10)
    gradePoint      = models.CharField(max_length = 10)

    def __str__(self):
        return "%s, %s, %d, %s, %s, %s, %s, %d, %s, %s, %s, %s" % (self.username, self.academisc, self.semester, self.courseCode, self.number, self.courseType, self.credit, self.totalGrade, self.makeupGrade, self.finalGrade, self.gradePoint)

    class Admin:
        list_display = ("username", "academisc", "semester", "courseCode", "number", "courseType", "credit", "totalGrade", "makeupGrade", "finalGrade", "gradePoint")

    class Meta:
        ordering = ["username"]



def login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = auth.authenticate(username=username, password=password)
    if user is not None and user.is_active:
        # Correct password, and the user is marked "active"
        auth.login(request, user)
        # Redirect to a success page.
        return HttpResponseRedirect("/account/loggedin/")
    else:
        # Show an error page
        return HttpResponseRedirect("/account/invalid/")

def logout(request):
    auth.logout(request)
    # Redirect to a success page.
    return HttpResponseRedirect("/account/loggedout/")