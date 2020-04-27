from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import *

app_name = 'blogs'
urlpatterns = [
	path('', login_required(ArticelListView.as_view(extra_context={'hello':'Ankee'})),name='blog-list'),
	path('<int:id>/', ArticleDetailView.as_view(),name='blog-detail'),
	path('<int:id>/update/', ArticleUpdateView.as_view(),name='blog-update'),
	path('<int:id>/delete/', ArticleDeleteView.as_view(),name='blog-delete'),
	path('create/', ArticleCreateView.as_view(),name='blog-create'),
]