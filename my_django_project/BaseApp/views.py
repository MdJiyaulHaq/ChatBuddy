from django.http import HttpResponse
from django.template import loader
from django.http import HttpResponse

def home(request):
  return HttpResponse('home page')

def room(request):
  return HttpResponse('Room')

def members(request):
  template = loader.get_template('myfirst.html')
  return HttpResponse(template.render())