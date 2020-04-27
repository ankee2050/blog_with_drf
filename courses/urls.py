from django.urls import path
from .views import *

app_name = 'courses'
urlpatterns = [
	path('',CourseListView.as_view(),name='course-details'),
	path('create/',CourseCreateView.as_view(),name='course-create'),
	path('<int:id>',CourseView.as_view(),name='about-course'),
	path('<int:id>/update/',CourseUpdateView.as_view(), name='update-course'),
	path('<int:id>/delete/',CourseDeleteView.as_view(), name='update-course'),
]