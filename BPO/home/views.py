from django.shortcuts import render
from django.http import request

def home_render(request):
    return render(request, 'home/home.html')
