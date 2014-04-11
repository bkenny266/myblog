from django.test import TestCase

from django.contrib.auth.models import User

from blog.models import *


class AuthorTest(TestCase):

	def setUp(self):
		self.u = User.objects.create(username="test_name", password="test_pass")
		self.a = self.u.author

	def test_user_linked_to_author(self):
		self.assertEqual(type(self.u.author), Author)

	def test_author_name(self):
		self.assertEqual(self.u.author.name, "test_name")

	def test_author_create_post(self):
		post = self.a.create_post("test_title", "test_content", 1)
		self.assertEqual(type(post), Post)
		self.assertEqual(post.title, "test_title")
		self.assertEqual(post.content, "test_content")
		self.assertEqual(post.status, 1)

class BlogViewTest(TestCase):
	def setUp(self):
		fixtures = ['/blog/fixtures/testdb.json']


	def test_blog_get_success(self):
		resp = self.client.get('/blog/')
		self.assertEqual(resp.status_code, 200)

	def test_blog_post_success(self):
		resp = self.client.post('/blog/')
		self.assertEqual(resp.status_code, 200)

	def test_blog_get_posts_available_as_anonymous(self):
		resp = self.client.get('/blog/')
		posts = resp.context['posts']
		page = resp.context['page']
		self.assertEqual(page, 1)
		self.assertEqual(posts, 5)
		

'''
class ConvertDateTest(test_get_lowesttCase):
	def test_good_date_conversion(self):
		d = "Mar 13 '14"
		d_converted = GameList.convert_date(d)
		self.assertEqual(d_converted, datetime.date(2014, 3, 13))

	def test_incorrect_format(self):
		d = "Mar 13 14"
		self.assertRaises(ValueError, GameList.convert_date, d)


class ConvertGameId(TestCase):
	def test_good_game_id_conversion(self):
		season = "20122013"
		game_id = "020431"
		self.assertEqual(12020431, GameList.convert_game_id(season, game_id))

	def test_game_id_conversion_season_error_message(self):
		season = "199121444"
		game_id = "020431"
		with self.assertRaises(Exception) as context:
			GameList.convert_game_id(season, game_id)
		self.assertEqual(context.exception.message, 
			"season value is 91 - should be between 12 and 19")

	def test_game_id_conversion_game_id_error_message(self):
		season = "20122013"
		game_id = "139299"
		with self.assertRaises(Exception) as context:
			GameList.convert_game_id(season, game_id)
		self.assertEqual(context.exception.message, 
			"game_id starts with 13 - should start with 02 or 03")


	def test_game_id_conversion_wrong_input_size(self):
		season = "201211111"
		game_id = "02040000"
		with self.assertRaises(Exception) as context:
			GameList.convert_game_id(season, game_id)
		self.assertEqual(context.exception.message, 
			"game_id is length 10 - should be length 8")


'''