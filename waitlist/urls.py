from django.urls import path
from .views import waitlist_view

urlpatterns = [
    path('', waitlist_view, name='waitlist'),
    
]
