from django.http import HttpResponse
from django.template import Context, loader
from main.models import Test

def index(request):
    var = Test.test
    t = loader.get_template('main/index.html')
    c = Context({ 'tempvars': var, 'tempvar2': 'helloworld2'})
    return HttpResponse(t.render(c))

def index(request):
    t = loader.get_template('main/post.html')
    c = Context({})
    return HttpResponse(t.render(c))
