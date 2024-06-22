from django.urls import path
from platforms.views import combined_view

urlpatterns = [
    path('', combined_view, name='combined_view'),
]
