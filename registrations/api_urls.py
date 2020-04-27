from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("getting_emp", EmployeeViewSet)

# emp_list_view = EmployeeViewSet.as_view({
# 		"get":"list",
# 		"post":"create",
# 		"put":"update"
# 	})

urlpatterns = [
	path('employee/', include(router.urls)),
	path('upload/', UploadView.as_view(), name="file_upload"),
	# path('get_emp/', emp_list_view),

]