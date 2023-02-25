from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse


def home(request):
    return render(request, 'first.html')


def room(request):
    return render(request, 'room.html')


def members(request):
    template = loader.get_template('first.html')
    return HttpResponse(template.render())
