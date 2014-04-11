from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.db.models import Q

class Author(models.Model):
	'''Author information, linked to User model(OneToOne)'''
	
	user = models.OneToOneField(User)
	name = models.CharField(max_length=255)
	created_date = models.DateField(auto_now_add=True)


	def __unicode__(self):
		return self.name

	def create_post(self, title, content, status):
		'''Creates a new post linked to this Author'''

		return Post.objects.create(author=self, title=title, 
			content=content, status=status)

	def get_blog_view_posts(self):
		'''
		Override Manager model so that only has access to 
		self posts and public
		'''
		return Post.objects.filter(Q(status = 1) | Q(author=self))

	def _create_author(sender, instance, created, **kwargs):
		'''
		Used in the User creation process to extend that class with an Author class
		'''
		if created:
			profile, created = Author.objects.get_or_create(user=instance, 
	    	name=instance.username)

	post_save.connect(_create_author, sender=User) 
 


class PostManager(models.Manager):
	'''
	Default manager for Post objects
	'''

	def public(self):
		'''
		query public Post objects
		'''
		return self.filter(status=1)

	def author(self, author):
		'''
		get all Author's posts and other users public posts
		''' 
		return self.filter(Q(status=1) | Q(author=author))

class Post(models.Model):
	'''
	Blog post, linked to Author (ManyToOne)
	'''

	published_date = models.DateField(auto_now_add=True)
	modified_date = models.DateField(auto_now=True)
	author = models.ForeignKey('Author')
	title = models.CharField(max_length=255)
	content = models.TextField()

	objects = PostManager()

	STATUS_SETTINGS = (
			(1, 'Public'),
			(2, 'Draft'),
			(3, 'Private'),
		)
	status = models.IntegerField(choices=STATUS_SETTINGS)

	class Meta:
		ordering = ['-published_date', '-pk']

	def __unicode__(self):
		return self.title

