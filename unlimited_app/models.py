from django.db import models
# from django.contrib.auth.models import User
from datetime import date
from django.conf import settings
import os

User = settings.AUTH_USER_MODEL

class MainCategory(models.Model):
	image = models.ImageField(null = True, blank = True,upload_to= "images/")
	name = models.CharField(max_length= 100)
	description = models.TextField(blank = True, null = True)
	created_at = models.DateTimeField(auto_now=True)
	updated_at = models.DateTimeField(auto_now= True)

	def image_url(self):
		return os.path.join('',settings.MEDIA_URL+'images/', os.path.basename(str(self.image)))

	def __str__(self):
		return self.name

class SubCategory(models.Model):
	name = models.CharField(max_length= 100)
	image = models.ImageField(null = True, blank = True,upload_to= "images/")
	description = models.TextField(blank = True, null = True)
	created_at = models.DateTimeField(auto_now=True)
	updated_at = models.DateTimeField(auto_now= True)

	def image_url(self):
		return os.path.join('',settings.MEDIA_URL+'images/', os.path.basename(str(self.image)))
	

	def __str__(self):
		return self.name

class FileType(models.Model):
	name = models.CharField(max_length= 100)
	description = models.TextField(blank = True, null = True)
	created_at = models.DateTimeField(auto_now=True)
	updated_at = models.DateTimeField(auto_now= True)

	def __str__(self):
		return self.name

class Tag(models.Model):
	name = models.CharField(max_length= 200, blank= False, null = False)
	created_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.name

class ImageStore(models.Model):
	# image_category_type = models.ForeignKey(MainCategory, on_delete=models.CASCADE)
	sub_category_type = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
	image = models.ImageField(null=True, blank=True, upload_to="images/")
	image_title = models.CharField(blank=True, null=True, max_length=1000)
	image_description = models.TextField()
	image_tag = models.ManyToManyField(Tag)
	image_upload_date = models.DateField(default=date.today)
	file_type = models.ForeignKey(FileType, on_delete= models.CASCADE)
	user = models.ForeignKey(User,on_delete= models.CASCADE)
	verified = models.BooleanField(default = False)
	isActive = models.BooleanField(default = True)
	isPremium = models.BooleanField(default = False)
	download_count = models.IntegerField(default=0)

	def image_url(self):
		return os.path.join('',settings.MEDIA_URL+'images/', os.path.basename(str(self.image)))

	def __str__(self):
		return self.image_title

class ImageFile(models.Model):

	image = models.ForeignKey(ImageStore, on_delete=models.CASCADE)
	file = models.FileField(upload_to = 'image_file/',null=True)

	def __str__(self):
		return "%s"%(self.image.image_title)

class MyFavorite(models.Model):
	user = models.OneToOneField(User,on_delete= models.CASCADE)
	images = models.ManyToManyField(ImageStore)

class MyDownload(models.Model):
	user = models.OneToOneField(User,on_delete= models.CASCADE)
	images = models.ManyToManyField(ImageStore)

class UserUploadHistory(models.Model):
	user = models.ForeignKey(User,on_delete= models.CASCADE)
	image = models.ForeignKey(ImageStore,null = True,blank = True, on_delete=models.CASCADE)
	status = models.CharField(blank=True, null=True, max_length=100)
	created_at = models.DateTimeField(auto_now=True)