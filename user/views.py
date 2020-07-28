#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  6 14:04:16 2019

@author: sambhav
"""
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from user.serializers import UserRegistrationSerializer, UserLoginSerializer
from rest_framework.generics import RetrieveAPIView
from django.http import HttpResponse, JsonResponse
from rest_framework.views import APIView
from .models import User
from profile.models import UserProfile


class UserRegistrationView(CreateAPIView):

    serializer_class = UserRegistrationSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        status_code = status.HTTP_201_CREATED
        response = {
            'success' : 'True',
            'status code' : status_code,
            'message': 'User registered  successfully',
            }
        
        return Response(response, status=status_code)

class UserLoginView(RetrieveAPIView):

    permission_classes = (AllowAny,)
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = {
            'success' : 'True',
            'status code' : status.HTTP_200_OK,
            'message': 'User logged in  successfully',
            'token' : serializer.data['token'],
            }
        status_code = status.HTTP_200_OK

        return Response(response, status=status_code)

class UserView(APIView):

    permission_classes = (IsAuthenticated,)
    # serializer_class = UserLoginSerializer
    
    def get(self,request):
        user = request.user
        if user.is_superuser:
            users = User.objects.filter(is_active = True)
            result = []
            for user in users:
                profile_data = {}
                profile_data["id"] = user.id
                profile_data["email"] = user.email
                try:
                    profile = UserProfile.objects.get(user = user)
                    profile_data["first_name"] = profile.first_name
                    profile_data["last_name"] = profile.last_name
                    profile_data["phone_number"] = profile.phone_number
                    profile_data["age"] = profile.age
                    profile_data["gender"] = profile.gender
                except:
                    profile_data["first_name"] = ""
                    profile_data["last_name"] = ""
                    profile_data["phone_number"] = ""
                    profile_data["age"] = ""
                    profile_data["gender"] = ""
                result.append(profile_data)
            return JsonResponse(result,safe = False,status=status.HTTP_200_OK)

        else:
            return JsonResponse([{"status":"Not authorized"}], safe = False)


                

