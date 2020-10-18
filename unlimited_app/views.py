import uuid
from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework import status
from .models import *

import os
import zipfile
from io import StringIO, BytesIO


from unlimited_project.settings import ROOT_URL,STATIC_URL

import zipfile

def generating_id():
	image_unique_id = str(uuid.uuid4().fields[-1])[:6]
	return image_unique_id

def add_user_item_history(user,item, status):
	history = UserUploadHistory.objects.create(user = user, image = item, status = status)
	return history

class MainCategoryAPI(APIView):
	permission_classes = (AllowAny,)
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
	permission_classes = (AllowAny,)
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
	permission_classes = (AllowAny,)
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
	permission_classes = (AllowAny,)
	def get(self,request):
		tag = request.GET.get('tag', None)
		print(tag)
		if tag is not None:
			all_tags = [x.name for x in Tag.objects.filter(name__icontains = tag)]
			
			return JsonResponse(all_tags,safe = False,status=status.HTTP_200_OK)
		else:
			return JsonResponse({"error":"empty parameter passed"},safe = False)


class ImageAPI(APIView):
	permission_classes = (AllowAny,)
	def post(self, request, format="json"):
		user = request.user
		filetype = request.data.get('image_type', None)
		sub_category_type = request.data.get('sub_category_type', None)
		image = request.FILES.get('image')
		image_files = request.FILES.getlist('image_files')
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
															image = image,
															image_title = image_title,
															image_description = image_description,
															file_type = file_type,
															user = user
												)
		image_obj.image_tag.add(*tags_list)
		image_obj.save()
		for image_file in image_files:
			ImageFile.objects.create(image=image_obj,file = image_file)
		history = add_user_item_history(user,image_obj,"Image created")
		return Response(status=status.HTTP_200_OK)

	def get(self, request, format="json"):
		image_tag = request.GET.get('tag',None)
		image_type = request.GET.get('type',None)
		sort = request.GET.get('sort','new')


		if sort == "new":
			sort_by = "-image_upload_date"
		elif sort == "old":
			sort_by = "image_upload_date"

		if image_tag != None:
			tags = image_tag.split(',')
			tags = Tag.objects.filter(name__in = tags)
			if len(tags) != 0 and image_type:
				try:
					image_type = FileType.objects.get(name = image_type)
					images = ImageStore.objects.filter(image_tag__in = tags,file_type = image_type,verified = True).order_by(sort_by)
				except:
					return JsonResponse([{"error":"invalid file type"}],safe = False)
			elif len(tags) != 0:
				images = ImageStore.objects.filter(image_tag__in = tags,verified = True).order_by(sort_by)
			
			# else:
			# 	try:
			# 		if image_type:
			# 			image_type = FileType.objects.get(name = image_type)
			# 			images = ImageStore.objects.filter(image_tag__in = tags,file_type = image_type).order_by(sort_by)
			# 		else:
			# 			return JsonResponse([{"error":"No data found"}], safe =False)
			# 	except:
			# 		return JsonResponse([{"error":"invalid file type"}],safe = False)

				# images = ImageStore.objects.filter(image_tag__in = tags,file_type = image_type).order_by(sort_by)
			
			response = []
			for image in images:
				tags = []
				for x in image.image_tag.all():
					tags.append(x.name)
				data = {
					"id": image.id,
					"sub_category_type":str(image.sub_category_type),
					"image":ROOT_URL+image.image.url[1:],
					"image_title":image.image_title,
					"image_description":image.image_description,
					"image_tag":tags,
					"image_upload_date":image.image_upload_date,
					"file_type":str(image.file_type),
					"isPremium":image.isPremium,
					"download_count":image.download_count
				}
				response.append(data)
			return JsonResponse(response,safe = False,status=status.HTTP_200_OK)

		else:
			return JsonResponse([{"error":"no tag"}],safe = False)


	def delete(self, request):
		image_id = request.data.get('image_id', None)
		user = request.user
		try:
			image = ImageStore.objects.get(id = image_id)
			if user.is_superuser or user == image.user:
				image.objects.delete()

				history = add_user_item_history(user,None,"Image deleted")

				return JsonResponse([{"status":"record deleted successfully"}], safe = False)
			else:
				return JsonResponse([{"status":"Not authorized"}], safe = False)

		except:
			return JsonResponse([{"error":"invalid id"}], safe = False)

class MyDownloadAPI(APIView):
	permission_classes = (IsAuthenticated,)
	def get(self, request, format="json"):
		
		user = request.user

		
		data, created = MyDownload.objects.get_or_create(user = user)
		images = []
		for image in data.images.all():
			images.append(image)
			
		response = []
		for image in images:
			tags = []
			for x in image.image_tag.all():
				tags.append(x.name)
			data = {
				"id": image.id,
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


class ImageDeactivateAPI(APIView):
	permission_classes = (IsAuthenticated,)
	def put(self, request):
		image_id = request.data.get('image_id', None)
		user = request.user
		try:
			image = ImageStore.objects.get(id = image_id)
			if user.is_superuser or user == image.user:
				image.isActive = False
				image.save()
				history = add_user_item_history(user,image,"Image deacivated")
				return JsonResponse([{"status":"record deactivated successfully"}], safe = False)
			else:
				return JsonResponse([{"status":"Not authorized"}], safe = False)

		except:
			return JsonResponse([{"error":"invalid id"}], safe = False)


class ImageDetailsAPI(APIView):
	permission_classes = (AllowAny,)
	def get(self,request):
		imageId = request.GET.get('imageId',None)

		images = ImageStore.objects.filter(id = imageId, isActive = True)
		if len(images) != 0:
			image = images[0]
			tags = []
			for x in image.image_tag.all():
				tags.append(x.name)
			data = {
				"id": image.id,
				"sub_category_type":str(image.sub_category_type),
				"image":ROOT_URL+image.image.url[1:],
				"image_title":image.image_title,
				"image_description":image.image_description,
				"image_tag":tags,
				"image_upload_date":image.image_upload_date,
				"file_type":str(image.file_type)
			}
			
			return JsonResponse(data,safe = False,status=status.HTTP_200_OK)

		else:
			return JsonResponse([{"error":"invalid id"}], safe = False)

class ImageDownloadAPI(APIView):
	permission_classes = (AllowAny,)
	def get(self,request):
		imageId = request.GET.get('imageId',None)
		if imageId:
			try:
				image = ImageStore.objects.get(id = int(imageId))
				image.downloadCount += 1
				image.save()
				if image.isPremium:
					count = ImageStore.objects.filter(user= request.user, verified = True).count()
					if count < 3:
						return JsonResponse({"error":"Premium Content- contibute " + str(3-count) + " content"}, safe = False)
				image_files = ImageFile.objects.filter(image=image)
				files_list = []
				files_list.append(image.image.path)
				
				for image_file in image_files:
					pass
					files_list.append(image_file.file.path)
    

				zip_subdir = image.image_title
				zip_filename = "%s.zip" % zip_subdir

				# Open StringIO to grab in-memory ZIP contents
				s = BytesIO()

				# The zip compressor
				zf = zipfile.ZipFile(s, "w")

				for fpath in files_list:
					# Calculate path for file in zip
					fdir, fname = os.path.split(fpath)
					zip_path = os.path.join(zip_subdir, fname)

					# Add file, at correct path
					zf.write(fpath, zip_path)

				# Must close zip for all contents to be written
				zf.close()

				# Grab ZIP file from in-memory, make response with correct MIME-type
				resp = HttpResponse(s.getvalue(), content_type = "application/x-zip-compressed")
				# ..and correct content-disposition
				resp['Content-Disposition'] = 'attachment; filename=%s' % zip_filename

				return resp
				# return JsonResponse(files_list,safe= False)



			except Exception as e:
				print(e)
				return JsonResponse({"error":"invalid id"}, safe = False)
		else:
			return JsonResponse({"error":"invalid id"}, safe = False)


class MyFavoriteAPI(APIView):
	permission_classes = (IsAuthenticated,)
	def post(self, request):
		user = request.user
		imageId = request.data.get('imageId',None)
		dislike = request.data.get('dislike',False)

		

		try:
			image = ImageStore.objects.get(id = imageId)
			try:
				myFavObj = MyFavorite.objects.get(user = user)
				if dislike == True:
					myFavObj.images.remove(image)
					response= {"status":"disliked"}
					return Response(response)
					

				myFavObj.images.add(image)
				response= {"status":"liked"}
				return Response(response)

			except Exception as e:
				print(e)
				try:
					myFavObj = MyFavorite.objects.create(user = user)
					myFavObj.images.add(image)
					response= {"status":"liked"}
					return Response(response)
				except:
					return JsonResponse({"error":"invalid user"}, safe = False)
		except Exception as e:
				print(e)
				return JsonResponse({"error":"invalid id"}, safe = False)
	
	def get(self, request):
		user = request.user

		try:
			MyFavObj = MyFavorite.objects.get(user = user)
			print(user,"   ",MyFavObj.images.all())
			response = []
			for image in MyFavObj.images.all():
				data = {
						"id": image.id,
						"image":ROOT_URL+image.image.url[1:],
						"image_title":image.image_title,
						"file_type":str(image.file_type)
					}
				response.append(data)
			return Response(response)

		except Exception as e:
			print(e)
			return JsonResponse({"error":"invalid id"}, safe = False)

		
class ImageVerifyAPI(APIView):
	permission_classes = (IsAuthenticated,)

	def get(self,request):
		if request.user.is_superuser:

			data = []

			images = ImageStore.objects.filter(verified = False)
			response = []
			for image in images:
				tags = []
				for x in image.image_tag.all():
					tags.append(x.name)
				data = {
					"id": image.id,
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
			return JsonResponse({"Status":"Unauthorized"},status=status.HTTP_401_UNAUTHORIZED)
	
	def put(self,request):
		image_id = request.data.get('image_id', None)
		user = request.user
		if user.is_superuser:
			try:
				image = ImageStore.objects.get(id = image_id)
				image.verified = True
				image.save()
				return JsonResponse([{"status":"image verified successfully"}], safe = False)
				

			except:
				return JsonResponse([{"error":"invalid id"}], safe = False)
		else:
			return JsonResponse([{"status":"Not authorized"}], safe = False)

class ImageUserHistoryAPI(APIView):
	permission_classes = (IsAuthenticated,)

	def get(self,request):
		if request.user.is_superuser:

			data = []

			histories = UserUploadHistory.objects.all().order_by("-created_at")
			response = []
			for history in histories:
				data = {
					"id": history.id,
					"user_id":history.user.id,
					"email":history.user.email,
					"image":ROOT_URL+history.image.image.url[1:] if history.image else None,
					"image_title":history.image.image_title if history.image else None,
					"created_at":history.created_at,
					"status":history.status
	
				}
				response.append(data)
			return JsonResponse(response,safe = False,status=status.HTTP_200_OK)
		else:
			return JsonResponse({"Status":"Unauthorized"},status=status.HTTP_401_UNAUTHORIZED)
