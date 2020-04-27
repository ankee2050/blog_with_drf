from django.db import models
from django.urls import reverse
# Create your models here.

class ArticleManager(models.Manager):

	def get_queryset(self):
		return super().get_queryset().filter(published=False)

	def all_objects(self):
		return super().get_queryset()

	def unpublished(self):
		return self.all_objects().filter(published=False)

class Article(models.Model):
	title = models.CharField(max_length=120)
	author = models.CharField(max_length=120,blank=True,null=True)
	published = models.BooleanField(default=False)
	objects = ArticleManager()


	def get_absolute_url(self):
		return reverse('blogs:blog-detail', kwargs={"id":self.id})

	@property
	def choices(self):
		return self.choice_set.all()


class Choice(models.Model):
	question = models.ForeignKey('blogs.Article', on_delete=models.CASCADE)
	text = models.TextField(null=True, blank=True)

	def __str__(self):
		return self.text