from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
def index(request):
    return HttpResponse('Home')


def group_posts(request, slug):
    return HttpResponse('page group')
