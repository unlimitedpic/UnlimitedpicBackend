from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework import status
from django.core.mail import send_mail
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from unlimited_auth.models import SocialLogin


class Login(APIView):
	def post(self, request, format="json"):
		username = request.data.get('username')
		password = request.data.get('password')
		user = authenticate(request, username=username, password=password)

		if user:
			login(request,user)
			return Response({
						"user_status":user.is_authenticated, 
						"is_superuser": user.is_superuser,
						"user_id": user.id
						},
						status=status.HTTP_200_OK)
		else:
			return Response({"user_status":False}, status=status.HTTP_401_UNAUTHORIZED)

	def get(self, request, format="json"):
		user = User.objects.get(id=request.user.id)
		return Response({
					"username":user.first_name+' '+user.last_name
					},
					status=status.HTTP_200_OK)

class Logout(APIView):

	def get(self,request,format="json"):
		"""
			Destroys user's logged in session
		"""
		logout(request)
		return Response(status=status.HTTP_200_OK)

@api_view(['GET'])
def user_authentication_status(request):
	"""
		User frontend authentication verifier
		unauthenticated function - returns dict with rest status
	"""
	authentication_dict = {
			'user_status': request.user.is_authenticated
		}
	if(request.user.is_authenticated):
		authentication_dict['is_superuser'] = request.user.is_superuser

	return Response(authentication_dict, status.HTTP_200_OK)


class Register_Form(APIView):

	def post(self,request,format = "json"):

		user_name,user_email,password,first_name,last_name = (request.data.get('user_name', ''),
																	request.data.get('user_email', ''),
																		request.data.get('password', ''),
																			request.data.get('first_name', ''),
																				request.data.get('last_name', ''))
		user_profile = User.objects.create_user(username=user_name,
													first_name=first_name ,
														last_name=last_name ,
															email=user_email ,
																password=password)

		return Response("Profile Created Successful",status=status.HTTP_201_CREATED)


class ForgotPassword(APIView):
	def post(self, request, format="json"):
		email = request.data.get('email',None)
		# email = request.user.email
		print(email)

		try:
			profile_obj = User.objects.get(email=email)
			employee_name = profile_obj.first_name+ " " +profile_obj.last_name

			message = """
				Hi {},

				http://localhost:8000/api/Reset_Password/
				Click this link to reset your password.

				This is a system generated email, please do not reply to this.
				
				Sincerely,
				UnlimitedPic Team
				"""
			message = message.format(employee_name.capitalize())
			send_mail( subject="Password Rest Link",
						message = message,
						from_email = "upic2112.smtp@gmail.com",
						recipient_list = [email],
						fail_silently = True  
					)
			return Response("Mail Sent Successful!",status=status.HTTP_200_OK)
		except ObjectDoesNotExist:
			return Response("Mail Not Sent Successful",status=status.HTTP_404_NOT_FOUND)


class ResetPassword(APIView):
	"""
	Parameters: email, password
	try: password saves into database  
	Retunrn: status
	
	"""
	def post(self, request, format="json"):
		email = request.data.get('email', None)
		username = request.data.get('username', None)
		password = request.data.get('password', None)
		try:
			profile_obj = User.objects.get(Q(email=email) | Q(username = username))
			user_obj = User.objects.get(Q(email=email) | Q(username = username))
			user_obj.set_password(password)
			user_obj.save()

			return Response("Password has been changed Successfully! ",status=status.HTTP_200_OK)
		except ObjectDoesNotExist:
			return Response("Unable to change Password!",status=status.HTTP_400_BAD_REQUEST)


# class Googlelogin(APIView):
# 	def post(self,request,format="json"):
# 		provider = request.data.get('provider', None)

# 		email = request.data.get('email', None)
# 		access_token = request.data.get('access_token', None)
# 		first_name = request.data.get('given_name', None)
# 		last_name = request.data.get('family_name', None)
# 		username = request.data.get('username', None)

# 		client_id = request.data.get('client_id', None)
# 		refresh_token = request.data.get('refresh_token', None)
# 		id_token = request.data.get('id_token', None)
# 		access_token_expiry = request.data.get('access_token_expiry', None)

# 		try:
# 			user_obj = User.objects.get(email=email)


# 			try:
# 				login_obj = SocialLogin.objects.get(user=user_obj)
# 				login_obj.google_access_token = access_token
# 				login_obj.google_refresh_token = refresh_token
# 				login_obj.google_client_id = client_id
# 				login_obj.save()
# 			except ObjectDoesNotExist:
# 				social_login_obj = SocialLogin.objects.create(
# 										user=user_obj,google_client_id=client_id,
# 										google_id_token=id_token, access_token_expiry=access_token_expiry)

# 			return Response(status=status.HTTP_200_OK)

# 		except ObjectDoesNotExist:
# 			username = first_name+last_name
# 			chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
# 			password = get_random_string(6, chars)

# 			user = User.objects.create(first_name=first_name, last_name=last_name, 
# 									email=email, username=username, password=password)
# 			socail = SocialLogin.objects.create(user=user,google_client_id=client_id,
# 										google_id_token=id_token, access_token_expiry=access_token_expiry)

# 			socail.google_access_token = access_token
# 			socail.google_refresh_token = refresh_token
# 			socail.google_client_id = client_id
# 			socail.save()

# 			return Response(status=status.HTTP_200_OK)

# class Facebooklogin(APIView):

# 	def post(self,request,format="json"):
# 		provider = 'facebook'
# 		access_token = request.data.get('access_token', None)

# 		URL = request.data.get('url', None)
# 		import urllib.request, json
# 		with urllib.request.urlopen(URL) as url:
# 			data = url.read().decode()

# 		data = json.loads(data)

# 		email = data['email']
# 		first_name = data['first_name']
# 		last_name = data['last_name']
# 		username = data['name']
# 		client_id = data['id']
# 		# access_token = data['access_token']

# 		try:
# 			user_obj = User.objects.get(email=email)

# 			try:
# 				login_obj = SocialLogin.objects.get(user=user_obj)
# 				login_obj.facebook_access_token = access_token
# 				login_obj.facebook_client_id = client_id
# 				login_obj.save()
# 			except ObjectDoesNotExist:
# 				social_login_obj = SocialLogin.objects.create(user=user_obj,facebook_client_id=client_id)
# 			return Response(status=status.HTTP_200_OK)

# 		except ObjectDoesNotExist:
# 			if username:
# 				username = first_name+last_name
# 			chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
# 			password = get_random_string(6, chars)

# 			user = User.objects.create(first_name=first_name, last_name=last_name, 
# 									email=email, username=username, password=password)
# 			socail = SocialLogin.objects.create(user=user,facebook_client_id=client_id)

# 			socail.facebook_access_token = access_token
# 			socail.facebook_client_id = client_id
# 			socail.save()
# 			return Response(status=status.HTTP_200_OK)