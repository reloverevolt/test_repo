from django.test import TestCase
from posts.models import BlogPost, Recipe
from users.models import User
from django.urls import reverse
from random import shuffle
from rest_framework.test import APIClient, APITestCase    

class TestCreateStepsDraft(APITestCase):

	def setUp(self):
		self.user = User.objects.create(username='testuser')
		self.user.is_active = True
		self.user.save()
		self.access_token = self.user.tokens()['access']
		self.client = APIClient()
		self.client.credentials(
			HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
		self.recipe_data = {
				"user": self.user,
				"title": "Test Recipe",
				"slug": "test-recipe",
				"media": "test",
				"cuisine": "test cuisine",
				"servings": 2,
				"price": 1,
				"difficulty": 1,
				"dish_type": "test dish type"}
		self.recipe = Recipe.objects.create(**self.recipe_data)
		self.url = reverse('draft-recipe-steps-create', 
			kwargs={"username": self.user.username, "recipe_id": self.recipe.id})

	def test_recipe_step_create(self):
		
		data = {
			"step_number": 1,
			"step_image": "test",
			"instruction": "test instruction"
		}

		response = self.client.post(self.url, data, format='json')
		self.assertEqual(response.status_code, 201)

		
	def test_recipe_step_bulk_create(self):

		#1. Success Scenario:
		data = [{
			"step_number": i, 
			"step_image": "test", 
			"instruction": f"test {i}"} for i in range(1,5)]
		
		response = self.client.post(self.url, data, format='json')
		self.assertEqual(response.status_code, 201)


		#2. Wrong next step_number supplied (1,2,3,4) + (6,7)
		data = [{
			"step_number": i, 
			"step_image": "test", 
			"instruction": f"test {i}"} for i in range(6,8)]
		
		response = self.client.post(self.url, data, format='json')
		self.assertEqual(response.status_code, 400)

		#3. Wrong step_number order:
		shuffle(data)
		response = self.client.post(self.url, data, format='json')
		self.assertEqual(response.status_code, 400)

		#4. Wrong object supplied:
		self.url = self.url.replace('1', '2')
		response = self.client.post(self.url, data, format='json')
		self.assertEqual(response.status_code, 400)


