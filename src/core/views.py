from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialApp
from django.contrib.auth.decorators import login_required

def login_page(request):
    return render(request, 'login.html')

@login_required
def hello(request):
    return HttpResponse("<h1>welcome youre logged in</h1>")




