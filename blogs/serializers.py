from rest_framework import serializers, exceptions
from django.contrib.auth import authenticate
from .models import Article, Choice

class ChoiceSerializer(serializers.ModelSerializer):
	id = serializers.IntegerField(required=False)

	class Meta:
		model = Choice
		fields = [
			'id',
			'question',
			'text'
		]

		read_only_fields = ('question',)
		depth = 1


class ArticleSerializer(serializers.ModelSerializer):
	choices = ChoiceSerializer(many=True)
	class Meta:
		model = Article
		fields = [
			'id',
			'title',
			'author',
			'published',
			'choices'
		]

	def create(self, validated_data):
		choices = validated_data.pop('choices')
		article = Article.objects.create(**validated_data)
		for choice in choices:
			Choice.objects.create(**choice, question=article)
		return article

	def update(self, instance, validated_data):
		choices = validated_data.pop('choices')
		instance.title = validated_data.get('title',instance.title)
		instance.save()
		keep_choices = []
		existing_ids = [c.id for c in instance.choices]
		for choice in choices:
			if 'id' in choice.keys():
				if Choice.objects.filter(id=choice['id']).exists():
					c = Choice.objects.get(id=choice['id'])
					c.text = choice.get("text", c.text)
					c.save()
					keep_choices.append(c.id)
				else:
					continue
			else:
				c = Choice.objects.create(**choice, question=instance)
				keep_choices.append(c.id)

		for choice in instance.choices:
			if choice.id not in keep_choices:
				choice.delete()

		return instance



class LoginSerializer(serializers.Serializer):
	username = serializers.CharField()
	password = serializers.CharField()

	def validate(self, data):
		username = data.get('username', '')
		password = data.get('password', '')

		if username and password:
			user = authenticate(username=username, password=password)
			if user:
				if user.is_active:
					data["user"] = user
				else:
					msg = "User may has been deactivated."
					raise exceptions.ValidationError(msg)
			else:
				msg = "Unable to login with given credentials."
				raise exceptions.ValidationError(msg)
		else:
			msg = "Must provide username and password both."
			raise exceptions.ValidationError(msg)
		
		return data
