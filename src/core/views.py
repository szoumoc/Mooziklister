from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialApp

def login_page(request):
    return render(request, 'login.html')




