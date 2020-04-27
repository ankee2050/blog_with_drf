from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Product
from .forms import ProductForm, RawProductForm
from django.http import Http404
# Create your views here.
def home_view(request, *args, **kwargs):
	obj = Product.objects.all()
	context = {
		"queryset":obj
	}
	return render(request, 'home.html', context)

def contact_view(request, *args, **kwargs):
	return render(request, 'contact.html', {})

def about_view(request, *args, **kwargs):
	my_context = {
		"my_text":"About Me",
		"my_numbers":1212,
		"my_list":[1,2,3,4],
		"my_html":"<h3>Ankee Prazz!</h3>"
	}
	return render(request, 'about.html', my_context)

def social_view(request, *args, **kwargs):
	return render(request, 'social.html', {})

def product_detail_view(request,my_id):
	obj = get_object_or_404(Product, id=my_id)
	if request.method == 'POST':
		obj.delete()
		return redirect("/")
	# try:
	# 	obj = Product.objects.get(id=my_id)
	# except Product.DoesNotExist:
	# 	raise Http404
	# context = {
	# 	'title':obj.title,
	# 	'description':obj.description,
	# }
	context = {
		'obj':obj
	}
	return render(request,"product/detail.html",context)

def product_create_view(request):
	initial_data = {
		'title':'Sample Title!',
		'description':'Sample Description!',

	}
	obj = Product.objects.get(id=11)
	form = ProductForm(request.POST or None,instance=obj)
	if form.is_valid():
		form.save()
		form = ProductForm()
	else:
		print(form.errors)
	context = {
		"form":form
	}
	return render(request,"product/create.html",context)

# def product_create_view(request):
# 	form = RawProductForm()
# 	if request.method == 'POST':
# 		form = RawProductForm(request.POST)
# 		if form.is_valid():
# 			print(form.cleaned_data)
# 			Product.objects.create(**form.cleaned_data)
# 			form = RawProductForm()
# 		else:
# 			print(form.errors)
# 	context = {
# 		"form":form
# 	}
# 	return render(request,"product/create.html",context)