import uuid
from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework import status
from unlimited_app.models import Type_of_Image,\
									Image_store,\
									AI_and_Txt,\
									Sub_Category_Image
import zipfile

def generating_id():
	image_unique_id = str(uuid.uuid4().fields[-1])[:6]
	return image_unique_id

class image_upload(APIView):
	def post(self, request, format="json"):
		user = request.user
		image_type = request.data.get('image_type', '')
		sub_category_type = request.data.get('sub_category_type', '')
		list_of_images = request.FILES.get('list_of_images')
		ai_file = request.FILES.get('ai_file')
		txt_file = request.FILES.get('txt_file')
		image_title = request.data.get('image_title','')
		image_description = request.data.get('image_description','')

		image_type_obj,created = Type_of_Image.objects.get_or_create(image_category_type=image_type)
		sub_category_type_obj,created = Sub_Category_Image.objects.get_or_create(sub_category_type=sub_category_type)

		image_obj = Image_store.objects.create(image_category_type=image_type_obj,
												sub_category_type=sub_category_type_obj,
												image_id=generating_id(),
												image=list_of_images,
												image_title=image_title,
												image_description=image_description,
												)
		AI_and_Txt.objects.create(image=image_obj,ai_file=ai_file,txt_file=txt_file)

		return Response(status=status.HTTP_200_OK)

def category_name(request):
	category_names_list = []
	image_cat_obj = Type_of_Image.objects.all()
	for name in image_cat_obj:
		category_names_list.append(name.image_category_type)
	return HttpResponse(category_names_list)

def sub_category_name(request):
	sub_category_names_list = []
	image_cat_obj = Sub_Category_Image.objects.all()
	for name in image_cat_obj:
		sub_category_names_list.append(name.sub_category_type)
	return HttpResponse(sub_category_names_list)
