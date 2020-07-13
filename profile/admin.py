from django.contrib import admin
from profile.models import *

class UserProfileAdmin(admin.ModelAdmin):
	list_display = ('user','first_name',)
	search_fields = ('user','first_name',)

admin.site.register(UserProfile,UserProfileAdmin)