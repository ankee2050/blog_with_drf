from django.db import models
from django.urls import reverse
# Create your models here.
class Product(models.Model):
	title = models.CharField(max_length=120)
	description = models.TextField(blank=True, null=True)
	price = models.DecimalField(decimal_places=2,max_digits=60,null=True)
	summary = models.TextField(default='Awesome!')
	featured = models.BooleanField(default=False)

	def get_absolute_url(self):
		return reverse("product-details", kwargs={"my_id":self.id})
		# return f"/product/{self.id}"