from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class SocialLogin(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
	google_client_id = models.CharField(max_length=250,null=True)
	facebook_client_id = models.CharField(max_length=250,null=True)
	google_refresh_token = models.TextField(blank=True,null=True)
	facebook_refresh_token = models.TextField(blank=True,null=True)
	google_access_token = models.TextField(blank=True,null=True)
	facebook_access_token = models.TextField(blank=True,null=True)
	google_id_token = models.TextField(blank=True,null=True)
	access_token_expiry = models.DateTimeField(blank=True,null=True)

	def __str__(self):
		return str(self.user)