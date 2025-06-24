from django.urls import path
from .views import waitlist_view, confirm_view

urlpatterns = [
    path('', waitlist_view, name='waitlist'),
    path('confirm/<uuid:token>/', confirm_view, name='waitlist-confirm'),
]
