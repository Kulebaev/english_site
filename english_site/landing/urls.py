from django.urls import path
from django.conf.urls import handler404
from . import views

handler404 = 'landing.views.handler404'

urlpatterns = [
    path('', views.index_view, name='index'),
]