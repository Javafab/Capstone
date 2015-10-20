"""timeclock URL Configuration

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
from django.conf.urls import include, url, patterns
from django.contrib import admin
from django.contrib.auth import views as auth_views

from timestamp import views as timestamp_views


urlpatterns = [
    url('^', include('django.contrib.auth.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/login/$', auth_views.login, name='login'),
    url(r'^logged_out/$', auth_views.logout, name='logout'),
    url(r'^timestamp/', include([
        url(r'^user_profile/(?P<user_id>\d+)/$', timestamp_views.user_profile, name='user_profile'),
        url(r'^create/$', timestamp_views.create_user, name='create_user'),
        url(r'^record_time/$', timestamp_views.record_time, name='record_time'),
    ])),

]

from django.conf import settings

if settings.DEBUG:
    urlpatterns += patterns('',
                            url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
                               'document_root': settings.MEDIA_ROOT,
                           }),
                           url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
                               'document_root': settings.STATIC_ROOT,
                           }),
                            )