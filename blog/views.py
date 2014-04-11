# Create your views here.
from datetime import datetime

from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from django.core.context_processors import csrf
from django.forms import ModelForm

from blog.models import Author, Post

POSTS_PER_PAGE = 10

class PostForm(ModelForm):
	'''
	A ModelForm linked to Post
	'''
	class Meta:
		model = Post
		fields = ['title', 'content', 'status']


def blog_page(request, page=1):

	c = {}
	page = int(page)

	#only want/need to display one message at a time on this page
	if not messages.get_messages(request):
		messages.info(request, "A simple blog, made with love.")

	if request.user.is_authenticated():
		c['posts'] = Post.objects.author(request.user.author)
	else:
		c['posts'] = Post.objects.public()

	last_page = (len(c['posts'])/POSTS_PER_PAGE)+1

	if page == last_page:
		c['last_page'] = True
	elif page > last_page:
		#if out of bounds, show first page
		page = 1

	#formula to slice off POSTS_PER_PAGE # of posts from the original query
	c['posts'] = c['posts'][(page-1)*POSTS_PER_PAGE:(page*POSTS_PER_PAGE)]
	c['page'] = page

	return render(request, 'blog.html', c)


@login_required
def create_post_page(request):
	'''Page view for creating a new post'''
	c = {}

	c.update(csrf(request))
	if request.method == 'POST':
		form = PostForm(request.POST)
		if form.is_valid():
			title = form.cleaned_data['title']
			content = form.cleaned_data['content']
			status = form.cleaned_data['status']
	 		request.user.author.create_post(title, content, status)
	 		messages.success(request, '"%s" has been posted.' % (title))
			return HttpResponseRedirect('/blog/')
		else:
			messages.error(request, ("Post could not be created. "
				"Please review all fields are valid."))
			c['form'] = form
	else:
		c['form'] = PostForm()

	return render(request, 'create_post.html', c)

@login_required
def edit_post_page(request, post_id):
	'''
	Page view for editing post contents.
	Gets post_id argument from URL
	'''
	
	c = {}

	c.update(csrf(request))

	post = get_object_or_404(Post, pk=int(post_id))

	if post.author != request.user.author:
		raise Http404

	if request.method == 'POST':
		received_form = PostForm(request.POST)
		if received_form.is_valid():
			post.title = received_form.cleaned_data['title']
			post.content = received_form.cleaned_data['content']
			post.status = received_form.cleaned_data['status']
			post.modified = datetime.now()
			post.save()
			messages.success(request, 'Changes have been made to "%s".' 
				% post.title)
			return HttpResponseRedirect('/blog')
		else:
			messages.error(request, ("Post could not be edited.  "
				"Please review all fields are valid."))
			c['form'] = PostForm(request.POST)

	else:
		c['form'] = PostForm(instance=post)
	

	return render(request, 'edit_post.html', c)

@login_required
def manage_posts_page(request):
	'''Not yet implemented view for Author's Post management interface'''
	pass

@login_required
def log_out(request):
	'''Log out current user'''
	messages.success(request, "%s is now logged out." % request.user)
	logout(request)
	return HttpResponseRedirect('/blog')
