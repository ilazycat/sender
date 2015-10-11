from django.db import models
from django.contrib import admin
from django.contrib import auth


class userinfo(models.Model):
#the school protal infomation,for login the school website

    web_username    = models.CharField(max_length = 18) #
    username        = models.CharField(max_length = 18) # belong to web_username
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
    url             = models.CharField(max_length = 255, null=True)

    def __str__(self):
        return "%s, %s" % (self.school,self.url)

    class Admin:
        list_display = ("school", "url")

    class Meta:
        ordering = ["school"]


class grades(models.Model):
#the grade, one column match one grade :), username is for website
#Please sort by username > school > academisc > semester

    web_username    = models.CharField(max_length = 18) # website_username
    username        = models.CharField(max_length = 18)
    password        = models.CharField(max_length = 18, null=True) # verify
    academisc       = models.CharField(max_length = 9, null=True)
    semester        = models.IntegerField(null=True)
    courseCode      = models.CharField(max_length = 18, null=True)
    number          = models.CharField(max_length = 18, null=True)
    courseName      = models.TextField(max_length = 100, null=True)
    courseType      = models.TextField(max_length = 100, null=True)
    credit          = models.IntegerField(null=True)
    totalGrade      = models.TextField(max_length = 10, null=True)
    makeupGrade     = models.TextField(max_length = 10, null=True)
    finalGrade      = models.TextField(max_length = 10, null=True)
    gradePoint      = models.CharField(max_length = 10, null=True)

    def __str__(self):
        return "%s, %s, %d, %s, %s, %s, %s, %d, %s, %s, %s, %s" % (self.username, self.academisc, self.semester, self.courseCode, self.number, self.courseType, self.credit, self.totalGrade, self.makeupGrade, self.finalGrade, self.gradePoint)

    class Admin:
        list_display = ("username", "academisc", "semester", "courseCode", "number", "courseType", "credit", "totalGrade", "makeupGrade", "finalGrade", "gradePoint")

    class Meta:
        ordering = ["username"]



