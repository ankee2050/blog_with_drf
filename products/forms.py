from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
	title = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Title"}))
	description = forms.CharField(
			required=False,
			widget=forms.Textarea(
					attrs={
						"class":"new-class-name, two",
						"id":"new_id",
						"rows":20,
						"cols":100,
						"placeholder":"Write a short description..."
					}
				)
		)	
	class Meta:
		model = Product
		fields= [
			'title',
			'description',
			'price',
			'featured'
		]

	def clean_title(self, *args, **kwargs):
		title = self.cleaned_data.get('title')
		if "CFE" in title:
			return title
		else:
			raise forms.ValidationError("This is not a valid title!")

class RawProductForm(forms.Form):
	title = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Title"}))
	description = forms.CharField(
			required=False,
			widget=forms.Textarea(
					attrs={
						"class":"new-class-name, two",
						"id":"new_id",
						"rows":20,
						"cols":100,
						"placeholder":"Write a short description..."
					}
				)
		)
	price = forms.DecimalField(initial=199.99)

