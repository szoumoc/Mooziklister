from django.urls import path
from .views import your_view

urlpatterns = [
    path("viewcheck/", your_view),
]



