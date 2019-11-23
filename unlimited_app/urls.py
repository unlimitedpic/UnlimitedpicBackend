from django.conf.urls import url
from unlimited_app.views import image_upload,\
								category_name,\
								sub_category_name


urlpatterns = [
	url(r'^images_posting/', image_upload.as_view(), name='uploading image for admin'),
	url(r'^category_names/', category_name, name='image category names'),
	url(r'^sub_category_names/', sub_category_name, name='image sub category names'),
]