import uuid
from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse
from rest_framework.views import APIView
from rest_framework import status
from .models import *
from unlimited_project.settings import ROOT_URL,STATIC_URL

# from unlimited_app.models import Type_of_Image,\
# 									Image_store,\
# 									AI_and_Txt,\
# 									Sub_Category_Image
import zipfile

def generating_id():
	image_unique_id = str(uuid.uuid4().fields[-1])[:6]
	return image_unique_id

class MainCategoryAPI(APIView):
	def get(self,request):
		all_categories = [x for x in MainCategory.objects.all()]
		response = []

		for each_category in all_categories:
			response.append({"name":each_category.name,
							"image": ROOT_URL+each_category.image.url[1:],
							"description":each_category.description,
							"created_at":each_category.created_at,
							"updated_at":each_category.updated_at
			})
		return JsonResponse(response,safe = False,status=status.HTTP_200_OK)

class SubCategoryAPI(APIView):
	def get(self,request):
		all_sub_categories = [x for x in SubCategory.objects.all()]
		response = []

		for each_category in all_sub_categories:
			response.append({"name":each_category.name,
							"image": ROOT_URL+ each_category.image.url[1:],
							"description":each_category.description,
							"created_at":each_category.created_at,
							"updated_at":each_category.updated_at
			})
		return JsonResponse(response,safe = False,status=status.HTTP_200_OK)

class FileTypeAPI(APIView):
	def get(self, request):
		all_types = [x for x in FileType.objects.all()]

		response = []

		for each_type in all_types:
			response.append({"name":each_type.name,
							"description": each_type.description,
							"created_at": each_type.created_at
			})
		
		return JsonResponse(response,safe = False,status=status.HTTP_200_OK)

class TagAPI(APIView):
	def get(self,request):
		tag = request.GET.get('tag', None)
		print(tag)
		if tag is not None:
			all_tags = [x.name for x in Tag.objects.filter(name__icontains = tag)]
			
			return JsonResponse(all_tags,safe = False,status=status.HTTP_200_OK)
		else:
			return JsonResponse({"error":"empty parameter passed"},safe = False)


class ImageUploadAPI(APIView):
	def post(self, request, format="json"):
		user = User.objects.get(id = 1)#request.user
		filetype = request.data.get('image_type', None)
		sub_category_type = request.data.get('sub_category_type', None)
		list_of_images = request.FILES.get('list_of_images')
		ai_file = request.FILES.get('ai_file')
		txt_file = request.FILES.get('txt_file')
		image_title = request.data.get('image_title',None)
		image_description = request.data.get('image_description','')
		image_tags = request.data.get('image_tags','')

		if image_title == None:
			return JsonResponse({"error":"type image title"},safe = False)

		# image_type_obj,created = Type_of_Image.objects.get_or_create(image_category_type=image_type)
		# sub_category_type_obj,created = Sub_Category_Image.objects.get_or_create(sub_category_type=sub_category_type)
		try:
			file_type = FileType.objects.get(name = filetype)
		except:
			return JsonResponse({"error":"file type not available"},safe = False)
		
		try:
			sub_category = SubCategory.objects.get(name = sub_category_type)
		except:
			return JsonResponse({"error":"sub category not available"},safe = False)
		
		tags = image_tags.split(',')
		tags_list = []
		for tag in tags:
			x,y = Tag.objects.get_or_create(name = tag)
			tags_list.append(x)
		
		image_obj = ImageStore.objects.create(sub_category_type = sub_category,
															image = list_of_images,
															image_title = image_title,
															image_description = image_description,
															file_type = file_type,
															user = user
												)
		image_obj.image_tag.add(*tags_list)
		image_obj.save()
		AIandTxt.objects.create(image=image_obj,ai_file=ai_file,txt_file=txt_file)

		return Response(status=status.HTTP_200_OK)

	def get(self, request, format="json"):
		image_tag = request.data.get('tag',None)
		image_type = request.data.get('type',None)
		if image_tag != None:
			tags = image_tag.split(',')
			tags = Tag.objects.filter(name__in = tags)
			if image_tag == None:
				images = ImageStore.objects.filter(image_tag__in = tags)
			else:
				try:
					image_type = FileType.objects.get(name = image_type)
				except:
					return JsonResponse({"error":"invalid file type"},safe = False)

				images = ImageStore.objects.filter(image_tag__in = tags,file_type = image_type)
			
			response = []
			for image in images:
				tags = []
				for x in image.image_tag.all():
					tags.append(x.name)
				data = {
					"sub_category_type":str(image.sub_category_type),
					"image":ROOT_URL+image.image.url[1:],
					"image_title":image.image_title,
					"image_description":image.image_description,
					"image_tag":tags,
					"image_upload_date":image.image_upload_date,
					"file_type":str(image.file_type)
				}
				response.append(data)
			return JsonResponse(response,safe = False,status=status.HTTP_200_OK)

		else:
			return JsonResponse({"error":"no tag"},safe = False)

# class GetImage(APIView):



		

# def category_name(request):
# 	category_names_list = []
# 	image_cat_obj = Type_of_Image.objects.all()
# 	for name in image_cat_obj:
# 		category_names_list.append(name.image_category_type)
# 	return HttpResponse(category_names_list)

# def sub_category_name(request):
# 	sub_category_names_list = []
# 	image_cat_obj = Sub_Category_Image.objects.all()
# 	for name in image_cat_obj:
# 		sub_category_names_list.append(name.sub_category_type)
# 	return HttpResponse(sub_category_names_list)
