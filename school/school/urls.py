"""school URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""

from django.conf.urls import include, url
from django.contrib import admin
from grade.views import current_datetime, hours_ahead, Index, Login, Logout, Home, Register, Manage, Add
import school.settings

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    # url(r'^accounts/login/$',  Login),
    # url(r'^accounts/logout/$', logout),
    url(r'^time/$',current_datetime),
    url(r'^index/$',Index),
    url(r'^register/$',Register),
    url(r'^login/$',Login),
    url(r'^logout/$',Logout),
    url(r'^home/$', Home),
    url(r'^time/plus/(\d{1,2})/$',hours_ahead),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^manage/$', Manage),
    url(r'^add/$', Add),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root':school.settings.STATIC_URL}),
]
