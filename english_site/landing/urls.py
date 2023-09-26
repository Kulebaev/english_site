from django.urls import path
from django.conf.urls import handler404
from . import views

handler404 = 'landing.views.handler404'

urlpatterns = [
    path('', views.index_view, name='index'),
    path('subscribe/', views.subscribe_view, name='subscribe'),
    path('message_text/', views.message_text, name='message_text'),
]