from django.shortcuts import render
from django.http import HttpResponse

def profile(request, username):
    return HttpResponse('<h1>This is the profile page! The user is {}.</h1>'.format(username))

def home(request, username):
    