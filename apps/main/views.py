from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, RequestContext, loader
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, SetPasswordForm
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django import forms
from django.shortcuts import render_to_response
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core.urlresolvers import reverse

from main.models import *
import urllib2
def index(request):
	posts = Post.objects.all().order_by("-created").filter(private=False)
	paginator = Paginator(posts, 10)

	try:
		page = int(request.GET.get("page", '1'))
	except ValueError:
		page = 1
	
	try:
		posts = paginator.page(page)
	except (InvalidPage, EmptyPage):
		posts = paginator.page(paginator.num_pages)
	
	t = loader.get_template('main/index.html')
	c = RequestContext(request, {'posts':posts})
	return HttpResponse(t.render(c))

def post(request):
	if request.method == 'POST':
		username = request.user.username
		try:
			anonymous = request.POST['anonymous']
		except:
			anonymous = False
		try:
			private = request.POST['private']
		except:
			private = False
		body = request.POST['body']
		#network = request.POST['network']
		network = 'main'
		if not body:
			return render_to_response('main/post.html', {'error': 'please enter a post'}, context_instance=RequestContext(request))
		else:
			post = Post(username=username, anonymous=anonymous, private=private, body=body, network=network)
			post.save()
			return HttpResponseRedirect("/you/")
	else:
		return render_to_response('main/post.html', {}, context_instance=RequestContext(request))

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect("/login/")
    else:
        form = UserCreationForm()
    return render_to_response("main/registration.html", {'form': form,}, context_instance=RequestContext(request))
    
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                auth_login(request, user)
                return HttpResponseRedirect("/you/")
            else:
                return render_to_response('main/login.html', {'error': 'your account has been disabled.'}, context_instance=RequestContext(request))
        else:
            return render_to_response('main/login.html', {'error': 'invalid login - please try again.'}, context_instance=RequestContext(request))
    else:
        return render_to_response('main/login.html', {}, context_instance=RequestContext(request))
        
def profile(request, username):
	user = User.objects.get(username=username)
	fullname = user.first_name + " " + user.last_name
	email = user.email
	try:
		user_profile = UserProfile.objects.get(user=user.pk)
	except UserProfile.DoesNotExist:
		user_profile = UserProfile(user=user)
		user_profile.save()
	city = user_profile.city
	website_url = user_profile.website_url
	facebook_url = user_profile.facebook_url
	twitter_url = user_profile.twitter_url
	if user.pk == request.user.pk:
		your_posts = Post.objects.all().filter(username=user.username).order_by("-created")
	else:
		your_posts = Post.objects.all().filter(username=user.username).order_by("-created").filter(private=False)
	paginator = Paginator(your_posts, 10)

	try:
		page = int(request.GET.get("page", '1'))
	except ValueError:
		page = 1
	
	try:
		your_posts = paginator.page(page)
	except (InvalidPage, EmptyPage):
		your_posts = paginator.page(paginator.num_pages)
	return render_to_response("main/profile.html", {'username':user.username, 'fullname':fullname, 'email':email, 'city': city, 'website_url':website_url, 'facebook_url':facebook_url, 'twitter_url':twitter_url, 'your_posts':your_posts}, context_instance=RequestContext(request))
    
def edit_profile(request, username):
	if username is not request.user.username:
		return HttpResponseRedirect('/user/'+request.user.username+'/')
	else:
		try:
			user_profile = UserProfile.objects.get(user=request.user.pk)
		except UserProfile.DoesNotExist:
			user_profile = UserProfile(user=request.user)
			user_profile.save()
		request_variables = ['first_name', 'last_name', 'email']
		user_variables = ['city', 'website_url', 'facebook_url', 'twitter_url']
		if request.method == 'POST':
			for request_variable in request_variables:
				x = getattr(request.user, request_variable)
				if x:
					try:
						postvar = request.POST[request_variable]
						setattr(request.user, request_variable, postvar)
					except:
						setattr(request.user, request_variable, '')
				else:
					try:
						postvar = request.POST[request_variable]
						setattr(request.user, request_variable, postvar)
					except:
						pass
			for user_variable in user_variables:
				x = getattr(user_profile, user_variable)
				if x:
					try:
						postvar = request.POST[user_variable]
						setattr(user_profile, user_variable, postvar)
					except:
						setattr(user_profile, user_variable, '')
				else:
					try:
						postvar = request.POST[user_variable]
						setattr(user_profile, user_variable, postvar)
					except:
						pass
			request.user.save()
			user_profile.save()
			return HttpResponseRedirect('/you/')
		else:
			variables = request_variables + user_variables
			values = [request.user.first_name, request.user.last_name, request.user.email, user_profile.city, user_profile.website_url, user_profile.facebook_url, user_profile.twitter_url]
			list = zip(variables, values)
			return render_to_response('main/edit_profile.html', {'list': list}, context_instance=RequestContext(request))

 
def logout(request):
    if request.user.is_authenticated():
        auth_logout(request)
        return render_to_response("main/logout.html", {'message': 'you have been successfully logged out.'}, context_instance=RequestContext(request))
    else:
        return render_to_response("main/logout.html", {'error': 'you haven\'t logged in yet.'}, context_instance=RequestContext(request))
        
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(SetPasswordForm(request.POST))
        if form.is_valid():
            #new_user = form.save()
            return HttpResponseRedirect("/login/")
    else:
        form = PasswordChangeForm()
    return render_to_response("main/change_password.html", {'form': form,}, context_instance=RequestContext(request))
    
    
def edit(request, postpk):
	next_url = urllib2.unquote(request.GET.get('next'))
	post = Post.objects.get(pk=postpk)
	if request.method == 'POST':
		if post.anonymous:
			try:
				post.anonymous = request.POST['anonymous']
			except:
				post.anonymous = False
		else:
			try:
				post.anonymous = request.POST['anonymous']
			except:
				pass
		if post.private:
			try:
				post.private = request.POST['private']
			except:
				post.private = False
		else:
			try:
				post.private = request.POST['private']
			except:
				pass
		try:
			post.body = request.POST['body']
		except:
			return render_to_response('main/edit.html', {'error': 'please enter a post'}, context_instance=RequestContext(request))
		post.save()
		return HttpResponseRedirect(next_url)
	else:
		return render_to_response('main/edit.html', {'anonymous':post.anonymous, 'private':post.private, 'body':post.body}, context_instance=RequestContext(request))


def delete(request, postpk):
	next_url = urllib2.unquote(request.GET.get('next'))
	s = Post.objects.get(pk=postpk).delete()
	return HttpResponseRedirect(next_url)
