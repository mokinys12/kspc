from django.urls import path
from . import views

urlpatterns = [
    path('selfld', views.vsel_fld, name="nsel_fld"),
    path('findrow', views.vfnd_row, name="nfnd_row"),
    path('', views.vindex, name="nindex"),
    path('newclient/', views.vnew_clnt, name="nnew_clnt"),
    # newclient/ подразумевает, что после него будет следующая страница (clntsave/) с параметрами
    path('newclient/clntsave/', views.vsave_clnt, name="nsave_clnt"),
    path('isdel', views.visdel, name="nisdel"),
    path('delclnt', views.vdelclnt, name="ndelclnt"),
    path('dict', views.vdict, name="ndict"),
    path('newdict', views.vnew_dict, name="nnew_dict"),
    # тут dictsave будет сразу после корня (spcapp/)
    path('dictsave', views.vsave_dict, name="nsave_dict"),
    path('deldict', views.vdeldict, name="ndeldict"),
    path('acnt/', views.vaccount, name="naccount"),
    path('monthes/', views.vmonth, name="nmonth"),
]

