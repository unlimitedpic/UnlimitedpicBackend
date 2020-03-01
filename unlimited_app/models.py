from django.db import models
from django.contrib.auth.models import User
from datetime import date
from django.conf import settings
import os

# class Type_of_Image(models.Model):

# 	image_category_type = models.CharField(blank=True, null=True, max_length=100)

# 	class Meta:
# 		unique_together = ('image_category_type',)

# 	def __str__(self):
# 		return "%s"%(self.image_category_type)

# class Sub_Category_Image(models.Model):

# 	sub_category_type = models.CharField(blank=True, null=True, max_length=100)

# 	class Meta:
# 		unique_together = ('sub_category_type',)

# 	def __str__(self):
# 		return "%s"%(self.sub_category_type)

# class Image_store(models.Model):
# 	image_category_type = models.ForeignKey(Type_of_Image, on_delete=models.CASCADE)
# 	sub_category_type = models.ForeignKey(Sub_Category_Image, on_delete=models.CASCADE)
# 	image_id = models.IntegerField(blank=True)
# 	image = models.ImageField(null=True, blank=True, upload_to="Unlimited_images/images/")
# 	image_title = models.CharField(blank=True, null=True, max_length=1000)
# 	image_description = models.TextField()
# 	image_upload_date = models.DateField(default=date.today)

# 	class Meta:
# 		unique_together = ('image_id',)

# 	def __str__(self):
# 		return "%s"%(self.image_title)




#Amar models
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

	def image_url(self):
		return os.path.join('',settings.MEDIA_URL+'images/', os.path.basename(str(self.image)))

	def __str__(self):
		return self.image_title

class ImageFile(models.Model):

	image = models.ForeignKey(ImageStore, on_delete=models.CASCADE)
	file = models.FileField(upload_to = 'image_file/',null=True)

	def __str__(self):
		return "%s"%(self.image.image_title)