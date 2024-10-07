from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('year/<int:year>', views.year),
    path('age/<int:age>', views.age),
    path('members', views.members)
]