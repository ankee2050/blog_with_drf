from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import(
		CreateView,
		DetailView,
		ListView,
		UpdateView,
		DeleteView
	)
from rest_framework import mixins, generics, viewsets, status
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from django.views.decorators.csrf import csrf_exempt
from .models import Article, Choice
from .forms import ArticleForm
from .serializers import ArticleSerializer, ChoiceSerializer, LoginSerializer
from django.contrib.auth import login as django_login, logout as django_logout
from rest_framework.authtoken.models import Token

class BlogViewSet(viewsets.ModelViewSet):
	serializer_class = ArticleSerializer
	queryset = Article.objects.all()
	lookup_field = 'id'

	@action(detail=True, methods=["GET"])
	def choices(self, request, id=None):
		articles = self.get_object()
		choices = Choice.objects.filter(question=articles)
		serializer = ChoiceSerializer(choices, many=True)
		return Response(serializer.data, status=200)

	@action(detail=True, methods=["POST"])
	def choice(self,request,id=None):
		articles = self.get_object()
		data = request.data
		data['question'] = articles.id
		serializer = ChoiceSerializer(data=data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=201)
		else:
			return Response(serializer.errors,status=400)


class TestView(generics.GenericAPIView):
	
	def get(self, request):
		return Response("Hello")
	def get(self, request, id=None):
		instance = self.get_object(id)
		serializer = ArticleSerializer(instance=instance)
		return Response(serializer.data, status=200)

class BlogListView(generics.GenericAPIView,
					mixins.ListModelMixin,
					mixins.CreateModelMixin,
					mixins.RetrieveModelMixin,
					mixins.UpdateModelMixin,
					mixins.DestroyModelMixin):

	serializer_class = ArticleSerializer
	queryset = Article.objects.all()
	lookup_field = 'id'
	authentication_classes = [TokenAuthentication, SessionAuthentication, BasicAuthentication]
	permission_classes = [IsAuthenticated, IsAdminUser]

	def get(self, request, id=None):
		if id:
			return self.retrieve(request,id)
		else:
			return self.list(request)

	def post(self, request):
		return self.create(request)

	def perform_create(self, serializer):
		serializer.save(author=self.request.user)

	def put(self, request, id=None):
		return self.update(request, id)

	def perform_update(self, serializer):
		serializer.save(author=self.request.user.username)

	def delete(self, request, id=None):
		return self.destroy(id)


class BlogAPIView(APIView):
	
	def get(self, request):
		articles = Article.objects.all()
		serializer = ArticleSerializer(articles,many=True)
		return Response(serializer.data, status=200)

	def post(self, request):
		data = request.data
		serializer = ArticleSerializer(data=data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=201)
		else:
			return Response(serializer.errors, status=400)

class BlogDetailAPIView(APIView):

	def get_object(self, id):
		try:
			return Article.objects.get(id=id)
		except Article.DoesNotExist as e:
			return Response({"Error":"Article object is not found."},status=404)

	def get(self, request, id=None):
		instance = self.get_object(id)
		serializer = ArticleSerializer(instance=instance)
		return Response(serializer.data, status=200)

	def put(self, request, id=None):
		data = request.data
		instance = self.get_object(id)
		serializer = ArticleSerializer(instance=instance, data=data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=200)
		else:
			return Response(serializer.errors, status=400)

	def patch(self, request, id=None):
		data = request.data
		instance = self.get_object(id)
		serializer = ArticleSerializer(instance=instance, data=data, partial=True)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=200)
		else:
			return Response(serializer.errors, status=400)

	def delete(self, request, id=None):
		instance = self.get_object(id)
		instance.delete()
		return HttpResponse(status=204)


@csrf_exempt
def blog(request):
	print(request.method)
	if request.method == 'GET':
		articles = Article.objects.all()
		serializer = ArticleSerializer(articles,many=True)
		return JsonResponse(serializer.data, safe=False)
	
	elif request.method == 'POST':
		json_parser = JSONParser()
		data = json_parser.parse(request)
		serializer = ArticleSerializer(data=data)
		if serializer.is_valid():
			serializer.save()
			return JsonResponse(serializer.data, status=201) # 201 - Creating Object
		else:
			return JsonResponse(serializers.errors, status=400) # 400 Bad Request

@csrf_exempt
def blog_details(request,id):
	try:
		instance = Article.objects.get(id=id)
	except Article.DoesNotExist as e:
		return JsonResponse({"error":"Article Object is not found."}, status=404)

	if request.method == 'GET':
		serializer = ArticleSerializer(instance=instance)
		return JsonResponse(serializer.data,safe=True)
	
	elif request.method == 'PUT':
		json_parser = JSONParser()
		data = json_parser.parse(request)
		serializer = ArticleSerializer(instance=instance, data=data)
		if serializer.is_valid():
			serializer.save()
			return JsonResponse(serializer.data, status=200)
		else:
			return JsonResponse(serializer.errors, status=400)

	elif request.method == 'PATCH':
		json_parser = JSONParser()
		data = json_parser.parse(request)
		serializer = ArticleSerializer(instance=instance, data=data, partial=True)
		if serializer.is_valid():
			serializer.save()
			return JsonResponse(serializer.data, status=200)
		else:
			return JsonResponse(serializer.errors, status=400)

	elif request.method == 'DELETE':
		instance.delete()
		return HttpResponse(status=204)


class ArticelListView(ListView):
	# login_url = '/login/'
	# template_name = 'blogs/article_list.html'
	queryset = Article.objects.all()

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		print(context)
		context['number'] = "another context attribute"
		return context

class ArticleDetailView(DetailView):
	queryset = Article.objects.all()

	def get_object(self):
		id_ = self.kwargs.get('id')
		return get_object_or_404(Article,id=id_)

class ArticleCreateView(CreateView):
	template_name = 'blogs/article_create.html'
	queryset = Article.objects.all()
	form_class = ArticleForm
	# success_url = '/'

	def form_valid(self,form):
		print(form.cleaned_data)
		return super().form_valid(form)

	# def get_success_url(self):
	# 	return '/'

class ArticleUpdateView(UpdateView):
	template_name = 'blogs/article_create.html'
	queryset = Article.objects.all()
	form_class = ArticleForm

	def get_object(self):
		id_ = self.kwargs.get('id')
		return get_object_or_404(Article,id=id_)

	def form_valid(self,form):
		return  super().form_valid(form)

class ArticleDeleteView(DeleteView):
	template_name = 'blogs/article_delete.html'
	# queryset = Article.objects.all()

	def get_object(self):
		id_ = self.kwargs.get('id')
		return get_object_or_404(Article,id=id_)

	def get_success_url(self):
		return reverse('blogs:blog-list')


class LoginView(APIView):
	def post(self, request):
		serializer = LoginSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		user = serializer.validated_data["user"]
		# django_login(request, user)
		token, created = Token.objects.get_or_create(user=user)
		return Response({"Token":token.key}, status=200)


class LogoutView(APIView):
	authentication_classes = (TokenAuthentication, )
	def post(self, request):
		django_logout(request)
		return Response(status=204)

