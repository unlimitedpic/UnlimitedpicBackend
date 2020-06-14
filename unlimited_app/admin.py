from django.contrib import admin
from unlimited_app.models import *




# class Type_of_ImageAdmin(admin.ModelAdmin):
# 	list_display = ('image_category_type',)
# 	search_fields = ('image_category_type',)

# admin.site.register(Type_of_Image,Type_of_ImageAdmin)


# class Sub_Category_ImageAdmin(admin.ModelAdmin):
# 	list_display = ('sub_category_type',)
# 	search_fields = ('sub_category_type',)

# admin.site.register(Sub_Category_Image,Sub_Category_ImageAdmin)

# class Image_storeAdmin(admin.ModelAdmin):
# 	list_display = ('image_id','image_category_type','sub_category_type','image_title','image_upload_date')
# 	search_fields = ('image_title','image_id')

# admin.site.register(Image_store,Image_storeAdmin)

# class AI_and_TxtAdmin(admin.ModelAdmin):
# 	list_display = ('image',)
# 	search_fields = ('image',)

# admin.site.register(AI_and_Txt,AI_and_TxtAdmin)


class MainCategoryAdmin(admin.ModelAdmin):
	list_display = ('name','created_at',)
	search_fields = ('name','created_at',)

class SubCategoryAdmin(admin.ModelAdmin):
	list_display = ('name','created_at',)
	search_fields = ('name','created_at',)

class FileTypeAdmin(admin.ModelAdmin):
	list_display = ('name','created_at',)
	search_fields = ('name','created_at',)

class TagAdmin(admin.ModelAdmin):
	list_display = ('name','created_at',)
	search_fields = ('name','created_at',)

class ImageStoreAdmin(admin.ModelAdmin):
	list_display = ('image_title','image_upload_date','file_type','sub_category_type',)
	search_fields = ('image_title','image_upload_date','file_type','sub_category_type',)

class ImageFileAdmin(admin.ModelAdmin):
	list_display = ('image','file',)
	search_fields = ('image','file',)

class MyFavoriteAdmin(admin.ModelAdmin):
	list_display = ('user',)
	search_fields = ('user',)

class MyDownloadAdmin(admin.ModelAdmin):
	list_display = ('user',)
	search_fields = ('user',)

admin.site.register(MainCategory,MainCategoryAdmin)
admin.site.register(SubCategory,SubCategoryAdmin)
admin.site.register(FileType,FileTypeAdmin)
admin.site.register(Tag,TagAdmin)
admin.site.register(ImageStore,ImageStoreAdmin)
admin.site.register(ImageFile, ImageFileAdmin)
admin.site.register(MyFavorite,MyFavoriteAdmin)
admin.site.register(MyDownload,MyDownloadAdmin)