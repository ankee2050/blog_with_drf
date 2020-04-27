from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework import exceptions
from .models import Profile

class ProfileSerializer(serializers.ModelSerializer):
	class Meta:
		model = Profile
		fields = [
			'salary',
			'designation',
			'picture'
		]

class EmployeeSerializer(serializers.ModelSerializer):
	profile = ProfileSerializer(read_only=True)

	class Meta:
		 model =  User
		 fields = [
		 	'id','username','first_name',
		 	'last_name','profile','email',
		 	'is_staff','is_active','date_joined',
		 	'is_superuser'
		 ]