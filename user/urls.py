#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  6 14:04:16 2019

@author: sambhav
"""
from django.conf.urls import url
from user.views import UserRegistrationView, UserLoginView, UserView


urlpatterns = [
    url(r'^signup', UserRegistrationView.as_view()),
    url(r'^signin', UserLoginView.as_view()),
    url(r'^users', UserView.as_view()),
    ]