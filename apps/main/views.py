from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import Context, RequestContext, loader
from main.models import Test
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, SetPasswordForm
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django import forms
from django.shortcuts import render_to_response

def index(request):
    t = loader.get_template('main/index.html')
    c = RequestContext(request, {})
    return HttpResponse(t.render(c))

def post(request):
    t = loader.get_template('main/post.html')
    c = RequestContext(request, {})
    return HttpResponse(t.render(c))
    
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
        
def profile(request):
    return render_to_response("main/profile.html", {}, context_instance=RequestContext(request))
    
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
            
            
    

    
