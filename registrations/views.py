from django.shortcuts import render, render_to_response
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from rest_framework import generics
from .serializers import EmployeeSerializer, ProfileSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters import FilterSet, rest_framework as rest_filter
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser, FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Profile



class EmployeeFilter(FilterSet):
	is_active = rest_filter.CharFilter('is_active')
	designation = rest_filter.CharFilter('profile__designation')
	min_salary = rest_filter.CharFilter(method='filter_by_min_salary')
	max_salary = rest_filter.CharFilter(method='filter_by_max_salary')

	class Meta:
		model = User
		fields = [
			'is_active','designation','username'
		]

	def filter_by_min_salary(self, queryset, name, value):
		queryset = queryset.filter(profile__salary__gt=value)
		return queryset

	def filter_by_max_salary(self, queryset, name, value):
		queryset = queryset.filter(profile__salary__lt=value)
		return queryset		

class EmployeeViewSet(viewsets.ModelViewSet):
	serializer_class = EmployeeSerializer
	queryset = User.objects.all()

	filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
	filter_class = EmployeeFilter
	# authentication_classes = (TokenAuthentication, )
	permission_classes = (IsAuthenticated, )
	parser_classes = (JSONParser, FormParser, MultiPartParser)

	ordering_fields = ('is_active','username')
	ordering = ('username',)
	search_fields = ('username','first_name')

	@action(detail=True, methods=["PUT"])
	def profile(self, request, pk=None):
		user = self.get_object()

		profile = user.profile
		serializer = ProfileSerializer(profile, data=request.data)
		if serializer.is_valid():
			print("validated")
			serializer.save()
			return Response(serializer.data, status=200)
		else:
			return Response(serializer.errors, status=400)

class UploadView(APIView):
	parser_classes = (FileUploadParser, )
	authentication_classes = (TokenAuthentication, )
	permission_classes = (IsAuthenticated, )
	def post(self, request):
		file = request.data.get('file',None)
		import pdb; pdb.set_trace()
		print(file)
		if file:
			msg = "File is uploaded!"
			return Response(msg, status=200)
		else:
			msg = "File is missing!"
			return Response(msg, status=400)

class EmployeeListView(generics.ListAPIView):
	serializer_class = EmployeeSerializer
	queryset = User.objects.all()
	filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
	# filter_fields = ('is_active', 'profile__designation', 'profile__salary')
	filter_class = EmployeeFilter
	ordering_fields = ('is_active','username')
	ordering = ('username',)
	search_fields = ('username', 'first_name','email')

	
	# def get_queryset(self):
	# 	queryset = User.objects.all()
	# 	active = self.request.query_params.get('is_active','')
	# 	if active:
	# 		if active == 'False':
	# 			active = False
	# 		elif active == 'True':
	# 			active = True
	# 		else:
	# 			return queryset
	# 		return queryset.filter(is_active=active)
	# 	return queryset



def loginpage(request):
	print("----------------------------------------")
	# username = password = ''
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username,password=password)
		if user is not None:
			if user.is_active:
				login(request,user)
				return HttpResponseRedirect('/blogs')
	return render(request,'registrations/login.html')
