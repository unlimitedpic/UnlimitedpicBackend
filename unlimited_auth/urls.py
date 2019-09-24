from django.conf.urls import url
from unlimited_auth.views import Login,\
								Logout,\
								user_authentication_status,\
								Register_Form,\
								ForgotPassword,\
								ResetPassword

urlpatterns = [
	url(r'^user/login/', Login.as_view(),name='login_user'),
	url(r'^user/logout/',Logout.as_view(), name='logout'),
	url(r'^user/auth_status/',user_authentication_status, name='auth_status'),
	url(r'^registration_form/', Register_Form.as_view(),name='Registrstion Form'),
	url(r'^ForgotPassword_Email/', ForgotPassword.as_view(),name='ForgotPassword Email'),
	url(r'^Reset_Password/', ResetPassword.as_view(),name='Reset Password'),
]