from django.db import models
from django.urls import reverse
# Create your models here.

class Course(models.Model):
	title = models.CharField(max_length=120)
	author = models.CharField(max_length=120)
	duration = models.IntegerField()

	def get_absolute_url(self):
		return reverse("courses:about-course", kwargs={"id":self.id})