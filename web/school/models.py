from django.db import models
from django.contrib import admin
from django.contrib import auth
import datetime

class userinfo(models.Model):
#the school protal infomation,for login the school website

    belongs_id      = models.IntegerField() #
    username        = models.CharField(max_length = 25) # belong to web_username
    name            = models.TextField(null = True)
    password        = models.CharField(max_length = 25, null=True)
    cookies         = models.CharField(max_length = 255, null=True)
    email           = models.CharField(max_length = 255, null=True) #models.EmailField()
    school          = models.TextField()
    verify          = models.BooleanField() # is verify success
    updateTime      = models.TimeField(auto_now = True)
    def __str__(self):
        return "%s, %s, %s, %s, %s, %s, %s, %s" % (self.belongs_id, self.username, self.password, self.name, self.email, self.school, self.verify, self.updateTime)
    class Admin:
        list_display = ("belongs_id","name","username", "password", "email", "school", "verify", "updateTime")
        # pass
    class Meta:
        ordering = ["belongs_id"]


class information(models.Model):
#The schoo:url information

    school          = models.TextField()
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

    belongs_id      = models.IntegerField() # --> userinfo
    academisc       = models.CharField(max_length = 255, null=True)
    semester        = models.CharField(max_length=255,null=True)
    courseCode      = models.CharField(max_length = 255, null=True)
    number          = models.CharField(max_length = 255,null=False)    ###
    courseName      = models.TextField(null=False)  ###
    courseType      = models.TextField(null=True)
    credit          = models.CharField(max_length=255,null=True)
    totalGrade      = models.TextField(null=True)
    makeupGrade     = models.TextField(null=True)
    finalGrade      = models.TextField(null=True)
    gradePoint      = models.CharField(max_length = 255, null=True)
    updateTime      = models.CharField(max_length = 19, null=False)
#TODO: add time
    def __str__(self):
        return "%d, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s" % (self.belongs_id, self.academisc, self.semester, self.courseCode, self.number, self.courseName, self.courseType, self.credit, self.totalGrade, self.makeupGrade, self.finalGrade, self.gradePoint, self.updateTime)

    class Admin:
        list_display = ("belongs_id", "academisc", "semester", "courseCode", "number", "courseType", "credit", "totalGrade", "makeupGrade", "finalGrade", "gradePoint", "updateTime")

    class Meta:
        ordering = ["belongs_id"]
