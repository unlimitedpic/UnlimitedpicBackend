from django.conf.urls import url
from unlimited_app.views import *


urlpatterns = [
	url(r'^main_category/', MainCategoryAPI.as_view(), name='main_category'),
	url(r'^sub_category/', SubCategoryAPI.as_view(), name='sub_category'),
	url(r'^file_type/', FileTypeAPI.as_view(), name='file_type'),
	url(r'^tags/', TagAPI.as_view(), name='tags'),
	url(r'^image_upload/', ImageUploadAPI.as_view(), name='image_upload'),
	url(r'^image_download/', ImageDownloadAPI.as_view(), name='image_download'),
	url(r'^image_details/', ImageDetailsAPI.as_view(), name='image_details'),
	url(r'^myfavorite/', MyFavoriteAPI.as_view(), name='my_favorite'),

]