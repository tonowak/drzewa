from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:loc_x>/<str:loc_y>/", views.location, name="location"),
]
