from django.contrib import admin 
from django.urls import path 
from . import views 

urlpatterns = [ 
	path('', views.youtube, name='youtube'),
    # path('download/', views.download_video, name='download_video'), 
]
