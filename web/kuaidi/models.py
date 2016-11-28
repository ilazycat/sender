from django.db import models
from django.contrib import admin
from django.contrib import auth
import datetime


class kuaidiInfo(models.Model):
#the grade, one column match one grade :), username is for website
#Please sort by username > school > academisc > semester

    belongs_id      = models.IntegerField() # --> userinfo
    num             = models.CharField(max_length = 255, null=False)
    company         = models.CharField(max_length=255,null=False)
    comment         = models.CharField(max_length=255,null=True)
    updateTime      = models.CharField(max_length = 255, null=True)
    time            = models.CharField(max_length = 255,null=True)    ###
    context         = models.TextField(null=True)  ###
    submit          = models.DateField(auto_now=True)

#TODO: add time
    def __str__(self):
        return "%d, %s, %s, %s, %s, %s" % (self.belongs_id, self.num, self.company, self.updateTime, self.time, self.context)

    class Admin:
        list_display = ("belongs_id", "num ", "company", "updateTime", "time", "context")

    class Meta:
        ordering = ["belongs_id"]
