from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse

def say_hello(request):
    return render(request, 'hello.html', {'name':'Md'})
