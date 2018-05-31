"""njdz URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from njdz_wechat import views as njdz_wechat_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    #url(r'^$', njdz_wechat.views.index, name='index'),

    url(r'^$', njdz_wechat_views.index),
    url(r'^index/$', njdz_wechat_views.index, name='index'),
    url(r'^examtype/$', njdz_wechat_views.selectexamtype, name='examtype'),
    #url(r'^(.{4})/$', njdz_wechat_views.selectquestiontype, name='questiontype'),
    url(r'^(thzh|zfdm|yzdd|zjtz)/$', njdz_wechat_views.selectquestiontype, name='questiontype'),
    url(r'^(thzh|zfdm|yzdd|zjtz)/(\d{1})/$', njdz_wechat_views.showrule, name='rule'),
    url(r'^(thzh|zfdm|yzdd|zjtz)/(\d{1})/exam/$', njdz_wechat_views.answerquestion, name='questioncontent'),
    #url(r'^(thzh|zfdm|yzdd|zjtz)/(\d{1})/(\d{1,3})/(\d{1,3})/$', njdz_wechat_views.inputuserinfo, name='userinfo'),
    url(r'^inputUserInfo/$', njdz_wechat_views.inputUserInfo, name='inputUserInfo'),
    url(r'^result/$', njdz_wechat_views.result, name='result'),
    url(r'^ranklist/$', njdz_wechat_views.ranklistselect, name='ranktype'),
    url(r'^ranklist/(week|month|quarter|year)/$', njdz_wechat_views.ranlistresult, name='ranlilist'),

    url(r'^download/$', njdz_wechat_views.download, name='downloadtype'),
    url(r'^(week|month)/(\d{4})/(\d{1,2})/$', njdz_wechat_views.send_excle_file, name='downloadexcel'),

    #url(r'^ruletongyong/$', njdz_wechat_views.ruletongyong, name='ruletongyong'),
    #url(r'^tihaizongheng/$', njdz_wechat_views.tihaizongheng, name='tihaizongheng'),
    #url(r'^info/$', njdz_wechat_views.info, name='info'),
    #url(r'^score/$', njdz_wechat_views.score, name='score'),


    url(r'^ajax_list/$', njdz_wechat_views.ajax_list, name='ajax_list'),
    url(r'^ajax_dict/$', njdz_wechat_views.ajax_dict, name='ajax_dict'),

    url(r'^polly/$', njdz_wechat_views.polly, name='polly'),

    url(r'^formTest/$', njdz_wechat_views.formTest, name='formTest'),
]
