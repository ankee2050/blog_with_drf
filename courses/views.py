from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .models import Course
from .forms import CourseModelForm
from rest_framework import viewsets
from .serializers import EmployeeSerializer
from django.contrib.auth.models import User


class CourseObjectMixin(object):
	model = Course
	lookup = 'id'
	def get_object(self):
		lookup = self.kwargs.get(self.lookup)
		obj = None
		if lookup is not None:
			obj = get_object_or_404(self.model,id=lookup)
		return obj

class CourseCreateView(View):
	template_name = 'courses/course_create.html'
	
	def get(self, request, *args, **kwargs):
		form = CourseModelForm()
		context = {"form":form}
		return render(request,self.template_name,context)

	def post(self, request, *args, **kwargs):
		form = CourseModelForm(request.POST)
		if form.is_valid():
			form.save()
			form = CourseModelForm()
		context = {"form":form}
		return render(request,self.template_name,context)

class CourseUpdateView(CourseObjectMixin, View):
	template_name = 'courses/course_update.html'

	def get(self, request, id=None, *args, **kwargs):
		context = {}
		obj = self.get_object()
		if obj is not None:
			form = CourseModelForm(instance=obj)
			context['object'] = obj
			context['form'] = form
		return render(request,self.template_name,context)
	
	def post(self, request, id=None, *args, **kwargs):
		context = {}
		obj = self.get_object()
		if obj is not None:
			form = CourseModelForm(request.POST,instance=obj)
			if form.is_valid():
				form.save()
			context['object'] = obj
			context['form'] = form
		return render(request, self.template_name, context)


class CourseListView(View):
	queryset = Course.objects.all()
	template_name = 'courses/course_list.html'

	def get_queryset(self):
		return self.queryset

	def get(self, request, *args, **kwargs):
		context = {'object_list':self.get_queryset()}
		return render(request, self.template_name, context)

# class MyListView(CourseListView):
# 	queryset = Course.objects.filter(id=1)

class CourseDeleteView(CourseObjectMixin, View):
	template_name = 'courses/course_delete.html'

	def get(self,request,id=None,*args,**kwargs):
		context = {}
		obj = self.get_object()
		if obj is not None:
			context['object'] = obj
		return render(request,self.template_name,context)

	def post(self,request,id=None,*args,**kwargs):
		context = {}
		obj = self.get_object()
		if obj is not None:
			obj.delete()
			context['object'] = None
			return redirect('/courses')
		return render(request,self.template_name,context)

class CourseView(View):
	template_name = 'courses/course_detail.html'
	def get(self, request, id=None, *args, **kwargs):
		context = {}
		if id is not None:
			obj = get_object_or_404(Course,id=id)
			context['object'] = obj
		return render(request,self.template_name,context)

# def my_fbv(request, *args, **kwargs):
# 	return render(request,'about.html',{})

class EmployeeViewSet(viewsets.ModelViewSet):
	queryset = User.objects.all()
	serializer_class = EmployeeSerializer