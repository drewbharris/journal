from django.http import HttpResponse
from django.template import Context, loader
from main.models import Test
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.shortcuts import render_to_response

def index(request):
    var = Test.test
    t = loader.get_template('main/index.html')
    c = Context({ 'tempvars': var, 'tempvar2': 'helloworld2'})
    return HttpResponse(t.render(c))

def post(request):
    t = loader.get_template('main/post.html')
    c = Context({})
    return HttpResponse(t.render(c))
    
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return render_to_response('registration/registration_complete.html')
    else:
        form = UserCreationForm()
        return render_to_response("registration/registration_form.html", {'form' : form})
    
