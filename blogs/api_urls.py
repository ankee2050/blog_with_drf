from django.urls import path,include
from .views import *
from rest_framework.routers import DefaultRouter, SimpleRouter

router = DefaultRouter()
router.register("blogset", BlogViewSet)

blog_list_view = BlogViewSet.as_view({
		"get":"list",
		"post":"create"
	})

urlpatterns = [
	path('blogset/', include(router.urls)),
	path('blogset/blog/', blog_list_view),
	path('serialized_blog/', blog),
	path('serialized_blog_byclass/', BlogAPIView.as_view()),
	path('serialized_blog/<int:id>/', blog_details),
	path('serialized_blog_byclass/<int:id>/', BlogDetailAPIView.as_view()),
	path('generics/blog/', BlogListView.as_view()),
	path('generics/blog/<int:id>/', BlogListView.as_view()),
	path('testing/blog/', TestView.as_view()),
]