from django.contrib import admin
from unlimited_app.models import *




class Type_of_ImageAdmin(admin.ModelAdmin):
	list_display = ('image_category_type',)
	search_fields = ('image_category_type',)

admin.site.register(Type_of_Image,Type_of_ImageAdmin)


class Sub_Category_ImageAdmin(admin.ModelAdmin):
	list_display = ('sub_category_type',)
	search_fields = ('sub_category_type',)

admin.site.register(Sub_Category_Image,Sub_Category_ImageAdmin)

class Image_storeAdmin(admin.ModelAdmin):
	list_display = ('image_id','image_category_type','sub_category_type','image_title','image_upload_date')
	search_fields = ('image_title','image_id')

admin.site.register(Image_store,Image_storeAdmin)

class AI_and_TxtAdmin(admin.ModelAdmin):
	list_display = ('image',)
	search_fields = ('image',)

admin.site.register(AI_and_Txt,AI_and_TxtAdmin)










