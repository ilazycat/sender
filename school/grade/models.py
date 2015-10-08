from django.db import models
from django.contrib import admin
class users(models.Model):
    username = models.CharField(max_length = 18)
    password = models.CharField(max_length = 30)

    def __str__(self):
        return "%s, %s" % (self.username, self.password)
    class Admin:
        list_display = ("username", "password")

class grades(models.Model):
    username    = models.CharField(max_length = 18)
    academisc   = models.CharField(max_length = 9)
    semester    = models.IntegerField()
    courseCode  = models.CharField(max_length = 18)
    number      = models.CharField(max_length = 18)
    courseName  = models.TextField(max_length = 100)
    courseType  = models.TextField(max_length = 100)
    credit      = models.IntegerField()
    totalGrade  = models.TextField(max_length = 10)
    makeupGrade = models.TextField(max_length = 10)
    finalGrade  = models.TextField(max_length = 10)
    gradePoint  = models.CharField(max_length = 10)

    def __str__(self):
        return "%s, %s, %d, %s, %s, %s, %s, %d, %s, %s, %s, %s" % (self.username, self.academisc, self.semester, self.courseCode, self.number, self.courseType, self.credit, self.totalGrade, self.makeupGrade, self.finalGrade, self.gradePoint)

    class Admin:
        list_display = ("username", "academisc", "semester", "courseCode", "number", "courseType", "credit", "totalGrade", "makeupGrade", "finalGrade", "gradePoint")
