# -*- coding: utf-8 -*-
"""
Created on Sun Jul 28 12:15:15 2019

@author: surese.kumaar.ma
"""

from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('search',views.search,name='search'),
    
]