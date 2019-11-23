from django.db import models
from django.contrib.auth.models import User
from datetime import date


class Type_of_Image(models.Model):

	image_category_type = models.CharField(blank=True, null=True, max_length=100)

	class Meta:
		unique_together = ('image_category_type',)

	def __str__(self):
		return "%s"%(self.image_category_type)

class Sub_Category_Image(models.Model):

	sub_category_type = models.CharField(blank=True, null=True, max_length=100)

	class Meta:
		unique_together = ('sub_category_type',)

	def __str__(self):
		return "%s"%(self.sub_category_type)

class Image_store(models.Model):
	image_category_type = models.ForeignKey(Type_of_Image, on_delete=models.CASCADE)
	sub_category_type = models.ForeignKey(Sub_Category_Image, on_delete=models.CASCADE)
	image_id = models.IntegerField(blank=True)
	image = models.ImageField(null=True, blank=True, upload_to="Unlimited_images/images/")
	image_title = models.CharField(blank=True, null=True, max_length=1000)
	image_description = models.TextField()
	image_upload_date = models.DateField(default=date.today)

	class Meta:
		unique_together = ('image_id',)

	def __str__(self):
		return "%s"%(self.image_title)


class AI_and_Txt(models.Model):

	image = models.ForeignKey(Image_store, on_delete=models.CASCADE)
	ai_file = models.FileField(upload_to = 'Unlimited_images/ai_file/',null=True)
	txt_file = models.FileField(upload_to = 'Unlimited_images/txt_file/',null=True)

	def __str__(self):
		return "%s"%(self.image.image_title)